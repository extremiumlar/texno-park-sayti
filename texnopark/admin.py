from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import reverse
from parler.admin import TranslatableAdmin
from .models import (
    Quote, AboutCompany, MainServices, ServiceSections,
    DetailServices, News, AboutUs, Team, Aboutusimages,
    HistoryTechnopark, Questions, ConnectionForm, QuestionForm
)
from .forms import QuoteAdminForm, MainServicesAdminForm


@admin.action(description="Tanlanganlarni o‘chirish")
def make_deleted(modeladmin, request, queryset):
    count = queryset.delete()
    modeladmin.message_user(request, f"{count[0]} ta obyekt o‘chirildi.")


@admin.action(description="Tanlanganlarni faollashtirish")
def make_active(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"{updated} ta obyekt faollashtirildi.")


# ==================== QUOTE ADMIN ====================
@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    form = QuoteAdminForm
    list_display = ['full_name', 'quote_choices']
    list_filter = ['quote_choices']
    search_fields = ['full_name']

    def add_view(self, request, form_url='', extra_context=None):
        if Quote.objects.exists():
            existing_quote = Quote.objects.first()
            url = reverse('admin:texnopark_quote_change', args=[existing_quote.id])
            return HttpResponseRedirect(url)
        return super().add_view(request, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        if Quote.objects.exists():
            existing_quote = Quote.objects.first()
            url = reverse('admin:texnopark_quote_change', args=[existing_quote.id])
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context)


# ==================== ABOUT COMPANY ADMIN ====================
@admin.register(AboutCompany)
class AboutCompanyAdmin(TranslatableAdmin):
    list_display = ('id', 'title', 'created_at', 'image_preview', 'has_image2')
    list_display_links = ('id', 'title')
    search_fields = ('translations__title',)
    list_filter = ('created_at',)
    readonly_fields = ('image_preview', 'image2_preview', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

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

@admin.register(MainServices)
class MainServicesAdmin(TranslatableAdmin):
    form = MainServicesAdminForm
    list_display = ('id', 'title', 'slug', 'created_at', 'image_preview', 'detail_services_count')
    list_display_links = ('id', 'title')
    search_fields = ('translations__title',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'image_preview')  # slug bu yerda emas!
    # prepopulated_fields = {'slug': ('title',)}  # QAYTA QO'SHILDI! (JavaScript orqali avtomatik to'ldirish)
    ordering = ('-created_at',)

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'image', 'image_preview'),
            'description': 'Slug: Sarlavha yozilganda avtomatik to\'ldiriladi. Istasangiz o\'zgartirishingiz mumkin.'
        }),
        ('Kontent', {
            'fields': ('body',),
            'classes': ('wide',)
        }),

    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="60" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = 'Rasm'

    def detail_services_count(self, obj):
        count = obj.details.count()
        url = reverse('admin:texnopark_detailservices_changelist') + f'?detail__id__exact={obj.id}'
        return format_html('<a href="{}" style="font-weight: bold;">{} ta</a>', url, count)
    detail_services_count.short_description = 'Detail xizmatlar'



# ==================== SERVICE SECTIONS ADMIN ====================
@admin.register(ServiceSections)
class ServiceSectionsAdmin(TranslatableAdmin):
    list_display = ('id', 'title', 'main_service_link')
    list_display_links = ('id', 'title')
    search_fields = ('translations__title',)
    list_filter = ('sections',)

    def main_service_link(self, obj):
        url = reverse('admin:texnopark_mainservices_change', args=[obj.sections.id])
        return format_html('<a href="{}">{}</a>', url, obj.sections)
    main_service_link.short_description = 'Asosiy xizmat'


# ==================== DETAIL SERVICES ADMIN ====================
@admin.register(DetailServices)
class DetailServicesAdmin(TranslatableAdmin):
    list_display = ('id', 'title', 'main_service_link', 'body_preview', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('translations__title',)
    list_filter = ('detail', 'created_at')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def body_preview(self, obj):
        return obj.body_small[:100] + '...' if len(obj.body_small) > 100 else obj.body_small
    body_preview.short_description = 'Matn (qisqa)'

    def main_service_link(self, obj):
        url = reverse('admin:texnopark_mainservices_change', args=[obj.detail.id])
        return format_html('<a href="{}">{}</a>', url, obj.detail)
    main_service_link.short_description = 'Asosiy xizmat'


# ==================== NEWS ADMIN ====================
@admin.register(News)
class NewsAdmin(TranslatableAdmin):
    list_display = ('id', 'title', 'created_at', 'img_preview', 'body_preview')
    list_display_links = ('id', 'title')
    search_fields = ('translations__title',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'img_preview')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def img_preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="100" height="70" style="object-fit: cover;" />', obj.img.url)
        return "-"
    img_preview.short_description = 'Rasm'

    def body_preview(self, obj):
        return obj.body_small[:150] + '...' if len(obj.body_small) > 150 else obj.body_small
    body_preview.short_description = 'Matn (qisqa)'


# ==================== ABOUT US ADMIN ====================
@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'body_preview', 'students', 'direction', 'specialist', 'created_at')
    readonly_fields = ('created_at',)

    def body_preview(self, obj):
        return obj.body[:100] + '...' if len(obj.body) > 100 else obj.body
    body_preview.short_description = 'Matn (qisqa)'

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


# ==================== TEAM ADMIN ====================
@admin.register(Team)
class TeamAdmin(TranslatableAdmin):
    list_display = ('id', 'full_name', 'position', 'img_preview')
    list_display_links = ('id', 'full_name')
    search_fields = ('translations__full_name',)
    readonly_fields = ('img_preview',)

    def img_preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="80" height="80" style="border-radius: 50%; object-fit: cover;" />', obj.img.url)
        return "-"
    img_preview.short_description = 'Rasm'


# ==================== ABOUT US IMAGES ADMIN ====================
@admin.register(Aboutusimages)
class AboutusimagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_preview')
    list_display_links = ('id',)
    readonly_fields = ('img_preview',)

    def img_preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="150" height="100" style="object-fit: cover;" />', obj.img.url)
        return "-"
    img_preview.short_description = 'Rasm'


# ==================== HISTORY TECHNOPARK ADMIN ====================
@admin.register(HistoryTechnopark)
class HistoryTechnoparkAdmin(TranslatableAdmin):
    list_display = ('id', 'title', 'body_preview', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('translations__title',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def body_preview(self, obj):
        return obj.body_small[:100] + '...' if len(obj.body_small) > 100 else obj.body_small
    body_preview.short_description = 'Matn (qisqa)'


# ==================== QUESTIONS ADMIN ====================
@admin.register(Questions)
class QuestionsAdmin(TranslatableAdmin):
    list_display = ('id', 'question', 'answer_preview', 'created_at')
    list_display_links = ('id', 'question')
    search_fields = ('translations__question',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

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

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
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

    def body_preview(self, obj):
        return obj.body_small[:100] + '...' if len(obj.body_small) > 100 else obj.body_small
    body_preview.short_description = 'Savol (qisqa)'


# ==================== CUSTOM ADMIN SITE CONFIGURATION ====================
admin.site.site_header = "MyProject Admin Panel"
admin.site.site_title = "MyProject Admin"
admin.site.index_title = "Boshqaruv paneliga xush kelibsiz"