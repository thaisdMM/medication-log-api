"""URL configuration for the user account and token authentication endpoints."""

from django.urls import path

from users.views import CurrentUserView, LoginView, UserRegistrationView

urlpatterns = [
    path("users/", UserRegistrationView.as_view(), name="user-register"),
    path("users/me/", CurrentUserView.as_view(), name="user-me"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
]
