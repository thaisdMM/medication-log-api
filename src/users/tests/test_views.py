"""Test for the user account endpoints."""

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_registration_without_authentication_returns_201(
    client: Client, registration_data: dict[str, str]
) -> None:
    """Anonymous sign-up is accepted, despite the project's closed default."""
    response = client.post(
        reverse("user-register"),
        registration_data,
        content_type="application/json",
    )

    assert response.status_code == 201
