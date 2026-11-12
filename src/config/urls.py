"""URL configuration for config project."""

from http import HTTPStatus

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from config.error_handlers import (
    BAD_REQUEST_MESSAGE,
    NOT_FOUND_MESSAGE,
    PERMISSION_DENIED_MESSAGE,
    SERVER_ERROR_MESSAGE,
    JsonErrorHandler,
)
from ops.views import healthz

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/", healthz, name="healthz"),
    path("api/", include("users.urls")),
    path("api/", include("medications.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="api-docs",
    ),
]

handler400 = JsonErrorHandler(HTTPStatus.BAD_REQUEST, BAD_REQUEST_MESSAGE)
handler403 = JsonErrorHandler(HTTPStatus.FORBIDDEN, PERMISSION_DENIED_MESSAGE)
handler404 = JsonErrorHandler(HTTPStatus.NOT_FOUND, NOT_FOUND_MESSAGE)
handler500 = JsonErrorHandler(HTTPStatus.INTERNAL_SERVER_ERROR, SERVER_ERROR_MESSAGE)
