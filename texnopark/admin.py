from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Count
from .models import (
    Quote, AboutCompany, MainServices, ServiceSections,
    DetailServices, News, AboutUs, Team, Aboutusimages,
    HistoryTechnopark, Questions, ConnectionForm, QuestionForm
)
from .forms import QuoteAdminForm

# ==================== CUSTOM ADMIN ACTIONS ====================
@admin.action(description="Tanlanganlarni o‘chirish")
def make_deleted(modeladmin, request, queryset):
    count = queryset.delete()
    modeladmin.message_user(request, f"{count[0]} ta obyekt o‘chirildi.")


@admin.action(description="Tanlanganlarni faollashtirish (agar active field bo‘lsa)")
def make_active(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"{updated} ta obyekt faollashtirildi.")


# ==================== QUOTE ADMIN ====================
@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    form = QuoteAdminForm
    list_display = ['full_name', 'quote_choices']
    list_filter = ['quote_choices']
    search_fields = ['full_name', ]

    def add_view(self, request, form_url='', extra_context=None):
        """Agar obyekt mavjud bo'lsa, tahrirlash sahifasiga yo'naltirish"""
        if Quote.objects.exists():
            existing_quote = Quote.objects.first()
            # messages.warning(request, "Faqat bitta iqtibos bo'lishi mumkin! Mavjud iqtibosni tahrirlayapsiz.")
            url = reverse('admin:texnopark_quote_change', args=[existing_quote.id])
            return HttpResponseRedirect(url)
        return super().add_view(request, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        """Ro'yxat o'rniga tahrirlash sahifasini ko'rsatish"""
        if Quote.objects.exists():
            existing_quote = Quote.objects.first()
            url = reverse('admin:texnopark_quote_change', args=[existing_quote.id])
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context)
# ==================== ABOUT COMPANY ADMIN ====================
@admin.register(AboutCompany)
class AboutCompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'image_preview', 'has_image2')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')
    list_filter = ('created_at',)
    readonly_fields = ('image_preview', 'image2_preview', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Sarlavha', {
            'fields': ('title',)
        }),
        ('Matn (CKEditor)', {
            'fields': ('text',),
            'classes': ('wide',)
        }),
        ('Rasmlar', {
            'fields': ('image', 'image_preview', 'image2', 'image2_preview'),
            'description': 'Rasmlar formati: JPG, PNG. Tavsiya etilgan o‘lcham: 800x600'
        }),
        ('Vaqt', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit: cover;" />', obj.image.url)
        return "-"

    image_preview.short_description = 'Rasm 1'

    def image2_preview(self, obj):
        if obj.image2:
            return format_html('<img src="{}" width="80" height="60" style="object-fit: cover;" />', obj.image2.url)
        return "-"

    image2_preview.short_description = 'Rasm 2'

    def has_image2(self, obj):
        return bool(obj.image2)

    has_image2.boolean = True
    has_image2.short_description = '2-rasm bormi?'


# ==================== MAIN SERVICES ADMIN ====================
# admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import MainServices, DetailServices
from .forms import MainServicesAdminForm, QuoteAdminForm


@admin.register(MainServices)
class MainServicesAdmin(admin.ModelAdmin):
    form = MainServicesAdminForm
    list_display = ('id', 'title', 'slug', 'created_at', 'image_preview', 'detail_services_count')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'body')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'image_preview', 'detail_services_count_display')  # 'slug' ni o'chirdim
    prepopulated_fields = {'slug': ('title',)}  # Slug avtomatik generatsiya
    ordering = ('-created_at',)

    fieldsets = (
        ('Asosiy', {
            'fields': ('title', 'slug', 'image', 'image_preview')
        }),
        ('Kontent', {
            'fields': ('body',),
            'classes': ('wide',)
        }),
        ('Statistika', {
            'fields': ('detail_services_count_display', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """Rasm preview ko'rsatish"""
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="60" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = 'Rasm'
    image_preview.allow_tags = True

    def detail_services_count(self, obj):
        """Detail xizmatlar soni va link"""
        count = obj.details.count()  # related_name='details' bo'lsa
        # Agar related_name bo'lmasa:
        # count = DetailServices.objects.filter(main_service=obj).count()
        url = reverse('admin:texnopark_detailservices_changelist') + f'?main_service__id__exact={obj.id}'
        return format_html('<a href="{}" style="font-weight: bold;">{} ta</a>', url, count)

    detail_services_count.short_description = 'Detail xizmatlar'

    def detail_services_count_display(self, obj):
        """Detail xizmatlar soni ko'rsatish (readonly field)"""
        return self.detail_services_count(obj)

    detail_services_count_display.short_description = 'Bog‘langan detail xizmatlar'

    def save_model(self, request, obj, form, change):
        """Model saqlashdan oldin slug generatsiya"""
        if not obj.slug:
            from django.utils.text import slugify
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)
# ==================== SERVICE SECTIONS INLINE ====================
class ServiceSectionsInline(admin.TabularInline):
    model = ServiceSections
    extra = 1
    fields = ('title',)
    show_change_link = True


# ==================== DETAIL SERVICES INLINE ====================
class DetailServicesInline(admin.TabularInline):
    model = DetailServices
    extra = 1
    fields = ('title', 'body_small', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


# ==================== SERVICE SECTIONS ADMIN ====================
@admin.register(ServiceSections)
class ServiceSectionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'main_service_link')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('sections',)
    autocomplete_fields = ('sections',)

    def main_service_link(self, obj):
        url = reverse('admin:app_mainservices_change', args=[obj.sections.id])
        return format_html('<a href="{}">{}</a>', url, obj.sections.title)

    main_service_link.short_description = 'Asosiy xizmat'


# ==================== DETAIL SERVICES ADMIN ====================
@admin.register(DetailServices)
class DetailServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'main_service_link', 'body_preview', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'body_small')
    list_filter = ('detail', 'created_at')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('detail',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Asosiy', {
            'fields': ('title', 'detail')
        }),
        ('Matn', {
            'fields': ('body_small',)
        }),
        ('Vaqt', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def body_preview(self, obj):
        return obj.body_small[:100] + '...' if len(obj.body_small) > 100 else obj.body_small

    body_preview.short_description = 'Matn (qisqa)'

    def main_service_link(self, obj):
        url = reverse('admin:app_mainservices_change', args=[obj.detail.id])
        return format_html('<a href="{}">{}</a>', url, obj.detail.title)

    main_service_link.short_description = 'Asosiy xizmat'


# ==================== NEWS ADMIN ====================
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'img_preview', 'body_preview')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'body_small')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'img_preview')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Yangilik', {
            'fields': ('title', 'img', 'img_preview')
        }),
        ('Kontent', {
            'fields': ('body_small',),
            'classes': ('wide',)
        }),
        ('Vaqt', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def img_preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="100" height="70" style="object-fit: cover;" />', obj.img.url)
        return "-"

    img_preview.short_description = 'Rasm'

    def body_preview(self, obj):
        return mark_safe(obj.body_small[:150] + '...' if len(obj.body_small) > 150 else obj.body_small)

    body_preview.short_description = 'Matn (qisqa)'


# ==================== ABOUT US ADMIN (Singleton) ====================
@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'body_preview', 'students', 'direction', 'specialist', 'created_at')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Biz haqimizda matni', {
            'fields': ('body',)
        }),
        ('Statistika', {
            'fields': (('students', 'direction', 'specialist'),),
            'description': 'Statistik ma\'lumotlar (faqat raqamlar)'
        }),
        ('Vaqt', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def body_preview(self, obj):
        return obj.body[:100] + '...' if len(obj.body) > 100 else obj.body

    body_preview.short_description = 'Matn (qisqa)'

    def has_add_permission(self, request):
        # Singleton: faqat bitta obyekt bo‘lishi mumkin
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Singleton: o‘chirishga ruxsat yo‘q
        return False


# ==================== TEAM ADMIN ====================
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_preview', 'thumbnail')
    list_display_links = ('id',)
    readonly_fields = ('img_preview',)

    fieldsets = (
        ('Jamoa a\'zosi rasmi', {
            'fields': ('img', 'img_preview'),
            'description': 'Rasm formati: JPG, PNG. Tavsiya etilgan o‘lcham: 200x200'
        }),
    )

    def img_preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="80" height="80" style="border-radius: 50%; object-fit: cover;" />',
                               obj.img.url)
        return "-"

    img_preview.short_description = 'Rasm'

    def thumbnail(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%;" />', obj.img.url)
        return "-"

    thumbnail.short_description = 'Kichik rasm'


# ==================== ABOUT US IMAGES ADMIN ====================
@admin.register(Aboutusimages)
class AboutusimagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_preview', 'thumbnail')
    list_display_links = ('id',)
    readonly_fields = ('img_preview',)
    list_per_page = 20

    fieldsets = (
        ('Galereya rasmi', {
            'fields': ('img', 'img_preview'),
        }),
    )

    def img_preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="150" height="100" style="object-fit: cover;" />', obj.img.url)
        return "-"

    img_preview.short_description = 'Rasm'

    def thumbnail(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="50" height="35" style="object-fit: cover;" />', obj.img.url)
        return "-"

    thumbnail.short_description = 'Kichik rasm'


# ==================== HISTORY TECHNOPARK ADMIN ====================
@admin.register(HistoryTechnopark)
class HistoryTechnoparkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body_preview', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'body_small')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Tarix', {
            'fields': ('title', 'body_small')
        }),
        ('Vaqt', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def body_preview(self, obj):
        return obj.body_small[:100] + '...' if len(obj.body_small) > 100 else obj.body_small

    body_preview.short_description = 'Matn (qisqa)'


# ==================== QUESTIONS ADMIN ====================
@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer_preview', 'created_at')
    list_display_links = ('id', 'question')
    search_fields = ('question', 'answer')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    fieldsets = (
        ('Savol', {
            'fields': ('question',)
        }),
        ('Javob', {
            'fields': ('answer',)
        }),
        ('Vaqt', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def answer_preview(self, obj):
        return obj.answer[:100] + '...' if len(obj.answer) > 100 else obj.answer

    answer_preview.short_description = 'Javob (qisqa)'


# ==================== CONNECTION FORM ADMIN ====================
@admin.register(ConnectionForm)
class ConnectionFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'comfort_time', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'phone')
    list_filter = ('comfort_time', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Mijoz ma\'lumotlari', {
            'fields': (('name', 'phone'), 'comfort_time')
        }),
        ('Vaqt', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Formalar faqat frontend orqali yuboriladi, admin qo‘shish mumkin emas
        return False

    def has_change_permission(self, request, obj=None):
        # Formani o‘zgartirishga ruxsat yo‘q
        return False


# ==================== QUESTION FORM ADMIN ====================
@admin.register(QuestionForm)
class QuestionFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'company_name', 'body_preview', 'edit_allow', 'created_at')
    list_display_links = ('id', 'name')
    list_editable = ('edit_allow',)
    search_fields = ('name', 'phone', 'company_name', 'body_small')
    list_filter = ('edit_allow', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    actions = [make_deleted, make_active]

    fieldsets = (
        ('Shaxs ma\'lumotlari', {
            'fields': (('name', 'phone'), 'company_name')
        }),
        ('Savol matni', {
            'fields': ('body_small',)
        }),
        ('Ruxsatlar', {
            'fields': ('edit_allow',),
            'description': 'Tahrirlash ruxsati berilsa, foydalanuvchi o‘z savolini tahrirlay oladi'
        }),
        ('Vaqt', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def body_preview(self, obj):
        return obj.body_small[:100] + '...' if len(obj.body_small) > 100 else obj.body_small

    body_preview.short_description = 'Savol (qisqa)'


# ==================== CUSTOM ADMIN SITE CONFIGURATION ====================
admin.site.site_header = "MyProject Admin Panel"
admin.site.site_title = "MyProject Admin"
admin.site.index_title = "Boshqaruv paneliga xush kelibsiz"