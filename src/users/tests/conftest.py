"""Shared fixtures for the user account tests."""

import pytest
from knox.models import AuthToken

from users.models import User


@pytest.fixture
def registration_data() -> dict[str, str]:
    """Valid sign-up data that every password validator accepts."""
    return {
        "email": "ana.ribeiro@example.com",
        "name": "Ana Ribeiro",
        "password": "Blue-Kettle-42",
    }


@pytest.fixture
def login_data(registration_data: dict[str, str]) -> dict[str, str]:
    """Credentials of the account created from the sign-up data."""
    return {
        "email": registration_data["email"],
        "password": registration_data["password"],
    }


@pytest.fixture
def existing_account(registration_data: dict[str, str]) -> User:
    """An active account created from the sign-up data."""
    return User.objects.create_user(**registration_data)


@pytest.fixture
def other_account() -> User:
    """A second active account, unrelated to the sign-up data."""
    return User.objects.create_user(
        email="bruno.costa@example.com",
        name="Bruno Costa",
        password="Green-Lantern-17",
    )


@pytest.fixture
def account_token(existing_account: User) -> str:
    """A valid token for the existing account, created directly through knox."""
    _, token = AuthToken.objects.create(user=existing_account)
    return str(token)
