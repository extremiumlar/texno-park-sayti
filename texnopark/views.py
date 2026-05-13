# views.py
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from .models import (
    Quote, AboutCompany, MainServices, ServiceSections, DetailServices,
    News, AboutUs, Team, Aboutusimages, HistoryTechnopark, Questions,
    ConnectionForm, QuestionForm
)
from .serializers import (
    QuoteReadSerializer, QuoteWriteSerializer,
    AboutCompanyReadSerializer, AboutCompanyWriteSerializer,
    MainServicesReadSerializer, MainServicesWriteSerializer, MainServicesListSerializer,
    ServiceSectionsReadSerializer, ServiceSectionsWriteSerializer,
    DetailServicesReadSerializer, DetailServicesWriteSerializer,
    NewsReadSerializer, NewsWriteSerializer, NewsListSerializer,
    AboutUsReadSerializer, TeamReadSerializer, TeamWriteSerializer,
    AboutUsImagesReadSerializer, HistoryTechnoparkReadSerializer, HistoryTechnoparkWriteSerializer,
    QuestionsReadSerializer, QuestionsWriteSerializer,
    ConnectionFormWriteSerializer, QuestionFormWriteSerializer
)
from .filters import (
    MainServicesFilter, NewsFilter, QuoteFilter,
    DetailServicesFilter, ServiceSectionsFilter,
    ConnectionFormFilter, QuestionFormFilter
)
from rest_framework.pagination import PageNumberPagination


# ============ CUSTOM PAGINATION ============

class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination class"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class LargeResultsSetPagination(PageNumberPagination):
    """Large pagination for admin views"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200


# ============ CUSTOM PERMISSION CLASSES ============

class IsAdminOrReadOnly(permissions.BasePermission):
    """Custom permission: Admin can write, others can only read"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


# ============ VIEWSETS ============

