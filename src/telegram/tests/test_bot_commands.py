"""Tests for the bot's replies to the list and help commands and to unlinked chats."""

import pytest
from django.test import Client

from medications.models import Medication, MedicationState
from telegram.bot import (
    EMPTY_LIST_REPLY,
    HELP_REPLY,
    LIST_CUT_LINE,
    LIST_TITLE,
    NOT_LINKED_REPLY,
)
from telegram.models import TelegramLink
from telegram.tests.updates import (
    CHAT_ID,
    GROUP_CHAT_ID,
    message_update,
    reply_to,
    send,
)
from users.models import User

CHANNEL_CHAT_ID = -100987654321
LONG_NAME_LENGTH = 250
LONG_NAMES = [letter * LONG_NAME_LENGTH for letter in "abcdefghijklmnop"]


def list_reply(*lines: str) -> str:
    """The list reply holding these lines under its title."""
    return "\n".join([LIST_TITLE, *lines])


def record_in_use(account: User, names: list[str]) -> list[str]:
    """Record medications with only a name and return their lines in the list."""
    for name in names:
        Medication.objects.create(owner=account, name=name)
    return [f"- {name}" for name in names]


@pytest.mark.django_db
def test_list_replies_with_the_medications_in_use_of_the_linked_account(
    client: Client,
    secret_header: dict[str, str],
    account: User,
    account_link: TelegramLink,
) -> None:
    """A list from a linked chat is answered with that account's medications."""
    Medication.objects.create(
        owner=account,
        name="Dipirona",
        concentration_value="500",
        concentration_unit="mg",
        form="tablet",
    )

    response = send(client, secret_header, message_update("/list"))

    assert response.status_code == 200
    assert response.json() == reply_to(
        CHAT_ID, list_reply("- Dipirona · 500 mg · tablet")
    )


@pytest.mark.django_db
def test_list_leaves_out_the_medications_of_other_accounts(
    client: Client,
    secret_header: dict[str, str],
    account: User,
    other_account: User,
    account_link: TelegramLink,
) -> None:
    """The list of a linked chat holds no medication of another account."""
    Medication.objects.create(owner=account, name="Dipirona")
    Medication.objects.create(owner=other_account, name="Losartana")

    response = send(client, secret_header, message_update("/list"))

    assert response.json()["text"] == list_reply("- Dipirona")


@pytest.mark.django_db
def test_list_leaves_out_suspended_medications(
    client: Client,
    secret_header: dict[str, str],
    account: User,
    account_link: TelegramLink,
) -> None:
    """A suspended medication does not appear in the list."""
    Medication.objects.create(owner=account, name="Dipirona")
    Medication.objects.create(
        owner=account, name="Losartana", state=MedicationState.SUSPENDED
    )

    response = send(client, secret_header, message_update("/list"))

    assert response.json()["text"] == list_reply("- Dipirona")


@pytest.mark.django_db
def test_list_sorts_the_names_ignoring_case(
    client: Client,
    secret_header: dict[str, str],
    account: User,
    account_link: TelegramLink,
) -> None:
    """The list is sorted by name, upper and lower case alike."""
    record_in_use(account, ["Dipirona", "losartana", "amoxicilina"])

    response = send(client, secret_header, message_update("/list"))

    assert response.json()["text"] == list_reply(
        "- amoxicilina", "- Dipirona", "- losartana"
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("details", "line"),
    [
        pytest.param(
            {"concentration_value": "500", "concentration_unit": "mg"},
            "- Dipirona · 500 mg",
            id="value and unit",
        ),
        pytest.param(
            {"concentration_value": "1000"}, "- Dipirona · 1000", id="value only"
        ),
        pytest.param({}, "- Dipirona", id="name only"),
        pytest.param({"concentration_unit": "mg"}, "- Dipirona", id="unit only"),
        pytest.param({"form": "drop"}, "- Dipirona · drop", id="form only"),
        pytest.param(
            {"concentration_value": "0.500", "concentration_unit": "mg"},
            "- Dipirona · 0.5 mg",
            id="value with trailing zeros",
        ),
        pytest.param(
            {"concentration_value": "100", "concentration_unit": "ml"},
            "- Dipirona · 100 ml",
            id="value ending in zeros",
        ),
        pytest.param(
            {"concentration_value": "10", "concentration_unit": "other"},
            "- Dipirona · 10 other unit",
            id="other unit",
        ),
        pytest.param({"form": "other"}, "- Dipirona · other form", id="other form"),
    ],
)
def test_list_line_shows_the_details_the_medication_has(
    client: Client,
    secret_header: dict[str, str],
    account: User,
    account_link: TelegramLink,
    details: dict[str, str],
    line: str,
) -> None:
    """Each line holds the name, then the concentration and the form when recorded."""
    Medication.objects.create(owner=account, name="Dipirona", **details)

    response = send(client, secret_header, message_update("/list"))

    assert response.json()["text"] == list_reply(line)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "recorded",
    [
        pytest.param([], id="nothing recorded"),
        pytest.param([MedicationState.SUSPENDED], id="only suspended"),
    ],
)
def test_list_without_medications_in_use_replies_with_the_empty_list_reply(
    client: Client,
    secret_header: dict[str, str],
    account: User,
    account_link: TelegramLink,
    recorded: list[MedicationState],
) -> None:
    """An account with no medication in use gets the empty list reply."""
    for state in recorded:
        Medication.objects.create(owner=account, name="Dipirona", state=state)

    response = send(client, secret_header, message_update("/list"))

    assert response.json() == reply_to(CHAT_ID, EMPTY_LIST_REPLY)


