from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class Quote(models.Model):
    QUOTE_CHOICES = [
        (_("Biz haqimizda"), 'biz_haqimizda'),
        ("Innoweek", 'innoweek'),
    ]
    full_name = models.CharField(max_length=100, verbose_name=_("To'liq ism"))
    position = models.CharField(max_length=100, verbose_name=_("Lavozim"))
    img = models.ImageField(upload_to='images/iqtibos', verbose_name=_("Rasm"))
    body = models.TextField(max_length=500, verbose_name=_("Matn"))
    quote_choices = models.CharField(
        max_length=50,
        choices=QUOTE_CHOICES,
        default='biz_haqimizda',
        verbose_name=_("Iqtibos turi")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))

    class Meta:
        verbose_name = _("Iqtibos")
        verbose_name_plural = _("Iqtiboslar")
        ordering = ['-created_at']

    def __str__(self):
        return self.body[:50]


class AboutCompany(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name=_("Sarlavha")),
        text=CKEditor5Field(verbose_name=_("Matn"), config_name='extends'),
    )
    image = models.ImageField(upload_to='images/about', verbose_name=_("Rasm 1"))
    image2 = models.ImageField(upload_to='images/about', verbose_name=_("Rasm 2"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Kompaniya haqida")
        verbose_name_plural = _("Kompaniya haqida")

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)


# models.py

class MainServices(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name=_("Sarlavha")),
        body=CKEditor5Field(verbose_name=_("Matn"), config_name='extends'),
    )
    image = models.ImageField(upload_to='images/services', verbose_name=_("Rasm"))
    slug = models.SlugField(verbose_name=_("Slug"), unique=True, blank=True)  # blank=True qo'shildi
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Asosiy xizmat")
        verbose_name_plural = _("Asosiy xizmatlar")

    def save(self, *args, **kwargs):
        if not self.slug:
            # Hozirgi til yoki default tildagi title ni olish
            default_title = self.safe_translation_getter('title', any_language=True)
            if default_title:
                self.slug = slugify(default_title)
            else:
                # Faqat inglizcha yoki boshqa til
                for lang in ['uz', 'ru', 'en']:
                    self.set_current_language(lang)
                    if self.title:
                        self.slug = slugify(self.title)
                        break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

class ServiceSections(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name=_("Sarlavha")),
    )
    sections = models.ForeignKey(
        MainServices,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name=_("Asosiy xizmat")
    )

    class Meta:
        verbose_name = _("Xizmat bo'limi")
        verbose_name_plural = _("Xizmat bo'limlari")

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)


class DetailServices(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name=_("Sarlavha")),
        body_small=models.TextField(max_length=300, verbose_name=_("Qisqa matn")),
    )
    detail = models.ForeignKey(
        MainServices,
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name=_("Asosiy xizmat")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Batafsil xizmat")
        verbose_name_plural = _("Batafsil xizmatlar")

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)


class News(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name=_("Sarlavha")),
        body_small=CKEditor5Field(verbose_name=_("Matn"), config_name='extends'),
    )
    img = models.ImageField(upload_to='images/news', verbose_name=_("Rasm"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Yangilik")
        verbose_name_plural = _("Yangiliklar")

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)


class AboutUs(models.Model):
    body = models.TextField(max_length=300, verbose_name=_("Matn"))
    students = models.IntegerField(default=0, verbose_name=_("Talabalar soni"))
    direction = models.IntegerField(default=0, verbose_name=_("Yo'nalishlar soni"))
    specialist = models.IntegerField(default=0, verbose_name=_("Mutaxassislar soni"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Biz haqimizda")
        verbose_name_plural = _("Biz haqimizda")

    def save(self, *args, **kwargs):
        if not self.pk and AboutUs.objects.exists():
            raise ValidationError(_("Faqat bitta Biz haqimizda obyekti yaratish mumkin!"))
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.body[:50]


class Team(TranslatableModel):
    translations = TranslatedFields(
        full_name=models.CharField(max_length=100, verbose_name=_("To'liq ism")),
        position=models.CharField(max_length=100, verbose_name=_("Lavozim")),
    )
    img = models.ImageField(upload_to='images/team', verbose_name=_("Rasm"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Jamoa a'zosi")
        verbose_name_plural = _("Jamoa a'zolari")

    def __str__(self):
        return self.safe_translation_getter('full_name', any_language=True)


class Aboutusimages(models.Model):
    img = models.ImageField(upload_to='images/aboutusimages', verbose_name=_("Rasm"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Biz haqimizda rasm")
        verbose_name_plural = _("Biz haqimizda rasmlar")

    def __str__(self):
        return str(self.img)


class HistoryTechnopark(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name=_("Sarlavha")),
        body_small=models.TextField(max_length=200, verbose_name=_("Qisqa matn")),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Texnopark tarixi")
        verbose_name_plural = _("Texnopark tarixi")

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)


class Questions(TranslatableModel):
    translations = TranslatedFields(
        question=models.CharField(max_length=100, verbose_name=_("Savol")),
        answer=models.TextField(max_length=200, verbose_name=_("Javob")),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Savol-javob")
        verbose_name_plural = _("Savol-javoblar")

    def __str__(self):
        return self.safe_translation_getter('question', any_language=True)


class ConnectionForm(models.Model):
    com_time = [
        ("8:00 - 10:00", _("8:00 - 10:00")),
        ("10:00 - 12:00", _("10:00 - 12:00")),
        ("14:00 - 16:00", _("14:00 - 16:00")),
    ]
    name = models.CharField(max_length=100, verbose_name=_("Ism"))
    phone = models.CharField(max_length=9, verbose_name=_("Telefon"))
    comfort_time = models.CharField(
        max_length=50,
        choices=com_time,
        default="8:00 - 10:00",
        verbose_name=_("Qulay vaqt")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Bog'lanish formasi")
        verbose_name_plural = _("Bog'lanish formalari")

    def __str__(self):
        return self.name


class QuestionForm(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Ism"))
    phone = models.CharField(max_length=9, verbose_name=_("Telefon"))
    company_name = models.CharField(max_length=100, verbose_name=_("Kompaniya nomi"))
    body_small = models.TextField(max_length=200, verbose_name=_("Savol matni"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))
    edit_allow = models.BooleanField(default=True, verbose_name=_("Tahrirlashga ruxsat"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Savol formasi")
        verbose_name_plural = _("Savol formalari")

    def __str__(self):
        return self.name