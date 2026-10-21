"""Tests for the token authentication endpoints."""

from datetime import datetime, timedelta

import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from users.models import User
from users.serializers import INVALID_CREDENTIALS_MESSAGE


class ProtectedView(APIView):
    """Stands in for any endpoint behind the project's closed default."""

    def get(self, request: Request) -> Response:
        """Return the id of the authenticated account.

        Args:
            request: The incoming API request.

        Returns:
            Response: 200 with the account id.
        """
        return Response({"id": request.user.pk})


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
def test_login_token_authenticates_a_protected_view(
    client: Client, existing_account: User, login_data: dict[str, str]
) -> None:
    """The token from the login is accepted by an endpoint that needs one."""
    token = client.post(
        reverse("auth-login"),
        login_data,
        content_type="application/json",
    ).json()["token"]
    request = APIRequestFactory().get("/", HTTP_AUTHORIZATION=f"Token {token}")

    response = ProtectedView.as_view()(request)

    assert response.status_code == 200
    assert response.data == {"id": existing_account.pk}


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
