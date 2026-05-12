# forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import (
    Quote, AboutCompany, MainServices, ServiceSections, DetailServices,
    News, AboutUs, Team, Aboutusimages, HistoryTechnopark, Questions,
    ConnectionForm, QuestionForm
)
import re

# Try to import CKEditor, fallback to normal Textarea if not available
try:
    from ckeditor_uploader.widgets import CKEditorUploadingWidget
    CKEDITOR_AVAILABLE = True
except ImportError:
    try:
        from ckeditor.widgets import CKEditorWidget
        CKEDITOR_AVAILABLE = True
    except ImportError:
        CKEDITOR_AVAILABLE = False


class QuoteAdminForm(forms.ModelForm):
    """Admin form for Quote model with validation"""

    class Meta:
        model = Quote
        fields = '__all__'
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'full_name': forms.TextInput(attrs={'class': 'vTextField'}),
            'phone': forms.TextInput(attrs={'placeholder': '901234567'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\d{9}$', phone):
            raise ValidationError(_('Telefon raqami aniq 9 xonali raqamdan iborat bo\'lishi kerak'))
        return phone

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body and len(body) > 500:
            raise ValidationError(_('Iqtibos matni 500 belgidan oshmasligi kerak'))
        return body


class AboutCompanyAdminForm(forms.ModelForm):
    """Admin form for AboutCompany with CKEditor support"""

    class Meta:
        model = AboutCompany
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if CKEDITOR_AVAILABLE:
            self.fields['text'].widget = CKEditorUploadingWidget() if 'ckeditor_uploader' in str(
                CKEditorUploadingWidget) else CKEditorWidget()
        else:
            self.fields['text'].widget = forms.Textarea(attrs={'rows': 10, 'cols': 80})

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) > 100:
            raise ValidationError(_('Sarlavha 100 belgidan oshmasligi kerak'))
        return title


class MainServicesAdminForm(forms.ModelForm):
    """Admin form for Main Services"""

    class Meta:
        model = MainServices
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'vTextField'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if CKEDITOR_AVAILABLE:
            self.fields['body'].widget = CKEditorUploadingWidget() if 'ckeditor_uploader' in str(
                CKEditorUploadingWidget) else CKEditorWidget()
        else:
            self.fields['body'].widget = forms.Textarea(attrs={'rows': 10, 'cols': 80})
        self.fields['body'].required = False

        if 'slug' in self.fields:
            self.fields['slug'].widget.attrs['readonly'] = True
            self.fields['slug'].help_text = _("Avtomatik ravishda sarlavhadan generatsiya qilinadi")

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) > 100:
            raise ValidationError(_('Sarlavha 100 belgidan oshmasligi kerak'))
        return title

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            title = self.cleaned_data.get('title')
            if title:
                from django.utils.text import slugify
                slug = slugify(title)
            else:
                raise ValidationError(_('Slug generatsiya qilish uchun sarlavha kiritilishi kerak'))
        return slug


class DetailServicesAdminForm(forms.ModelForm):
    """Admin form for Detail Services"""

    class Meta:
        model = DetailServices
        fields = '__all__'
        widgets = {
            'body_small': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def clean_body_small(self):
        body_small = self.cleaned_data.get('body_small')
        if body_small and len(body_small) > 300:
            raise ValidationError(_('Qisqa matn 300 belgidan oshmasligi kerak'))
        return body_small


class NewsAdminForm(forms.ModelForm):
    """Admin form for News with CKEditor support"""

    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'body_small': forms.Textarea(attrs={'rows': 3, 'cols': 60}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # News modelida 'body' fieldi yo'q, faqat 'body_small' bor
        if CKEDITOR_AVAILABLE and 'body_small' in self.fields:
            self.fields['body_small'].widget = CKEditorUploadingWidget() if 'ckeditor_uploader' in str(
                CKEditorUploadingWidget) else CKEditorWidget()

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) > 100:
            raise ValidationError(_('Sarlavha 100 belgidan oshmasligi kerak'))
        return title


class AboutUsAdminForm(forms.ModelForm):
    """Admin form for About Us with CKEditor support"""

    class Meta:
        model = AboutUs
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # AboutUs modelida faqat 'body' fieldi bor
        if CKEDITOR_AVAILABLE and 'body' in self.fields:
            self.fields['body'].widget = CKEditorUploadingWidget() if 'ckeditor_uploader' in str(
                CKEditorUploadingWidget) else CKEditorWidget()
        elif 'body' in self.fields:
            self.fields['body'].widget = forms.Textarea(attrs={'rows': 10, 'cols': 80})


class TeamAdminForm(forms.ModelForm):
    """Admin form for Team members"""

    class Meta:
        model = Team
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'vTextField'}),
            'position': forms.TextInput(attrs={'class': 'vTextField'}),
        }

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if full_name and len(full_name.strip()) < 3:
            raise ValidationError(_('Ism familiya kamida 3 belgidan iborat bo\'lishi kerak'))
        return full_name.strip()


class HistoryTechnoparkAdminForm(forms.ModelForm):
    """Admin form for History"""

    class Meta:
        model = HistoryTechnopark
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'vTextField'}),
            'body_small': forms.Textarea(attrs={'rows': 5, 'cols': 60}),
        }


class ConnectionFormAdminForm(forms.ModelForm):
    """Admin form for Connection Form (readonly for admin)"""

    class Meta:
        model = ConnectionForm
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone': forms.TextInput(attrs={'readonly': 'readonly'}),
            'comfort_time': forms.Select(attrs={'readonly': 'readonly'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\d{9}$', phone):
            raise ValidationError(_('Telefon raqami aniq 9 xonali raqamdan iborat bo\'lishi kerak'))
        return phone


class QuestionFormAdminForm(forms.ModelForm):
    """Admin form for Question Form (readonly for admin)"""

    class Meta:
        model = QuestionForm
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone': forms.TextInput(attrs={'readonly': 'readonly'}),
            'company_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'body_small': forms.Textarea(attrs={'rows': 5, 'cols': 60, 'readonly': 'readonly'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\d{9}$', phone):
            raise ValidationError(_('Telefon raqami aniq 9 xonali raqamdan iborat bo\'lishi kerak'))
        return phone

