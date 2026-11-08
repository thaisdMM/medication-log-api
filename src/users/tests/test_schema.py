"""Tests for how the API schema describes the account and token endpoints."""

from collections.abc import Callable
from typing import Any

import pytest
from django.test import Client

from users.models import User


def get_schema(client: Client) -> dict[str, Any]:
    """Return the schema served to the Swagger UI page."""
    response = client.get("/api/schema/?format=json")
    assert response.status_code == 200
    schema: dict[str, Any] = response.json()
    return schema


def named_example(answer: dict[str, Any], name: str) -> Any:
    """Return the value of the example shown with this name in a response."""
    examples = answer["content"]["application/json"]["examples"]
    return next(
        example["value"]
        for key, example in examples.items()
        if example.get("summary", key) == name
    )


@pytest.mark.parametrize(
    ("path", "method", "statuses"),
    [
        ("/api/users/", "post", {"201", "400"}),
        ("/api/auth/login/", "post", {"200", "400"}),
        ("/api/users/me/", "get", {"200", "401"}),
        ("/api/auth/logout/", "post", {"204", "401"}),
        ("/api/auth/logoutall/", "post", {"204", "401"}),
        ("/api/users/me/delete/", "post", {"204", "400", "401"}),
    ],
)
def test_schema_lists_the_responses_of_each_account_operation(
    client: Client, path: str, method: str, statuses: set[str]
) -> None:
    """Each account and token operation documents its success and its errors."""
    response = client.get("/api/schema/?format=json")

    operation = response.json()["paths"][path][method]
    assert set(operation["responses"]) == statuses


WRONG_PASSWORD = "Wrong-Kettle-00"


@pytest.mark.parametrize(
    ("path", "name", "build_body"),
    [
        pytest.param(
            "/api/users/", "Refused field", lambda data: {}, id="sign-up-empty"
        ),
        pytest.param(
            "/api/users/", "Email in use", lambda data: data, id="sign-up-email-in-use"
        ),
        pytest.param(
            "/api/auth/login/", "Refused field", lambda data: {}, id="login-empty"
        ),
        pytest.param(
            "/api/auth/login/",
            "Wrong credentials",
            lambda data: {**data, "password": WRONG_PASSWORD},
            id="login-wrong-password",
        ),
        pytest.param(
            "/api/users/me/delete/",
            "Missing password",
            lambda data: {},
            id="deletion-empty",
        ),
        pytest.param(
            "/api/users/me/delete/",
            "Wrong password",
            lambda data: {"password": WRONG_PASSWORD},
            id="deletion-wrong-password",
        ),
    ],
)
@pytest.mark.django_db
def test_invalid_input_example_matches_the_real_response(
    client: Client,
    registration_data: dict[str, str],
    existing_account: User,
    account_token: str,
    path: str,
    name: str,
    build_body: Callable[[dict[str, str]], dict[str, str]],
) -> None:
    """Each invalid-input example is the body sent back for that refusal."""
    answer = get_schema(client)["paths"][path]["post"]["responses"]["400"]

    response = client.post(
        path,
        build_body(registration_data),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {account_token}",
    )

    assert response.status_code == 400
    assert response.json() == named_example(answer, name)
