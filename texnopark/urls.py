# texnopark/urls.py - API prefixsiz
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'quotes', views.QuoteViewSet)
router.register(r'about-company', views.AboutCompanyViewSet)
router.register(r'services', views.MainServicesViewSet)
router.register(r'service-sections', views.ServiceSectionsViewSet)
router.register(r'detail-services', views.DetailServicesViewSet)
router.register(r'news', views.NewsViewSet)
router.register(r'about-us', views.AboutUsViewSet)
router.register(r'team', views.TeamViewSet)
router.register(r'about-us-images', views.AboutUsImagesViewSet)
router.register(r'history', views.HistoryTechnoparkViewSet)
router.register(r'faqs', views.QuestionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', views.ContactFormAPIView.as_view()),
    path('inquiry/', views.InquiryFormAPIView.as_view()),
    path('faqs-list/', views.FAQsAPIView.as_view()),
    path('latest-news/', views.LatestNewsAPIView.as_view()),
    path('services/slug/<slug:slug>/', views.ServiceBySlugAPIView.as_view()),
    path('auth/', include('rest_framework.urls')),
]