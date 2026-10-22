"""Test for the user account endpoints."""

import pytest
from django.test import Client
from django.urls import reverse
from knox.models import AuthToken

from users.models import User


@pytest.mark.django_db
def test_registration_without_authentication_returns_only_the_id(
    client: Client, registration_data: dict[str, str]
) -> None:
    """Anonymous sign-up is accepted and answers with the new account's id only."""
    response = client.post(
        reverse("user-register"),
        registration_data,
        content_type="application/json",
    )

    assert response.status_code == 201
    assert response.json() == {"id": User.objects.get().pk}


@pytest.mark.django_db
def test_registration_with_an_invalid_token_returns_201(
    client: Client, registration_data: dict[str, str]
) -> None:
    """A stale or invalid token sent along with a sign-up is ignored."""
    response = client.post(
        reverse("user-register"),
        registration_data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Token not-a-real-token",
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_current_user_with_a_token_returns_only_id_and_name(
    client: Client, existing_account: User, account_token: str
) -> None:
    """The account behind the token answers with its id and name, never the email."""
    response = client.get(
        reverse("user-me"),
        HTTP_AUTHORIZATION=f"Token {account_token}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": existing_account.pk,
        "name": existing_account.name,
    }


@pytest.mark.django_db
def test_current_user_without_a_token_returns_401(client: Client) -> None:
    """The endpoint goes through the project's closed default."""
    response = client.get(reverse("user-me"))

    assert response.status_code == 401


@pytest.mark.django_db
def test_current_user_returns_the_account_behind_the_token(
    client: Client, existing_account: User, other_account: User, account_token: str
) -> None:
    """Each token returns its own account, never another one."""
    _, other_token = AuthToken.objects.create(user=other_account)

    ids = [
        client.get(reverse("user-me"), HTTP_AUTHORIZATION=f"Token {token}").json()["id"]
        for token in (account_token, other_token)
    ]

    assert ids == [existing_account.pk, other_account.pk]
