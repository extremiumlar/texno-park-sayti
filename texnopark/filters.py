# filters.py
from django_filters import rest_framework as filters
from .models import (
    MainServices, News, Quote, DetailServices,
    ServiceSections, ConnectionForm, QuestionForm
)


class MainServicesFilter(filters.FilterSet):
    """Filter for Main Services"""
    title = filters.CharFilter(lookup_expr='icontains')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = MainServices
        fields = ['title', 'slug']  # 'order' ni o'chirib tashladim!


class NewsFilter(filters.FilterSet):
    """Filter for News"""
    title = filters.CharFilter(lookup_expr='icontains')
    body = filters.CharFilter(field_name='body', lookup_expr='icontains')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = News
        fields = ['title', 'created_at']


class QuoteFilter(filters.FilterSet):
    """Filter for Quotes"""
    quote_choices = filters.ChoiceFilter(choices=Quote.QUOTE_CHOICES)
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Quote
        fields = ['quote_choices', 'full_name']


class DetailServicesFilter(filters.FilterSet):
    """Filter for Detail Services"""
    title = filters.CharFilter(lookup_expr='icontains')
    main_service = filters.NumberFilter(field_name='main_service__id')

    class Meta:
        model = DetailServices
        fields = ['title', 'main_service']


class ServiceSectionsFilter(filters.FilterSet):
    """Filter for Service Sections"""
    title = filters.CharFilter(lookup_expr='icontains')
    main_service = filters.NumberFilter(field_name='main_service__id')

    class Meta:
        model = ServiceSections
        fields = ['title', 'main_service']


class ConnectionFormFilter(filters.FilterSet):
    """Filter for Connection Forms (Admin only)"""
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    full_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ConnectionForm
        fields = ['full_name', 'created_at']


class QuestionFormFilter(filters.FilterSet):
    """Filter for Question Forms (Admin only)"""
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    full_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = QuestionForm
        fields = ['full_name', 'created_at']