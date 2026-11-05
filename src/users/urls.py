"""URL configuration for the user account and token authentication endpoints."""

from django.urls import path

from users.views import (
    AccountDeletionView,
    CurrentUserView,
    LoginView,
    LogoutAllView,
    LogoutView,
    UserRegistrationView,
)

urlpatterns = [
    path("users/", UserRegistrationView.as_view(), name="user-register"),
    path("users/me/", CurrentUserView.as_view(), name="user-me"),
    path("users/me/delete/", AccountDeletionView.as_view(), name="user-delete"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path("auth/logoutall/", LogoutAllView.as_view(), name="auth-logoutall"),
]
