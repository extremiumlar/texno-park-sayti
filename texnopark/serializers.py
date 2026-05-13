# serializers.py
from rest_framework import serializers
from .models import (
    Quote, AboutCompany, MainServices, ServiceSections, DetailServices,
    News, AboutUs, Team, Aboutusimages, HistoryTechnopark, Questions,
    ConnectionForm, QuestionForm
)
from django.utils.translation import gettext_lazy as _
import re


class PhoneFieldSerializer(serializers.Field):
    """Custom serializer for phone number validation"""

    def to_representation(self, value):
        return str(value) if value else None

    def to_internal_value(self, data):
        if not data:
            return None

        phone = str(data)

        if not re.match(r'^\d{9}$', phone):
            raise serializers.ValidationError(
                _("Telefon raqami 9 xonali raqamdan iborat bo'lishi kerak (masalan: 901234567)")
            )

        return phone


# ============ READ SERIALIZERS ============

class AboutUsImagesReadSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    class Meta:
        model = Aboutusimages
        fields = ['id', 'img', 'language', 'created_at']

    def get_img(self, obj):
        request = self.context.get('request')
        if obj.img and request:
            return request.build_absolute_uri(obj.img.url)
        return obj.img.url if obj.img else None

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'


class TeamReadSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'full_name', 'position', 'img', 'created_at', 'language']

    def get_img(self, obj):
        request = self.context.get('request')
        if obj.img and request:
            return request.build_absolute_uri(obj.img.url)
        return obj.img.url if obj.img else None

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'


class HistoryTechnoparkReadSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()

    class Meta:
        model = HistoryTechnopark
        fields = ['id', 'title', 'body_small', 'created_at', 'language']

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'


class QuestionsReadSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()

    class Meta:
        model = Questions
        fields = ['id', 'question', 'answer', 'created_at', 'language']

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'


class ServiceSectionsReadSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()

    class Meta:
        model = ServiceSections
        fields = ['id', 'title', 'language']

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'


class DetailServicesReadSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()

    class Meta:
        model = DetailServices
        fields = ['id', 'title', 'body_small', 'created_at', 'language']

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'


class MainServicesReadSerializer(serializers.ModelSerializer):
    sections = ServiceSectionsReadSerializer(many=True, read_only=True)
    details = DetailServicesReadSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    class Meta:
        model = MainServices
        fields = [
            'id', 'title', 'slug', 'body', 'image', 'created_at',
            'sections', 'details', 'language'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'


class NewsReadSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'body_small', 'img', 'created_at', 'language']

    def get_img(self, obj):
        request = self.context.get('request')
        if obj.img and request:
            return request.build_absolute_uri(obj.img.url)
        return obj.img.url if obj.img else None

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'


class AboutUsReadSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()

    class Meta:
        model = AboutUs
        fields = ['id', 'body', 'students', 'direction', 'specialist', 'created_at', 'language']

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'


class QuoteReadSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    class Meta:
        model = Quote
        fields = ['id', 'full_name', 'position', 'img', 'body', 'quote_choices', 'created_at', 'language']

    def get_img(self, obj):
        request = self.context.get('request')
        if obj.img and request:
            return request.build_absolute_uri(obj.img.url)
        return obj.img.url if obj.img else None

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'


class AboutCompanyReadSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image2 = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    class Meta:
        model = AboutCompany
        fields = ['id', 'title', 'text', 'image', 'image2', 'created_at', 'language']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

    def get_image2(self, obj):
        request = self.context.get('request')
        if obj.image2 and request:
            return request.build_absolute_uri(obj.image2.url)
        return obj.image2.url if obj.image2 else None

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'


# ============ WRITE SERIALIZERS ============

class QuoteWriteSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Quote
        fields = ['full_name', 'position', 'img', 'body', 'quote_choices']

    def validate_body(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError(_("Iqtibos matni 500 belgidan oshmasligi kerak"))
        return value

    def validate_full_name(self, value):
        if value and len(value.strip()) < 3:
            raise serializers.ValidationError(_("Ism familiya kamida 3 belgidan iborat bo'lishi kerak"))
        return value.strip()

    def validate_position(self, value):
        if value and len(value.strip()) < 3:
            raise serializers.ValidationError(_("Lavozim kamida 3 belgidan iborat bo'lishi kerak"))
        return value.strip()


class AboutCompanyWriteSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    image2 = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = AboutCompany
        fields = ['title', 'text', 'image', 'image2']

    def validate_title(self, value):
        if value and len(value) > 100:
            raise serializers.ValidationError(_("Sarlavha 100 belgidan oshmasligi kerak"))
        return value


class ServiceSectionsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSections
        fields = ['title', 'sections']


class DetailServicesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailServices
        fields = ['title', 'body_small', 'detail']

    def validate_body_small(self, value):
        if value and len(value) > 300:
            raise serializers.ValidationError(_("Qisqa matn 300 belgidan oshmasligi kerak"))
        return value


class MainServicesWriteSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = MainServices
        fields = ['title', 'image', 'body']

    def validate_title(self, value):
        if value and len(value) > 100:
            raise serializers.ValidationError(_("Sarlavha 100 belgidan oshmasligi kerak"))
        return value


class TeamWriteSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Team
        fields = ['full_name', 'position', 'img']


class AboutUsImagesWriteSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Aboutusimages
        fields = ['img']


class NewsWriteSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = News
        fields = ['title', 'body_small', 'img']


class HistoryTechnoparkWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryTechnopark
        fields = ['title', 'body_small']

    def validate_title(self, value):
        if value and len(value) > 100:
            raise serializers.ValidationError(_("Sarlavha 100 belgidan oshmasligi kerak"))
        return value

    def validate_body_small(self, value):
        if value and len(value) > 200:
            raise serializers.ValidationError(_("Matn 200 belgidan oshmasligi kerak"))
        return value


class QuestionsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['question', 'answer']


class ConnectionFormWriteSerializer(serializers.ModelSerializer):
    phone = PhoneFieldSerializer()

    class Meta:
        model = ConnectionForm
        fields = ['name', 'phone', 'comfort_time']

    def validate_name(self, value):
        if value and len(value.strip()) < 3:
            raise serializers.ValidationError(_("Ism familiya kamida 3 belgidan iborat bo'lishi kerak"))
        return value.strip()


class QuestionFormWriteSerializer(serializers.ModelSerializer):
    phone = PhoneFieldSerializer()

    class Meta:
        model = QuestionForm
        fields = ["name", "phone", "company_name", "body_small"]

    def validate_name(self, value):
        if not value or not str(value).strip():
            raise serializers.ValidationError(_("Ism kiritilishi shart"))
        s = str(value).strip()
        if len(s) < 2:
            raise serializers.ValidationError(_("Ism kamida 2 belgi bo'lishi kerak"))
        return s[:100]

    def validate_company_name(self, value):
        s = (value or "").strip() or "Ko'rsatilmagan"
        if len(s) < 2:
            s = "Ko'rsatilmagan"
        return s[:100]

    def validate_body_small(self, value):
        s = (value or "").strip()
        if not s:
            s = "—"
        if len(s) > 200:
            raise serializers.ValidationError(_("Matn 200 belgidan oshmasligi kerak"))
        return s


# ============ LIST SERIALIZERS ============

class MainServicesListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    class Meta:
        model = MainServices
        fields = ['id', 'title', 'slug', 'image', 'created_at', 'language']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'


class NewsListSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'body_small', 'img', 'created_at', 'language']

    def get_img(self, obj):
        request = self.context.get('request')
        if obj.img and request:
            return request.build_absolute_uri(obj.img.url)
        return obj.img.url if obj.img else None

    def get_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE if request else 'uz'