class QuoteViewSet(viewsets.ModelViewSet):
    """
    Quote ViewSet
    Provides CRUD operations for quotes with singleton constraint
    """
    queryset = Quote.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = QuoteFilter
    search_fields = ['full_name', 'body']
    ordering_fields = ['created_at', 'full_name']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """Return appropriate serializer based on request method"""
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return QuoteWriteSerializer
        return QuoteReadSerializer

    def create(self, request, *args, **kwargs):
        """Override create to enforce singleton pattern"""
        if Quote.objects.exists():
            return Response(
                {"error": _("Faqat bitta iqtibos bo'lishi mumkin. Mavjud iqtibosni tahrirlang.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Override update to handle singleton"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get the latest quote"""
        quote = Quote.objects.first()
        if quote:
            serializer = self.get_serializer(quote)
            return Response(serializer.data)
        return Response({"message": _("Hozircha iqtibos mavjud emas")}, status=status.HTTP_404_NOT_FOUND)


class AboutCompanyViewSet(viewsets.ModelViewSet):
    """
    About Company ViewSet
    Provides CRUD operations for company information
    """
    queryset = AboutCompany.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """Return appropriate serializer based on request method"""
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return AboutCompanyWriteSerializer
        return AboutCompanyReadSerializer


# views.py

class MainServicesViewSet(viewsets.ModelViewSet):
    """
    Main Services ViewSet
    Provides CRUD operations for main services with nested sections and details
    """
    queryset = MainServices.objects.prefetch_related(
        'sections', 'details'
    ).all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MainServicesFilter
    # TO'G'RILANGAN - parler bilan ishlash uchun
    search_fields = ['translations__title', 'translations__body']  # 'title' emas!
    ordering_fields = ['translations__title', 'created_at']  # 'title' emas!
    ordering = ['-created_at']  # yoki ['translations__title']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """Return appropriate serializer based on request method and action"""
        if self.action == 'list':
            return MainServicesListSerializer
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return MainServicesWriteSerializer
        return MainServicesReadSerializer

    @action(detail=True, methods=['get'], url_path='sections')
    def get_sections(self, request, pk=None):
        """Get all sections for a specific service"""
        service = self.get_object()
        sections = service.sections.all()
        serializer = ServiceSectionsReadSerializer(sections, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='details')
    def get_details(self, request, pk=None):
        """Get all details for a specific service"""
        service = self.get_object()
        details = service.details.all()
        serializer = DetailServicesReadSerializer(details, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-slug/(?P<slug>[^/.]+)')
    def get_by_slug(self, request, slug=None):
        """Get service by slug"""
        service = get_object_or_404(MainServices, slug=slug)
        serializer = MainServicesReadSerializer(service, context={'request': request})
        return Response(serializer.data)

class ServiceSectionsViewSet(viewsets.ModelViewSet):
    """
    Service Sections ViewSet
    Provides CRUD operations for service sections
    """
    queryset = ServiceSections.objects.select_related('sections').all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceSectionsFilter
    # TO'G'RILANGAN - parler bilan ishlash uchun
    search_fields = ['translations__title']  # 'title' emas!
    ordering_fields = ['translations__title']  # 'title' emas!
    ordering = ['translations__title']  # 'title' emas!
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """Return appropriate serializer based on request method"""
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ServiceSectionsWriteSerializer
        return ServiceSectionsReadSerializer

class DetailServicesViewSet(viewsets.ModelViewSet):
    """
    Detail Services ViewSet
    Provides CRUD operations for detail services
    """
    queryset = DetailServices.objects.select_related('detail').all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DetailServicesFilter
    # TO'G'RILANGAN - parler bilan ishlash uchun
    search_fields = ['translations__title', 'translations__body_small']  # 'title' emas!
    ordering_fields = ['translations__title', 'created_at']  # 'title' emas!
    ordering = ['-created_at']  # yoki ['translations__title']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """Return appropriate serializer based on request method"""
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return DetailServicesWriteSerializer
        return DetailServicesReadSerializer


class NewsViewSet(viewsets.ModelViewSet):
    """
    News ViewSet
    Provides CRUD operations for news with view tracking
    """
    queryset = News.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NewsFilter
    search_fields = ['title', 'body_small']
    ordering_fields = ['title', 'created_at']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """Return appropriate serializer based on request method and action"""
        if self.action == 'list':
            return NewsListSerializer
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return NewsWriteSerializer
        return NewsReadSerializer

    @action(detail=False, methods=['get'], url_path='latest')
    def latest_news(self, request):
        """Get latest news items"""
        limit = request.query_params.get('limit', 3)
        try:
            limit = int(limit)
            if limit > 10:
                limit = 10
        except ValueError:
            limit = 3

        news = self.queryset.order_by('-created_at')[:limit]
        serializer = NewsListSerializer(news, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='increment-views')
    def increment_views(self, request, pk=None):
        """Manually increment view count"""
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return Response({"message": _("Ko'rishlar soni oshirildi"), "views": instance.views})


class AboutUsViewSet(viewsets.ModelViewSet):
    """
    About Us ViewSet (Singleton pattern)
    Only one instance can exist
    """
    queryset = AboutUs.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

    def get_serializer_class(self):
        return AboutUsReadSerializer

    def get_object(self):
        obj, created = AboutUs.objects.get_or_create(id=1)
        return obj

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """
    Team ViewSet
    Provides CRUD operations for team members
    """
    queryset = Team.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['full_name', 'position']
    ordering_fields = ['full_name', 'position', 'created_at']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TeamWriteSerializer
        return TeamReadSerializer


class AboutUsImagesViewSet(viewsets.ModelViewSet):
    """
    About Us Images ViewSet
    Provides CRUD operations for images in about us section
    """
    queryset = Aboutusimages.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        return AboutUsImagesReadSerializer


class HistoryTechnoparkViewSet(viewsets.ModelViewSet):
    """
    History Technopark ViewSet
    Provides CRUD operations for history timeline
    """
    queryset = HistoryTechnopark.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return HistoryTechnoparkWriteSerializer
        return HistoryTechnoparkReadSerializer


class QuestionsViewSet(viewsets.ModelViewSet):
    """
    Questions (FAQ) ViewSet
    Provides CRUD operations for frequently asked questions
    """
    queryset = Questions.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['question', 'answer']
    ordering_fields = ['question', 'created_at']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return QuestionsWriteSerializer
        return QuestionsReadSerializer


# ============ API VIEWS (For forms and contact) ============

class ContactFormAPIView(generics.CreateAPIView):
    """
    Contact Form API View
    Handles contact form submissions (no authentication required)
    """
    serializer_class = ConnectionFormWriteSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "success": True,
            "message": _("Xabaringiz muvaffaqiyatli yuborildi. Tez orada siz bilan bog'lanamiz."),
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class InquiryFormAPIView(APIView):
    """
    Savol / ariza formasi — faqat POST. GET ro'yxat yo'q (405).
    SPA uchun CSRF talab qilinmaydi (authentication o'chirilgan).
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = QuestionFormWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": _("Savolingiz muvaffaqiyatli yuborildi. Tez orada javob beramiz."),
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
                "message": _("Ma'lumotlar noto'g'ri yoki yetarli emas."),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "error": "method_not_allowed",
                "message": _("Faqat POST so'rovi qabul qilinadi."),
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class FAQsAPIView(generics.ListAPIView):
    """
    FAQs API View
    Returns all frequently asked questions
    """
    queryset = Questions.objects.all()
    serializer_class = QuestionsReadSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['question', 'answer']
    ordering_fields = ['question']


class LatestNewsAPIView(generics.ListAPIView):
    """
    Latest News API View
    Returns N latest news items
    """
    serializer_class = NewsListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        limit = self.request.query_params.get('limit', 3)
        try:
            limit = int(limit)
            if limit > 10:
                limit = 10
        except ValueError:
            limit = 3

        return News.objects.all().order_by('-created_at')[:limit]


class ServiceBySlugAPIView(generics.RetrieveAPIView):
    """
    Service by Slug API View
    Returns service details by slug
    """
    queryset = MainServices.objects.all()
    serializer_class = MainServicesReadSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'