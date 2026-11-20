"""Serializers for the link between an account and its conversation with the bot."""

from typing import Any

from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from telegram.models import TelegramLink


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Link",
            value={
                "link": (
                    "https://t.me/medication_log_api_bot"
                    "?start=Xq3vR8kLm2Np5sTw7yZa9bCd1eFg4hJk6uVx0oQi-_A"
                ),
                "expires_at": "2026-11-20T14:15:30.123456Z",
            },
            response_only=True,
        ),
    ]
)
class TelegramLinkCodeSerializer(serializers.Serializer[dict[str, Any]]):
    """Represent a new link code as the deep link that carries it.

    Attributes:
        link: The address that opens the bot with the code.
        expires_at: When the code stops being accepted.
    """

    link = serializers.URLField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Link",
            value={"linked_at": "2026-11-20T14:07:12.654321Z"},
            response_only=True,
        ),
    ]
)
class TelegramLinkSerializer(serializers.ModelSerializer[TelegramLink]):
    """Represent the account's link without the chat id.

    Attributes:
        linked_at: When the link was made.
    """

    class Meta:
        model = TelegramLink
        fields = ("linked_at",)
        read_only_fields = fields
