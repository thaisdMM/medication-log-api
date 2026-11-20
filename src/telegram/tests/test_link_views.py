"""Tests for the endpoints an account uses to link its conversation with the bot."""

import hashlib
from datetime import datetime

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.fixtures import Settings
from rest_framework import serializers

from telegram.models import TelegramLink, TelegramLinkCode, TelegramLinkCodeManager
from telegram.views import BOT_NOT_CONFIGURED_MESSAGE, LINK_NOT_FOUND_MESSAGE
from users.models import User

CHAT_ID = 123456789
OTHER_CHAT_ID = 987654321
ISSUE = TelegramLinkCodeManager.issue


def as_returned(moment: datetime) -> str:
    """Return a date and time written as the API writes it."""
    return str(serializers.DateTimeField().to_representation(moment))


def issue_then_replace(
    manager: TelegramLinkCodeManager, account: User
) -> tuple[str, TelegramLinkCode]:
    """Issue a code, then replace it as a request arriving right after would.

    Args:
        manager: The link code manager.
        account: The account that asks to link its conversation.

    Returns:
        tuple[str, TelegramLinkCode]: The first code and its row, already deleted.
    """
    issued = ISSUE(manager, account)
    ISSUE(manager, account)
    return issued


@pytest.mark.django_db
def test_link_request_answers_with_a_deep_link_carrying_the_new_code(
    client: Client, account: User, account_token: str, bot_username: str
) -> None:
    """The link opens the bot with the code whose hash the database keeps."""
    response = client.post(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 201
    prefix = f"https://t.me/{bot_username}?start="
    link = response.json()["link"]
    assert link.startswith(prefix)
    code = link.removeprefix(prefix)
    stored = TelegramLinkCode.objects.get(account=account)
    assert hashlib.sha256(code.encode()).hexdigest() == stored.code_hash


@pytest.mark.django_db
def test_link_request_answers_with_when_the_new_code_expires(
    client: Client, account: User, account_token: str, bot_username: str
) -> None:
    """The expiry in the answer is the one stored with the new code."""
    response = client.post(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 201
    stored = TelegramLinkCode.objects.get(account=account)
    assert response.json()["expires_at"] == as_returned(stored.expires_at)


@pytest.mark.django_db
def test_link_request_answers_even_when_a_concurrent_request_replaces_its_code(
    client: Client,
    account_token: str,
    bot_username: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A second request issuing right after this one does not break its answer."""
    monkeypatch.setattr(TelegramLinkCodeManager, "issue", issue_then_replace)

    response = client.post(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_link_request_is_refused_while_the_bot_username_is_not_configured(
    client: Client, account_token: str, settings: Settings
) -> None:
    """Without the bot's user name there is no link to give, so the API says so."""
    settings.TELEGRAM_BOT_USERNAME = ""

    response = client.post(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 503
    assert response.json() == {"detail": BOT_NOT_CONFIGURED_MESSAGE}


@pytest.mark.django_db
def test_link_request_issues_no_code_while_the_bot_username_is_not_configured(
    client: Client, account_token: str, settings: Settings
) -> None:
    """A refused request leaves no code behind in the database."""
    settings.TELEGRAM_BOT_USERNAME = ""

    response = client.post(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 503
    assert not TelegramLinkCode.objects.exists()


@pytest.mark.django_db
def test_link_status_shows_only_when_the_account_was_linked(
    client: Client, account: User, account_token: str
) -> None:
    """A linked account sees when it was linked, and never its chat id."""
    link = TelegramLink.objects.create(account=account, chat_id=CHAT_ID)

    response = client.get(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 200
    assert response.json() == {"linked_at": as_returned(link.linked_at)}


@pytest.mark.django_db
def test_link_status_of_an_account_without_a_link_is_not_found(
    client: Client, account_token: str
) -> None:
    """An account with no link gets the project's own not-found message."""
    response = client.get(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": LINK_NOT_FOUND_MESSAGE}


@pytest.mark.django_db
def test_link_status_leaves_out_another_account_link(
    client: Client, account_token: str, other_account: User
) -> None:
    """Another account's link does not count as the requesting account's."""
    TelegramLink.objects.create(account=other_account, chat_id=OTHER_CHAT_ID)

    response = client.get(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_unlinking_answers_with_no_body(
    client: Client, account: User, account_token: str
) -> None:
    """Undoing an existing link is answered with an empty body."""
    TelegramLink.objects.create(account=account, chat_id=CHAT_ID)

    response = client.delete(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 204
    assert response.content == b""


@pytest.mark.django_db
def test_unlinking_deletes_the_account_link(
    client: Client, account: User, account_token: str
) -> None:
    """After unlinking, the account has no link in the database."""
    TelegramLink.objects.create(account=account, chat_id=CHAT_ID)

    response = client.delete(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 204
    assert not TelegramLink.objects.filter(account=account).exists()


@pytest.mark.django_db
def test_unlinking_deletes_the_account_link_codes(
    client: Client, account: User, account_token: str
) -> None:
    """After unlinking, a link code the account asked for no longer works."""
    TelegramLink.objects.create(account=account, chat_id=CHAT_ID)
    TelegramLinkCode.objects.issue(account)

    response = client.delete(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 204
    assert not TelegramLinkCode.objects.filter(account=account).exists()


@pytest.mark.django_db
def test_unlinking_an_account_without_a_link_is_not_found(
    client: Client, account_token: str
) -> None:
    """An account with no link gets the same not-found message as the status."""
    response = client.delete(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": LINK_NOT_FOUND_MESSAGE}


@pytest.mark.django_db
def test_unlinking_an_account_without_a_link_still_deletes_its_link_codes(
    client: Client, account: User, account_token: str
) -> None:
    """A link asked for but not used yet can be cancelled before anyone opens it."""
    TelegramLinkCode.objects.issue(account)

    response = client.delete(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 404
    assert not TelegramLinkCode.objects.filter(account=account).exists()


@pytest.mark.django_db
def test_unlinking_keeps_another_account_link(
    client: Client, account: User, account_token: str, other_account: User
) -> None:
    """Unlinking one account leaves another account's link in place."""
    TelegramLink.objects.create(account=account, chat_id=CHAT_ID)
    TelegramLink.objects.create(account=other_account, chat_id=OTHER_CHAT_ID)

    response = client.delete(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 204
    assert TelegramLink.objects.filter(account=other_account).exists()


@pytest.mark.django_db
def test_unlinking_keeps_another_account_link_codes(
    client: Client, account: User, account_token: str, other_account: User
) -> None:
    """Unlinking one account leaves another account's link code in place."""
    TelegramLink.objects.create(account=account, chat_id=CHAT_ID)
    TelegramLinkCode.objects.issue(other_account)

    response = client.delete(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 204
    assert TelegramLinkCode.objects.filter(account=other_account).exists()


@pytest.mark.parametrize("method", ["post", "get", "delete"])
def test_link_endpoints_refuse_a_request_without_a_token(
    client: Client, method: str
) -> None:
    """Asking for, reading or undoing a link needs the account's token."""
    response = getattr(client, method)(reverse("telegram-link"))

    assert response.status_code == 401
