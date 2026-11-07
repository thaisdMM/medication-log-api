"""Tests for how the API schema describes the account and token endpoints."""

import pytest
from django.test import Client


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
