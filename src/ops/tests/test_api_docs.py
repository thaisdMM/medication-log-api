"""Tests for the interactive API documentation."""

from django.test import Client


def test_swagger_ui_page_opens_without_a_token(client: Client) -> None:
    """The documentation page is public, overriding the closed default."""
    response = client.get("/api/docs/")

    assert response.status_code == 200
    assert "text/html" in response["Content-Type"]


def test_schema_opens_without_a_token(client: Client) -> None:
    """The schema the page reads is public, overriding the closed default."""
    response = client.get("/api/schema/")

    assert response.status_code == 200


def test_schema_lists_every_slice_1_endpoint(client: Client) -> None:
    """The schema describes the account and token endpoints, not only the docs."""
    response = client.get("/api/schema/?format=json")

    assert response.status_code == 200
    assert set(response.json()["paths"]) >= {
        "/api/users/",
        "/api/users/me/",
        "/api/auth/login/",
        "/api/auth/logout/",
        "/api/auth/logoutall/",
    }
