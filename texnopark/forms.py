# forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from parler.forms import TranslatableModelForm
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


# ==================== NON-TRANSLATABLE MODELS (ModelForm) ====================

class QuoteAdminForm(forms.ModelForm):
    """Admin form for Quote model with validation"""

    class Meta:
        model = Quote
        fields = '__all__'
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'full_name': forms.TextInput(attrs={'class': 'vTextField'}),
        }

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body and len(body) > 500:
            raise ValidationError(_('Iqtibos matni 500 belgidan oshmasligi kerak'))
        return body

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if full_name and len(full_name.strip()) < 3:
            raise ValidationError(_('Ism familiya kamida 3 belgidan iborat bo\'lishi kerak'))
        return full_name.strip()


class AboutUsAdminForm(forms.ModelForm):
    """Admin form for About Us with CKEditor support"""

    class Meta:
        model = AboutUs
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if CKEDITOR_AVAILABLE and 'body' in self.fields:
            self.fields['body'].widget = CKEditorUploadingWidget() if 'ckeditor_uploader' in str(
                CKEditorUploadingWidget) else CKEditorWidget()
        elif 'body' in self.fields:
            self.fields['body'].widget = forms.Textarea(attrs={'rows': 10, 'cols': 80})


class AboutusimagesAdminForm(forms.ModelForm):
    """Admin form for About Us Images"""

    class Meta:
        model = Aboutusimages
        fields = '__all__'


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


# ==================== TRANSLATABLE MODELS (TranslatableModelForm) ====================

class AboutCompanyAdminForm(TranslatableModelForm):
    """Admin form for AboutCompany with CKEditor support and translations"""

    class Meta:
        model = AboutCompany
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CKEditor ni tarjima qilinadigan 'text' maydoniga qo'shish
        if CKEDITOR_AVAILABLE and 'text' in self.fields:
            self.fields['text'].widget = CKEditorUploadingWidget() if 'ckeditor_uploader' in str(
                CKEditorUploadingWidget) else CKEditorWidget()
        elif 'text' in self.fields:
            self.fields['text'].widget = forms.Textarea(attrs={'rows': 10, 'cols': 80})

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) > 100:
            raise ValidationError(_('Sarlavha 100 belgidan oshmasligi kerak'))
        return title


# forms.py

class MainServicesAdminForm(TranslatableModelForm):
    """Admin form for Main Services with translations support"""

    class Meta:
        model = MainServices
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CKEditor ni tarjima qilinadigan 'body' maydoniga qo'shish
        if CKEDITOR_AVAILABLE and 'body' in self.fields:
            self.fields['body'].widget = CKEditorUploadingWidget() if 'ckeditor_uploader' in str(
                CKEditorUploadingWidget) else CKEditorWidget()
        elif 'body' in self.fields:
            self.fields['body'].widget = forms.Textarea(attrs={'rows': 10, 'cols': 80})

        # Slug maydoni - READONLY NI O'CHIRILDI
        if 'slug' in self.fields:
            # self.fields['slug'].widget.attrs['readonly'] = True  # BU QATORNI O'CHIRING!
            self.fields['slug'].help_text = _("Agar bo'sh qoldirilsa, avtomatik ravishda sarlavhadan generatsiya qilinadi")
        self.fields['body'].required = False

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
                # Tarjima qilingan title ni string ga aylantirish
                if hasattr(title, 'translate'):
                    title = str(title)
                slug = slugify(title)
            else:
                raise ValidationError(_('Slug generatsiya qilish uchun sarlavha kiritilishi kerak'))
        return slug


class ServiceSectionsAdminForm(TranslatableModelForm):
    """Admin form for Service Sections with translations"""

    class Meta:
        model = ServiceSections
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) > 100:
            raise ValidationError(_('Sarlavha 100 belgidan oshmasligi kerak'))
        return title


class DetailServicesAdminForm(TranslatableModelForm):
    """Admin form for Detail Services with translations"""

    class Meta:
        model = DetailServices
        fields = '__all__'
        widgets = {
            'body_small': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) > 100:
            raise ValidationError(_('Sarlavha 100 belgidan oshmasligi kerak'))
        return title

    def clean_body_small(self):
        body_small = self.cleaned_data.get('body_small')
        if body_small and len(body_small) > 300:
            raise ValidationError(_('Qisqa matn 300 belgidan oshmasligi kerak'))
        return body_small


class NewsAdminForm(TranslatableModelForm):
    """Admin form for News with CKEditor support and translations"""

    class Meta:
        model = News
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CKEditor ni tarjima qilinadigan 'body_small' maydoniga qo'shish
        if CKEDITOR_AVAILABLE and 'body_small' in self.fields:
            self.fields['body_small'].widget = CKEditorUploadingWidget() if 'ckeditor_uploader' in str(
                CKEditorUploadingWidget) else CKEditorWidget()
        elif 'body_small' in self.fields:
            self.fields['body_small'].widget = forms.Textarea(attrs={'rows': 15, 'cols': 80})

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) > 100:
            raise ValidationError(_('Sarlavha 100 belgidan oshmasligi kerak'))
        return title


class TeamAdminForm(TranslatableModelForm):
    """Admin form for Team members with translations"""

    class Meta:
        model = Team
        fields = '__all__'
        widgets = {
            'img': forms.ClearableFileInput(attrs={'class': 'vFileField'}),
        }

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if full_name and len(full_name.strip()) < 3:
            raise ValidationError(_('Ism familiya kamida 3 belgidan iborat bo\'lishi kerak'))
        return full_name.strip()

    def clean_position(self):
        position = self.cleaned_data.get('position')
        if position and len(position.strip()) < 3:
            raise ValidationError(_('Lavozim kamida 3 belgidan iborat bo\'lishi kerak'))
        return position.strip()


class HistoryTechnoparkAdminForm(TranslatableModelForm):
    """Admin form for History with translations"""

    class Meta:
        model = HistoryTechnopark
        fields = '__all__'
        widgets = {
            'body_small': forms.Textarea(attrs={'rows': 5, 'cols': 60}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) > 100:
            raise ValidationError(_('Sarlavha 100 belgidan oshmasligi kerak'))
        return title

    def clean_body_small(self):
        body_small = self.cleaned_data.get('body_small')
        if body_small and len(body_small) > 200:
            raise ValidationError(_('Matn 200 belgidan oshmasligi kerak'))
        return body_small


class QuestionsAdminForm(TranslatableModelForm):
    """Admin form for Questions with translations"""

    class Meta:
        model = Questions
        fields = '__all__'
        widgets = {
            'question': forms.TextInput(attrs={'class': 'vTextField'}),
            'answer': forms.Textarea(attrs={'rows': 5, 'cols': 60}),
        }

    def clean_question(self):
        question = self.cleaned_data.get('question')
        if question and len(question) > 100:
            raise ValidationError(_('Savol 100 belgidan oshmasligi kerak'))
        return question

    def clean_answer(self):
        answer = self.cleaned_data.get('answer')
        if answer and len(answer) > 200:
            raise ValidationError(_('Javob 200 belgidan oshmasligi kerak'))
        return answer
