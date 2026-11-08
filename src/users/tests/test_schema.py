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


def only_example(body: dict[str, Any]) -> Any:
    """Return the value of the single example of a request or response body."""
    (example,) = body["content"]["application/json"]["examples"].values()
    return example["value"]


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


@pytest.mark.django_db
def test_sign_up_request_example_creates_an_account(client: Client) -> None:
    """The sign-up data in the request example is accepted and opens an account."""
    body = get_schema(client)["paths"]["/api/users/"]["post"]["requestBody"]

    response = client.post(
        "/api/users/", only_example(body), content_type="application/json"
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_sign_up_response_example_shows_every_returned_field(
    client: Client, registration_data: dict[str, str]
) -> None:
    """The sign-up response example has every field the API returns."""
    answer = get_schema(client)["paths"]["/api/users/"]["post"]["responses"]["201"]

    response = client.post(
        "/api/users/", registration_data, content_type="application/json"
    )

    assert set(only_example(answer)) == set(response.json())


@pytest.mark.django_db
def test_login_request_example_logs_in(client: Client, existing_account: User) -> None:
    """The credentials in the login request example open a session."""
    body = get_schema(client)["paths"]["/api/auth/login/"]["post"]["requestBody"]

    response = client.post(
        "/api/auth/login/", only_example(body), content_type="application/json"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_response_example_shows_every_returned_field(
    client: Client, existing_account: User, login_data: dict[str, str]
) -> None:
    """The login response example has every field the API returns."""
    answer = get_schema(client)["paths"]["/api/auth/login/"]["post"]["responses"]["200"]

    response = client.post(
        "/api/auth/login/", login_data, content_type="application/json"
    )

    assert set(only_example(answer)) == set(response.json())


@pytest.mark.django_db
def test_current_account_example_shows_every_returned_field(
    client: Client, account_token: str
) -> None:
    """The current-account response example has every field the API returns."""
    answer = get_schema(client)["paths"]["/api/users/me/"]["get"]["responses"]["200"]

    response = client.get("/api/users/me/", HTTP_AUTHORIZATION=f"Token {account_token}")

    assert set(only_example(answer)) == set(response.json())


@pytest.mark.django_db
def test_account_deletion_request_example_deletes_the_account(
    client: Client, account_token: str
) -> None:
    """The password in the deletion request example confirms the deletion."""
    body = get_schema(client)["paths"]["/api/users/me/delete/"]["post"]["requestBody"]

    response = client.post(
        "/api/users/me/delete/",
        only_example(body),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {account_token}",
    )

    assert response.status_code == 204
