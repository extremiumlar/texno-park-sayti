"""SPA dan keladigan til boshqaruvi — Parler tarjimalari uchun."""

from django.conf import settings
from django.utils import translation


class APIContentLanguageMiddleware:
    """
    /api/ marshrutlarida `X-App-Language: uz|en|ru` bo'lsa,
    LocaleMiddleware dan keyin qo'yiladi va aktiv tilni majburan o'rnatadi.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/"):
            code = (request.headers.get("X-App-Language") or "").strip().lower()
            if len(code) > 2:
                code = code.split("-")[0]
            valid = {c for c, _ in settings.LANGUAGES}
            if code in valid:
                translation.activate(code)
                request.LANGUAGE_CODE = code
        return self.get_response(request)
