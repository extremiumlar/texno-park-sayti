# utils.py
from django.utils.translation import gettext_lazy as _
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF to standardize error responses
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    # Log the exception
    logger.error(f"Exception occurred: {str(exc)}", exc_info=True)

    # Handle Django ValidationError
    if isinstance(exc, DjangoValidationError):
        return Response({
            "success": False,
            "message": _("Validatsiya xatosi"),
            "errors": exc.message_dict if hasattr(exc, 'message_dict') else str(exc),
            "data": None
        }, status=status.HTTP_400_BAD_REQUEST)

    # Handle IntegrityError (database constraints)
    if isinstance(exc, IntegrityError):
        return Response({
            "success": False,
            "message": _("Ma'lumotlar bazasi xatosi"),
            "errors": str(exc),
            "data": None
        }, status=status.HTTP_400_BAD_REQUEST)

    # Handle not found exceptions
    if response is not None and response.status_code == status.HTTP_404_NOT_FOUND:
        return Response({
            "success": False,
            "message": _("So'ralgan ma'lumot topilmadi"),
            "errors": response.data,
            "data": None
        }, status=status.HTTP_404_NOT_FOUND)

    # Handle permission errors
    if response is not None and response.status_code == status.HTTP_403_FORBIDDEN:
        return Response({
            "success": False,
            "message": _("Sizga bu amalni bajarishga ruxsat yo'q"),
            "errors": response.data,
            "data": None
        }, status=status.HTTP_403_FORBIDDEN)

    # Handle authentication errors
    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        return Response({
            "success": False,
            "message": _("Autentifikatsiya talab qilinadi"),
            "errors": response.data,
            "data": None
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Return standardized response for other errors
    if response is not None:
        return Response({
            "success": False,
            "message": _("Xatolik yuz berdi"),
            "errors": response.data,
            "data": None
        }, status=response.status_code)

    # Handle unhandled exceptions
    return Response({
        "success": False,
        "message": _("Serverda kutilmagan xatolik yuz berdi"),
        "errors": str(exc),
        "data": None
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)