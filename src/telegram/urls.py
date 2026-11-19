"""URL configuration for the Telegram bot endpoints."""

from django.urls import path

from telegram.views import TelegramWebhookView

urlpatterns = [
    path("telegram/webhook/", TelegramWebhookView.as_view(), name="telegram-webhook"),
]
