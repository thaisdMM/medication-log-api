"""Tests for how the API schema treats the Telegram bot endpoints."""

from django.test import Client


def test_schema_leaves_out_the_webhook(client: Client) -> None:
    """The webhook is called by Telegram only, so the schema does not list it."""
    response = client.get("/api/schema/?format=json")

    assert response.status_code == 200
    assert "/api/telegram/webhook/" not in response.json()["paths"]
