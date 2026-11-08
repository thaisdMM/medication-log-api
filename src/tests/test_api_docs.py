"""Tests for the interactive API documentation."""

from typing import Any

import pytest
from django.test import Client

FIELD_ERRORS = {
    "type": "object",
    "additionalProperties": {"type": "array", "items": {"type": "string"}},
}


def get_schema(client: Client) -> dict[str, Any]:
    """Return the schema served to the Swagger UI page."""
    response = client.get("/api/schema/?format=json")
    assert response.status_code == 200
    schema: dict[str, Any] = response.json()
    return schema


def error_responses(schema: dict[str, Any]) -> dict[tuple[str, str, str], Any]:
    """Map each error response of the schema to its path, method and status."""
    return {
        (path, method, status): answer
        for path, path_item in schema["paths"].items()
        for method, operation in path_item.items()
        for status, answer in operation["responses"].items()
        if status.startswith("4")
    }


def named_example(answer: dict[str, Any], summary: str) -> Any:
    """Return the value of the example shown with this name in a response."""
    examples = answer["content"]["application/json"]["examples"]
    return next(
        example["value"]
        for example in examples.values()
        if example.get("summary") == summary
    )


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


def test_schema_gives_every_error_response_an_example(client: Client) -> None:
    """Every error response in the schema shows at least one example body."""
    answers = error_responses(get_schema(client))

    assert answers
    assert [
        key
        for key, answer in answers.items()
        if not answer["content"]["application/json"].get("examples")
    ] == []


def test_schema_describes_invalid_input_as_messages_by_field(client: Client) -> None:
    """Every invalid-input response maps each field to a list of messages."""
    answers = error_responses(get_schema(client))

    invalid_inputs = {key: a for key, a in answers.items() if key[2] == "400"}
    assert invalid_inputs
    assert [
        key
        for key, answer in invalid_inputs.items()
        if answer["content"]["application/json"]["schema"] != FIELD_ERRORS
    ] == []


def test_no_token_example_matches_the_real_response(client: Client) -> None:
    """The "No token" example is the body sent back when no token is given."""
    answer = get_schema(client)["paths"]["/api/users/me/"]["get"]["responses"]["401"]

    response = client.get("/api/users/me/")

    assert response.status_code == 401
    assert response.json() == named_example(answer, "No token")


@pytest.mark.django_db
def test_invalid_token_example_matches_the_real_response(client: Client) -> None:
    """The "Invalid or expired token" example is the body sent for a bad token."""
    answer = get_schema(client)["paths"]["/api/users/me/"]["get"]["responses"]["401"]

    response = client.get("/api/users/me/", HTTP_AUTHORIZATION="Token not-a-token")

    assert response.status_code == 401
    assert response.json() == named_example(answer, "Invalid or expired token")
