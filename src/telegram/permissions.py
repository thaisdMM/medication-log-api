"""Permissions for the Telegram bot endpoints."""

import secrets

from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

SECRET_HEADER = "X-Telegram-Bot-Api-Secret-Token"


class HasTelegramWebhookSecret(BasePermission):
    """Allow only the requests that carry the secret set on the webhook."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Compare the secret sent in the request header with the configured one.

        Args:
            request: The incoming request.
            view: The view being accessed. Unused, required by DRF.

        Returns:
            bool: True when a secret is configured and the header carries it.
        """
        expected = settings.TELEGRAM_WEBHOOK_SECRET
        received = request.headers.get(SECRET_HEADER, "")
        return bool(expected) and secrets.compare_digest(
            received.encode(), expected.encode()
        )
