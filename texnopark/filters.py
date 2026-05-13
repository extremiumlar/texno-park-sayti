# filters.py
from django_filters import rest_framework as filters
from .models import (
    MainServices, News, Quote, DetailServices,
    ServiceSections, ConnectionForm, QuestionForm
)


class MainServicesFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='translations__title', lookup_expr='icontains')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = MainServices
        fields = ['title', 'slug']


class NewsFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='translations__title', lookup_expr='icontains')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = News
        fields = ['title', 'created_at']


class QuoteFilter(filters.FilterSet):
    quote_choices = filters.ChoiceFilter(choices=Quote.QUOTE_CHOICES)
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Quote
        fields = ['quote_choices', 'full_name']


class DetailServicesFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='translations__title', lookup_expr='icontains')
    detail = filters.NumberFilter(field_name='detail__id')

    class Meta:
        model = DetailServices
        fields = ['title', 'detail']


class ServiceSectionsFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='translations__title', lookup_expr='icontains')
    sections = filters.NumberFilter(field_name='sections__id')

    class Meta:
        model = ServiceSections
        fields = ['title', 'sections']


class ConnectionFormFilter(filters.FilterSet):
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = ConnectionForm
        fields = ['name', 'created_at']


class QuestionFormFilter(filters.FilterSet):
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = QuestionForm
        fields = ['name', 'created_at']