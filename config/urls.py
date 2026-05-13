# config/urls.py - TAVSIYA ETILADIGAN VERSIYA
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# REST API va maxsus marshrutlar til prefiksisiz — SPA / Vite bilan ishlash osonroq
urlpatterns = [
    path("api/v1/", include("texnopark.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]

# Admin panel tarjima prefiksi bilan
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    prefix_default_language=True,
)

# Media va static fayllar
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)