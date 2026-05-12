# config/urls.py - TAVSIYA ETILADIGAN VERSIYA
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# Tarjima qilinadigan URL'lar
urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/v1/', include('texnopark.urls')),
    prefix_default_language=True,
)

# Tarjima qilinmaydigan URL'lar (CKEditor uchun prefixsiz)
urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),  # CKEditor prefixsiz
]

# Media va static fayllar
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)