"""The bot's replies: how it reads a message and what it answers."""

from datetime import timedelta
from decimal import Decimal
from typing import Any

from medications.models import ConcentrationUnit, Medication, MedicationForm
from telegram.models import LINK_CODE_LIFETIME, TelegramLink, TelegramLinkCode
from users.models import User

LINK_CODE_MINUTES = LINK_CODE_LIFETIME // timedelta(minutes=1)
LINKED_REPLY = "Your account is linked. Send /list to see your medications in use."
INVALID_LINK_REPLY = (
    "This link is not valid. Ask for a new link and open it within "
    f"{LINK_CODE_MINUTES} minutes."
)
NOT_LINKED_REPLY = (
    "This chat is not linked to an account.\n"
    "\n"
    "Link it\n"
    "- Ask the API for a link: POST /api/telegram/link/\n"
    f"- Open the link within {LINK_CODE_MINUTES} minutes."
)
HELP_REPLY = (
    "This bot shows the medications in use in your Medication Log API account.\n"
    "\n"
    "/list\n"
    "- Shows your medications in use, with concentration and form.\n"
    "- Note: suspended medications do not appear. Change their state in the API.\n"
    "\n"
    "Unlink this chat\n"
    "- Delete the link in the API: DELETE /api/telegram/link/"
)
EMPTY_LIST_REPLY = (
    "You have no medications in use.\n"
    "\n"
    "- Add a medication in the API: POST /api/medications/\n"
    "- Suspended medications do not appear. Change their state in the API."
)
LIST_TITLE = "Your medications in use:"
LIST_CUT_LINE = "- ...and {count} more. See the full list in the API."
OTHER_UNIT = "other unit"
OTHER_FORM = "other form"
MESSAGE_LIMIT = 4096
START_COMMAND = "/start"
LIST_COMMAND = "/list"


def private_message(update: dict[str, Any] | list[Any]) -> tuple[int, str] | None:
    """Return the chat and the text of a message sent in a private chat.

    Args:
        update: The update Telegram delivers.

    Returns:
        tuple[int, str] | None: The chat id and the text, empty for a message
            without text; None when the update is not a message sent in a
            private chat.
    """
    if not isinstance(update, dict):
        return None
    message = update.get("message")
    if not isinstance(message, dict):
        return None
    chat = message.get("chat")
    if not isinstance(chat, dict):
        return None
    text = message.get("text", "")
    chat_id = chat.get("id")
    if not isinstance(text, str) or not isinstance(chat_id, int):
        return None
    if chat.get("type") != "private":
        return None
    return chat_id, text


def concentration_text(value: Decimal, unit: str) -> str:
    """Return a concentration as the list shows it.

    Args:
        value: The concentration value of a medication.
        unit: The concentration unit, empty when not chosen.

    Returns:
        str: The value without trailing zeros, then the unit when there is one.
    """
    number = f"{value.normalize():f}"
    if not unit:
        return number
    return f"{number} {OTHER_UNIT if unit == ConcentrationUnit.OTHER else unit}"


def medication_line(medication: Medication) -> str:
    """Return the line of the list that shows one medication.

    Args:
        medication: A medication of the list.

    Returns:
        str: The name, then the concentration and the form when recorded,
            separated by a middle dot.
    """
    parts = [medication.name]
    if medication.concentration_value is not None:
        parts.append(
            concentration_text(
                medication.concentration_value, medication.concentration_unit
            )
        )
    if medication.form:
        form = medication.form
        parts.append(OTHER_FORM if form == MedicationForm.OTHER else form)
    return "- " + " · ".join(parts)


def fit_in_one_message(lines: list[str]) -> str:
    """Return the list reply, cut to the message limit when it is longer.

    Args:
        lines: The lines of the list, one per medication.

    Returns:
        str: The title and every line; when that is over the limit, the title,
            as many lines as fit and a last line counting the ones left out.
    """
    shown = len(lines)
    reply = "\n".join([LIST_TITLE, *lines])
    while len(reply) > MESSAGE_LIMIT:
        shown -= 1
        cut_line = LIST_CUT_LINE.format(count=len(lines) - shown)
        reply = "\n".join([LIST_TITLE, *lines[:shown], cut_line])
    return reply


def list_reply(account: User) -> str:
    """Return the reply to the list command for the account linked to the chat.

    Args:
        account: The account linked to the chat.

    Returns:
        str: The account's medications in use, or the empty list reply.
    """
    lines = [
        medication_line(medication)
        for medication in Medication.objects.in_use_by(account)
    ]
    if not lines:
        return EMPTY_LIST_REPLY
    return fit_in_one_message(lines)


def answer_message(chat_id: int, text: str) -> str:
    """Link the chat when the message is a start with a code; return the reply.

    Args:
        chat_id: The chat the message came from.
        text: The text of the message, empty when it has none.

    Returns:
        str: The linked or not-valid reply to a start command with a code; the
            reply on how to link for a chat with no link; the list for the
            list command; the help text for anything else.
    """
    command, _, argument = text.partition(" ")
    if command == START_COMMAND and argument:
        linked = TelegramLinkCode.objects.link_chat(argument, chat_id)
        return LINKED_REPLY if linked else INVALID_LINK_REPLY
    link = TelegramLink.objects.filter(chat_id=chat_id).first()
    if link is None:
        return NOT_LINKED_REPLY
    if command == LIST_COMMAND:
        return list_reply(link.account)
    return HELP_REPLY
