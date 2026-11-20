"""Shared fixtures for the Telegram bot tests."""

import pytest
from pytest_django.fixtures import Settings

from users.models import User


@pytest.fixture
def webhook_secret(settings: Settings) -> str:
    """The secret Telegram sends with every update, set for the test."""
    settings.TELEGRAM_WEBHOOK_SECRET = "test-webhook-secret_42"
    return "test-webhook-secret_42"


@pytest.fixture
def account() -> User:
    """The account that links its conversation with the bot."""
    return User.objects.create_user(
        email="ana.ribeiro@example.com",
        name="Ana Ribeiro",
        password="Blue-Kettle-42",
    )


@pytest.fixture
def other_account() -> User:
    """A second account, unrelated to the first one."""
    return User.objects.create_user(
        email="bruno.costa@example.com",
        name="Bruno Costa",
        password="Green-Lantern-17",
    )
