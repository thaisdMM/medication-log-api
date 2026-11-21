"""Tests for linking a chat to an account through the bot's start command."""

from datetime import timedelta
from typing import Any

import pytest
from django.test import Client
from django.utils import timezone

from telegram.models import TelegramLink, TelegramLinkCode
from telegram.views import INVALID_LINK_REPLY, LINKED_REPLY
from users.models import User

WEBHOOK_URL = "/api/telegram/webhook/"
CHAT_ID = 123456789
OTHER_CHAT_ID = 987654321
GROUP_CHAT_ID = -100123456789


def message_update(
    text: str | None, chat_type: str = "private", chat_id: int = CHAT_ID
) -> dict[str, Any]:
    """Build an update carrying a message, shaped as Telegram delivers it."""
    message: dict[str, Any] = {
        "message_id": 1,
        "date": 1700000000,
        "chat": {"id": chat_id, "type": chat_type},
    }
    if text is not None:
        message["text"] = text
    return {"update_id": 1, "message": message}


def reply_to(chat_id: int, text: str) -> dict[str, Any]:
    """The message the webhook response asks Telegram to send."""
    return {"method": "sendMessage", "chat_id": chat_id, "text": text}


@pytest.mark.django_db
def test_start_with_a_valid_code_replies_that_the_account_is_linked(
    client: Client, secret_header: dict[str, str], link_code: str
) -> None:
    """A start with a valid code is answered with the linked reply to that chat."""
    response = client.post(
        WEBHOOK_URL,
        message_update(f"/start {link_code}"),
        content_type="application/json",
        headers=secret_header,
    )

    assert response.status_code == 200
    assert response.json() == reply_to(CHAT_ID, LINKED_REPLY)


@pytest.mark.django_db
def test_start_with_a_valid_code_links_the_chat_to_the_account_that_asked_for_it(
    client: Client, secret_header: dict[str, str], account: User, link_code: str
) -> None:
    """The chat that sent the code becomes the link of the account that asked for it."""
    client.post(
        WEBHOOK_URL,
        message_update(f"/start {link_code}"),
        content_type="application/json",
        headers=secret_header,
    )

    assert TelegramLink.objects.get(account=account).chat_id == CHAT_ID


@pytest.mark.django_db
def test_start_with_a_valid_code_uses_the_code_up(
    client: Client, secret_header: dict[str, str], link_code: str
) -> None:
    """The code is deleted once it links a chat."""
    client.post(
        WEBHOOK_URL,
        message_update(f"/start {link_code}"),
        content_type="application/json",
        headers=secret_header,
    )

    assert not TelegramLinkCode.objects.exists()


@pytest.mark.django_db
def test_start_with_an_expired_code_replies_that_the_link_is_not_valid(
    client: Client, secret_header: dict[str, str], expired_link_code: str
) -> None:
    """A code past its lifetime is answered with the not-valid reply."""
    response = client.post(
        WEBHOOK_URL,
        message_update(f"/start {expired_link_code}"),
        content_type="application/json",
        headers=secret_header,
    )

    assert response.status_code == 200
    assert response.json() == reply_to(CHAT_ID, INVALID_LINK_REPLY)


@pytest.mark.django_db
def test_start_with_an_unknown_code_replies_that_the_link_is_not_valid(
    client: Client, secret_header: dict[str, str]
) -> None:
    """A code that was never issued is answered with the same not-valid reply."""
    response = client.post(
        WEBHOOK_URL,
        message_update("/start never-issued"),
        content_type="application/json",
        headers=secret_header,
    )

    assert response.status_code == 200
    assert response.json() == reply_to(CHAT_ID, INVALID_LINK_REPLY)


@pytest.mark.django_db
def test_start_with_a_used_code_replies_that_the_link_is_not_valid(
    client: Client, secret_header: dict[str, str], link_code: str
) -> None:
    """A code that already linked a chat is answered with the same not-valid reply."""
    client.post(
        WEBHOOK_URL,
        message_update(f"/start {link_code}"),
        content_type="application/json",
        headers=secret_header,
    )

    response = client.post(
        WEBHOOK_URL,
        message_update(f"/start {link_code}"),
        content_type="application/json",
        headers=secret_header,
    )

    assert response.status_code == 200
    assert response.json() == reply_to(CHAT_ID, INVALID_LINK_REPLY)


@pytest.mark.django_db
def test_start_with_an_expired_code_links_nothing(
    client: Client, secret_header: dict[str, str], expired_link_code: str
) -> None:
    """A code past its lifetime does not link the chat to its account."""
    client.post(
        WEBHOOK_URL,
        message_update(f"/start {expired_link_code}"),
        content_type="application/json",
        headers=secret_header,
    )

    assert not TelegramLink.objects.exists()


