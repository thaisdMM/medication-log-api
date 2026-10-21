"""Shared fixtures for the user account tests."""

import pytest

from users.models import User


@pytest.fixture
def existing_account(registration_data: dict[str, str]) -> User:
    """An active account created from the sign-up data."""
    return User.objects.create_user(**registration_data)


@pytest.fixture
def registration_data() -> dict[str, str]:
    """Valid sign-up data that every password validator accepts."""
    return {
        "email": "ana.ribeiro@example.com",
        "name": "Ana Ribeiro",
        "password": "Blue-Kettle-42",
    }
