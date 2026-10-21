"""Test for the user account endpoints."""

import pytest
from django.test import Client
from django.urls import reverse

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