@pytest.mark.django_db
def test_start_replaces_the_account_earlier_link(
    client: Client, secret_header: dict[str, str], account: User, link_code: str
) -> None:
    """An account linked to another chat ends up linked to the new chat only."""
    TelegramLink.objects.create(account=account, chat_id=OTHER_CHAT_ID)

    client.post(
        WEBHOOK_URL,
        message_update(f"/start {link_code}"),
        content_type="application/json",
        headers=secret_header,
    )

    assert list(TelegramLink.objects.values_list("chat_id", flat=True)) == [CHAT_ID]


@pytest.mark.django_db
def test_start_takes_the_chat_from_the_account_it_was_linked_to(
    client: Client,
    secret_header: dict[str, str],
    other_account: User,
    link_code: str,
) -> None:
    """A chat linked to another account loses that link when it links a new one."""
    TelegramLink.objects.create(account=other_account, chat_id=CHAT_ID)

    client.post(
        WEBHOOK_URL,
        message_update(f"/start {link_code}"),
        content_type="application/json",
        headers=secret_header,
    )

    assert not TelegramLink.objects.filter(account=other_account).exists()


@pytest.mark.django_db
def test_start_again_from_the_linked_chat_renews_when_it_was_linked(
    client: Client,
    secret_header: dict[str, str],
    account: User,
    link_code: str,
    account_link: TelegramLink,
) -> None:
    """Linking the same chat to the same account again moves the link time forward."""
    earlier = timezone.now() - timedelta(days=1)
    TelegramLink.objects.filter(account=account).update(linked_at=earlier)

    client.post(
        WEBHOOK_URL,
        message_update(f"/start {link_code}"),
        content_type="application/json",
        headers=secret_header,
    )

    assert TelegramLink.objects.get(account=account).linked_at > earlier


@pytest.mark.django_db
def test_start_from_a_group_gets_no_reply(
    client: Client, secret_header: dict[str, str], link_code: str
) -> None:
    """A start sent in a group chat is accepted with an empty body."""
    response = client.post(
        WEBHOOK_URL,
        message_update(f"/start {link_code}", "group", GROUP_CHAT_ID),
        content_type="application/json",
        headers=secret_header,
    )

    assert response.status_code == 200
    assert response.content == b""


@pytest.mark.django_db
def test_start_from_a_group_leaves_the_code_unused(
    client: Client, secret_header: dict[str, str], link_code: str
) -> None:
    """A start sent in a group chat keeps the code for the private chat."""
    client.post(
        WEBHOOK_URL,
        message_update(f"/start {link_code}", "group", GROUP_CHAT_ID),
        content_type="application/json",
        headers=secret_header,
    )

    assert TelegramLinkCode.objects.exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "text",
    [
        pytest.param("/start", id="start without a code"),
        pytest.param(None, id="message without text"),
        pytest.param("hello", id="plain text"),
        pytest.param("/startle code", id="command that only begins like start"),
    ],
)
def test_message_that_is_not_a_start_with_a_code_gets_no_reply(
    client: Client, secret_header: dict[str, str], text: str | None
) -> None:
    """A message without a start command and a code is accepted with an empty body."""
    response = client.post(
        WEBHOOK_URL,
        message_update(text),
        content_type="application/json",
        headers=secret_header,
    )

    assert response.status_code == 200
    assert response.content == b""


def test_update_that_is_not_a_json_object_gets_no_reply(
    client: Client, secret_header: dict[str, str]
) -> None:
    """A body that is a JSON list instead of an update is accepted with an empty body."""
    response = client.post(
        WEBHOOK_URL,
        [{"update_id": 1}],
        content_type="application/json",
        headers=secret_header,
    )

    assert response.status_code == 200
    assert response.content == b""


@pytest.mark.parametrize(
    "message",
    [
        pytest.param(None, id="message that is null"),
        pytest.param(
            {"chat": "private", "text": "/start code"}, id="chat that is not an object"
        ),
        pytest.param(
            {"chat": {"id": CHAT_ID, "type": "private"}, "text": None},
            id="text that is null",
        ),
        pytest.param(
            {"chat": {"type": "private"}, "text": "/start code"},
            id="private chat without an id",
        ),
    ],
)
def test_update_in_a_shape_telegram_does_not_send_gets_no_reply(
    client: Client, secret_header: dict[str, str], message: dict[str, Any] | None
) -> None:
    """An update whose message, chat, text or chat id is malformed gets an empty body."""
    response = client.post(
        WEBHOOK_URL,
        {"update_id": 1, "message": message},
        content_type="application/json",
        headers=secret_header,
    )

    assert response.status_code == 200
    assert response.content == b""
