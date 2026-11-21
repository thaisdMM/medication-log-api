"""Updates shaped as Telegram delivers them, and the reply the webhook asks for."""

from typing import Any

from django.test import Client

WEBHOOK_URL = "/api/telegram/webhook/"
CHAT_ID = 123456789
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


def send(client: Client, secret_header: dict[str, str], update: Any) -> Any:
    """Deliver an update to the webhook with the secret, as Telegram does."""
    return client.post(
        WEBHOOK_URL, update, content_type="application/json", headers=secret_header
    )
