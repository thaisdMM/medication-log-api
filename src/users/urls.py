"""URL configuration for the user account and token authentication endpoints."""

from django.urls import path
from knox import views as knox_views

from users.views import CurrentUserView, LoginView, UserRegistrationView

urlpatterns = [
    path("users/", UserRegistrationView.as_view(), name="user-register"),
    path("users/me/", CurrentUserView.as_view(), name="user-me"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/logout/", knox_views.LogoutView.as_view(), name="auth-logout"),
    path("auth/logoutall/", knox_views.LogoutAllView.as_view(), name="auth-logoutall"),
]
