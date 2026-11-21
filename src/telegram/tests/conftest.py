"""Shared fixtures for the Telegram bot tests."""

from datetime import timedelta

import pytest
from django.utils import timezone
from knox.models import AuthToken
from pytest_django.fixtures import Settings

from telegram.models import TelegramLink, TelegramLinkCode
from telegram.tests.updates import CHAT_ID
from users.models import User


@pytest.fixture
def webhook_secret(settings: Settings) -> str:
    """The secret Telegram sends with every update, set for the test."""
    settings.TELEGRAM_WEBHOOK_SECRET = "test-webhook-secret_42"
    return "test-webhook-secret_42"


@pytest.fixture
def secret_header(webhook_secret: str) -> dict[str, str]:
    """The header carrying the webhook secret, as Telegram sends it."""
    return {"X-Telegram-Bot-Api-Secret-Token": webhook_secret}


@pytest.fixture
def bot_username(settings: Settings) -> str:
    """The bot's user name, which the deep link points to, set for the test."""
    settings.TELEGRAM_BOT_USERNAME = "test_link_bot"
    return "test_link_bot"


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


@pytest.fixture
def account_token(account: User) -> str:
    """A valid token for the account that links its conversation."""
    _, token = AuthToken.objects.create(user=account)
    return str(token)


@pytest.fixture
def link_code(account: User) -> str:
    """A link code the account asked for and has not used yet."""
    code, _ = TelegramLinkCode.objects.issue(account)
    return code


@pytest.fixture
def expired_link_code(account: User) -> str:
    """A link code the account asked for and let expire."""
    code, stored = TelegramLinkCode.objects.issue(account)
    TelegramLinkCode.objects.filter(pk=stored.pk).update(
        expires_at=timezone.now() - timedelta(seconds=1)
    )
    return code


@pytest.fixture
def account_link(account: User) -> TelegramLink:
    """The account's link with its conversation with the bot."""
    return TelegramLink.objects.create(account=account, chat_id=CHAT_ID)
