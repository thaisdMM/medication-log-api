"""Tests for how the API schema treats the Telegram bot endpoints."""

from typing import Any

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.fixtures import Settings

from telegram.models import TelegramLink
from users.models import User

LINK_PATH = "/api/telegram/link/"


def get_schema(client: Client) -> dict[str, Any]:
    """Return the schema served to the Swagger UI page."""
    response = client.get("/api/schema/?format=json")
    assert response.status_code == 200
    schema: dict[str, Any] = response.json()
    return schema


def only_example(body: dict[str, Any]) -> Any:
    """Return the value of the single example of a request or response body."""
    (example,) = body["content"]["application/json"]["examples"].values()
    return example["value"]


def test_schema_leaves_out_the_webhook(client: Client) -> None:
    """The webhook is called by Telegram only, so the schema does not list it."""
    response = client.get("/api/schema/?format=json")

    assert response.status_code == 200
    assert "/api/telegram/webhook/" not in response.json()["paths"]


@pytest.mark.parametrize(
    ("method", "statuses"),
    [
        ("post", {"201", "401", "503"}),
        ("get", {"200", "401", "404"}),
        ("delete", {"204", "401", "404"}),
    ],
)
def test_schema_lists_the_responses_of_each_link_operation(
    client: Client, method: str, statuses: set[str]
) -> None:
    """Each link operation documents its success and its error responses."""
    schema = get_schema(client)

    assert set(schema["paths"][LINK_PATH][method]["responses"]) == statuses


@pytest.mark.parametrize("method", ["get", "delete"])
@pytest.mark.django_db
def test_link_not_found_example_matches_the_real_response(
    client: Client, account_token: str, method: str
) -> None:
    """The not-found example is the body sent to an account without a link."""
    operation = get_schema(client)["paths"][LINK_PATH][method]

    response = getattr(client, method)(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 404
    assert response.json() == only_example(operation["responses"]["404"])


@pytest.mark.django_db
def test_bot_not_configured_example_matches_the_real_response(
    client: Client, account_token: str, settings: Settings
) -> None:
    """The bot-not-configured example is the body sent without the bot's user name."""
    settings.TELEGRAM_BOT_USERNAME = ""
    operation = get_schema(client)["paths"][LINK_PATH]["post"]

    response = client.post(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 503
    assert response.json() == only_example(operation["responses"]["503"])


@pytest.mark.django_db
def test_link_request_response_example_shows_every_returned_field(
    client: Client, account_token: str, bot_username: str
) -> None:
    """The link request example has every field the API returns."""
    answer = get_schema(client)["paths"][LINK_PATH]["post"]["responses"]["201"]

    response = client.post(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 201
    assert set(only_example(answer)) == set(response.json())


@pytest.mark.django_db
def test_link_status_response_example_shows_every_returned_field(
    client: Client, account: User, account_token: str
) -> None:
    """The link status example has every field the API returns."""
    answer = get_schema(client)["paths"][LINK_PATH]["get"]["responses"]["200"]
    TelegramLink.objects.create(account=account, chat_id=123456789)

    response = client.get(
        reverse("telegram-link"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 200
    assert set(only_example(answer)) == set(response.json())
