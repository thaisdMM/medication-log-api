"""URL configuration for the Telegram bot endpoints."""

from django.urls import path

from telegram.views import TelegramLinkView, TelegramWebhookView

urlpatterns = [
    path("telegram/webhook/", TelegramWebhookView.as_view(), name="telegram-webhook"),
    path("telegram/link/", TelegramLinkView.as_view(), name="telegram-link"),
]
