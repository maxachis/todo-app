from django.middleware.csrf import get_token
from django.http import HttpResponseForbidden


class APICSRFCookieMiddleware:
    """Ensure safe API requests prime a CSRF cookie for later mutations."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/"):
            if request.method in {"GET", "HEAD", "OPTIONS"}:
                get_token(request)
            elif request.method in {"POST", "PUT", "PATCH", "DELETE"}:
                cookie_token = request.COOKIES.get("csrftoken", "")
                header_token = request.headers.get("X-CSRFToken", "")
                if not cookie_token or cookie_token != header_token:
                    return HttpResponseForbidden("CSRF token missing or invalid.")
        return self.get_response(request)