@pytest.mark.django_db
def test_list_with_words_after_the_command_is_answered_as_the_list(
    client: Client,
    secret_header: dict[str, str],
    account: User,
    account_link: TelegramLink,
) -> None:
    """Text after the list command does not change the reply."""
    Medication.objects.create(owner=account, name="Dipirona")

    response = send(client, secret_header, message_update("/list please"))

    assert response.json()["text"] == list_reply("- Dipirona")


@pytest.mark.django_db
def test_list_that_fills_one_message_exactly_is_sent_whole(
    client: Client,
    secret_header: dict[str, str],
    account: User,
    account_link: TelegramLink,
) -> None:
    """A list of exactly the message limit keeps every line and no cut line."""
    lines = record_in_use(account, [*LONG_NAMES, "q" * 21])

    response = send(client, secret_header, message_update("/list"))

    assert len(list_reply(*lines)) == 4096
    assert response.json()["text"] == list_reply(*lines)


@pytest.mark.django_db
def test_list_longer_than_one_message_is_cut_to_the_limit(
    client: Client,
    secret_header: dict[str, str],
    account: User,
    account_link: TelegramLink,
) -> None:
    """A list one character over the message limit is cut to fit it."""
    lines = record_in_use(account, [*LONG_NAMES, "q" * 22])

    response = send(client, secret_header, message_update("/list"))

    assert len(list_reply(*lines)) == 4097
    assert len(response.json()["text"]) <= 4096


@pytest.mark.django_db
def test_list_cut_keeps_as_many_medications_as_fit_and_counts_the_rest(
    client: Client,
    secret_header: dict[str, str],
    account: User,
    account_link: TelegramLink,
) -> None:
    """A cut list shows the first lines that fit and a last line with the rest."""
    lines = record_in_use(account, [*LONG_NAMES, "q" * 22])

    response = send(client, secret_header, message_update("/list"))

    assert response.json()["text"] == list_reply(
        *lines[:15], LIST_CUT_LINE.format(count=2)
    )


@pytest.mark.django_db
def test_help_replies_with_the_help_text(
    client: Client, secret_header: dict[str, str], account_link: TelegramLink
) -> None:
    """The help command from a linked chat is answered with the help text."""
    response = send(client, secret_header, message_update("/help"))

    assert response.status_code == 200
    assert response.json() == reply_to(CHAT_ID, HELP_REPLY)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "text",
    [
        pytest.param("/stop", id="unknown command"),
        pytest.param("hello", id="plain text"),
        pytest.param(None, id="message without text"),
        pytest.param("/start", id="start without a code"),
        pytest.param("/LIST", id="list in capitals"),
        pytest.param("/startle code", id="command that only begins like start"),
    ],
)
def test_other_message_from_a_linked_chat_replies_with_the_help_text(
    client: Client,
    secret_header: dict[str, str],
    account_link: TelegramLink,
    text: str | None,
) -> None:
    """Any message that is not a known command gets the help text."""
    response = send(client, secret_header, message_update(text))

    assert response.json() == reply_to(CHAT_ID, HELP_REPLY)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "text",
    [
        pytest.param("/list", id="list"),
        pytest.param("/help", id="help"),
        pytest.param("hello", id="plain text"),
        pytest.param(None, id="message without text"),
        pytest.param("/start", id="start without a code"),
        pytest.param("/startle code", id="command that only begins like start"),
    ],
)
def test_message_from_an_unlinked_chat_replies_how_to_link(
    client: Client, secret_header: dict[str, str], text: str | None
) -> None:
    """A private chat with no link gets the reply on how to link it."""
    response = send(client, secret_header, message_update(text))

    assert response.status_code == 200
    assert response.json() == reply_to(CHAT_ID, NOT_LINKED_REPLY)


@pytest.mark.django_db
def test_list_from_a_group_gets_no_reply(
    client: Client, secret_header: dict[str, str], account: User
) -> None:
    """A list sent in a group is accepted with an empty body, even if linked."""
    TelegramLink.objects.create(account=account, chat_id=GROUP_CHAT_ID)
    Medication.objects.create(owner=account, name="Dipirona")

    response = send(
        client, secret_header, message_update("/list", "group", GROUP_CHAT_ID)
    )

    assert response.status_code == 200
    assert response.content == b""


@pytest.mark.django_db
def test_message_from_an_unlinked_group_gets_no_reply(
    client: Client, secret_header: dict[str, str]
) -> None:
    """A group with no link gets no reply on how to link."""
    response = send(
        client, secret_header, message_update("hello", "group", GROUP_CHAT_ID)
    )

    assert response.status_code == 200
    assert response.content == b""


@pytest.mark.django_db
def test_post_in_a_channel_gets_no_reply(
    client: Client, secret_header: dict[str, str]
) -> None:
    """A post in a channel, which Telegram delivers as a channel post, gets no reply."""
    update = {
        "update_id": 1,
        "channel_post": {
            "message_id": 1,
            "date": 1700000000,
            "chat": {"id": CHANNEL_CHAT_ID, "type": "channel"},
            "text": "/list",
        },
    }

    response = send(client, secret_header, update)

    assert response.status_code == 200
    assert response.content == b""
