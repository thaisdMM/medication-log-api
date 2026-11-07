"""Tests for the interactive API documentation."""

import pytest
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


def test_schema_lists_the_account_and_token_endpoints(client: Client) -> None:
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


@pytest.mark.parametrize("path", ["/api/auth/logout/", "/api/auth/logoutall/"])
def test_schema_describes_logout_as_answering_with_no_content(
    client: Client, path: str
) -> None:
    """The schema documents a logout as a 204 response with no body."""
    response = client.get("/api/schema/?format=json")

    responses = response.json()["paths"][path]["post"]["responses"]
    assert "content" not in responses["204"]


def test_schema_gives_every_operation_its_own_summary(client: Client) -> None:
    """Every operation in the schema has a summary, and no two share one."""
    response = client.get("/api/schema/?format=json")

    summaries = [
        operation.get("summary")
        for path_item in response.json()["paths"].values()
        for operation in path_item.values()
    ]
    assert summaries
    assert None not in summaries
    assert len(set(summaries)) == len(summaries)
