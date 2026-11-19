"""Shared fixtures for the Telegram bot tests."""

import pytest
from pytest_django.fixtures import Settings


@pytest.fixture
def webhook_secret(settings: Settings) -> str:
    """The secret Telegram sends with every update, set for the test."""
    settings.TELEGRAM_WEBHOOK_SECRET = "test-webhook-secret_42"
    return "test-webhook-secret_42"
