"""Tests for the endpoint Telegram delivers the bot's updates to."""

import pytest
from django.test import Client
from pytest_django.fixtures import Settings

WEBHOOK_URL = "/api/telegram/webhook/"
SECRET_HEADER = "X-Telegram-Bot-Api-Secret-Token"
UPDATE = {"update_id": 1}


def test_webhook_accepts_an_update_carrying_the_secret(
    client: Client, webhook_secret: str
) -> None:
    """An update sent with the configured secret is answered with no reply."""
    response = client.post(
        WEBHOOK_URL,
        UPDATE,
        content_type="application/json",
        headers={SECRET_HEADER: webhook_secret},
    )

    assert response.status_code == 200
    assert response.content == b""


@pytest.mark.parametrize(
    "headers",
    [
        pytest.param({SECRET_HEADER: "wrong-secret"}, id="wrong secret"),
        pytest.param({}, id="no secret"),
        pytest.param({SECRET_HEADER: "segredo-é"}, id="non-ASCII secret"),
    ],
)
def test_webhook_refuses_an_update_without_the_configured_secret(
    client: Client, webhook_secret: str, headers: dict[str, str]
) -> None:
    """An update without the configured secret is refused with the permission error."""
    response = client.post(
        WEBHOOK_URL, UPDATE, content_type="application/json", headers=headers
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "You do not have permission to perform this action."
    }


def test_webhook_refuses_every_update_when_no_secret_is_configured(
    client: Client, settings: Settings
) -> None:
    """With no secret configured, an update sending an empty secret is refused."""
    settings.TELEGRAM_WEBHOOK_SECRET = ""

    response = client.post(
        WEBHOOK_URL,
        UPDATE,
        content_type="application/json",
        headers={SECRET_HEADER: ""},
    )

    assert response.status_code == 403
