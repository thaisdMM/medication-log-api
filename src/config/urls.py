"""URL configuration for config project."""

from django.contrib import admin
from django.urls import include, path

from ops.views import healthz

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/", healthz, name="healthz"),
    path("api/users/", include("users.urls")),
]
