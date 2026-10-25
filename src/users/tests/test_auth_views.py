"""Tests for the token authentication endpoints."""

from datetime import datetime, timedelta

import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from knox.models import AuthToken

from users.models import User
from users.serializers import INVALID_CREDENTIALS_MESSAGE


@pytest.mark.django_db
def test_login_returns_only_expiry_and_token(
    client: Client, existing_account: User, login_data: dict[str, str]
) -> None:
    """A valid login answers with the token and its expiry, and no account data."""
    response = client.post(
        reverse("auth-login"),
        login_data,
        content_type="application/json",
    )

    assert response.status_code == 200
    assert set(response.json()) == {"expiry", "token"}


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("email", "password", "is_active"),
    [
        ("nobody@example.com", "Blue-Kettle-42", True),
        ("ana.ribeiro@example.com", "Wrong-Kettle-42", True),
        ("ana.ribeiro@example.com", "Blue-Kettle-42", False),
    ],
    ids=["unknown-email", "wrong-password", "inactive-account"],
)
def test_failed_login_gives_the_same_answer(
    client: Client,
    existing_account: User,
    email: str,
    password: str,
    is_active: bool,
) -> None:
    """Every failed login gets one generic 400, so accounts cannot be enumerated."""
    existing_account.is_active = is_active
    existing_account.save()

    response = client.post(
        reverse("auth-login"),
        {"email": email, "password": password},
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json() == {"non_field_errors": [INVALID_CREDENTIALS_MESSAGE]}


@pytest.mark.django_db
def test_login_with_email_in_mixed_case_succeeds(
    client: Client, existing_account: User, login_data: dict[str, str]
) -> None:
    """The email is compared in its canonical form, whatever the case typed."""
    response = client.post(
        reverse("auth-login"),
        {**login_data, "email": "Ana.Ribeiro@Example.com"},
        content_type="application/json",
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_token_reaches_the_current_user_endpoint(
    client: Client, existing_account: User, login_data: dict[str, str]
) -> None:
    """The token from the login authenticates the account that logged in."""
    token = client.post(
        reverse("auth-login"),
        login_data,
        content_type="application/json",
    ).json()["token"]

    response = client.get(reverse("user-me"), HTTP_AUTHORIZATION=f"Token {token}")

    assert response.status_code == 200
    assert response.json()["id"] == existing_account.pk


@pytest.mark.django_db
def test_login_token_expires_ten_hours_after_login(
    client: Client, existing_account: User, login_data: dict[str, str]
) -> None:
    """The token lifetime is 10 hours from the login."""
    before = timezone.now()
    response = client.post(
        reverse("auth-login"),
        login_data,
        content_type="application/json",
    )
    after = timezone.now()

    expiry = datetime.fromisoformat(response.json()["expiry"])

    assert before + timedelta(hours=10) <= expiry <= after + timedelta(hours=10)


@pytest.mark.django_db
def test_expired_token_is_rejected(client: Client, account_token: str) -> None:
    """A token whose expiry has passed gets 401 on the current user endpoint."""
    AuthToken.objects.update(expiry=timezone.now() - timedelta(seconds=1))

    response = client.get(
        reverse("user-me"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_using_a_token_does_not_move_its_expiry(
    client: Client, account_token: str
) -> None:
    """Using a token leaves its expiry where it was."""
    expiry = timezone.now() + timedelta(hours=1)
    AuthToken.objects.update(expiry=expiry)

    response = client.get(
        reverse("user-me"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert response.status_code == 200
    assert AuthToken.objects.get().expiry == expiry


@pytest.mark.django_db
def test_logout_makes_the_token_used_stop_working(
    client: Client, account_token: str
) -> None:
    """After a logout, the token it was called with is refused."""
    logout = client.post(
        reverse("auth-logout"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    response = client.get(
        reverse("user-me"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    assert logout.status_code == 204
    assert response.status_code == 401


@pytest.mark.django_db
def test_logout_keeps_the_other_tokens_of_the_account_working(
    client: Client, account_token: str, second_account_token: str
) -> None:
    """A logout ends only the token it was called with."""
    logout = client.post(
        reverse("auth-logout"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    response = client.get(
        reverse("user-me"), HTTP_AUTHORIZATION=f"Token {second_account_token}"
    )

    assert logout.status_code == 204
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_all_makes_every_token_of_the_account_stop_working(
    client: Client, account_token: str, second_account_token: str
) -> None:
    """After a logout-all, no token of the account is accepted."""
    logout = client.post(
        reverse("auth-logoutall"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    responses = [
        client.get(reverse("user-me"), HTTP_AUTHORIZATION=f"Token {token}")
        for token in (account_token, second_account_token)
    ]

    assert logout.status_code == 204
    assert [response.status_code for response in responses] == [401, 401]


@pytest.mark.django_db
def test_logout_all_keeps_the_tokens_of_other_accounts_working(
    client: Client, account_token: str, other_account: User
) -> None:
    """A logout-all ends only the tokens of the account that called it."""
    _, other_token = AuthToken.objects.create(user=other_account)
    logout = client.post(
        reverse("auth-logoutall"), HTTP_AUTHORIZATION=f"Token {account_token}"
    )

    response = client.get(reverse("user-me"), HTTP_AUTHORIZATION=f"Token {other_token}")

    assert logout.status_code == 204
    assert response.status_code == 200
