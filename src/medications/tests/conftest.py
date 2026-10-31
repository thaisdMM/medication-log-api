"""Shared fixtures for the medication tests."""

import pytest

from users.models import User


@pytest.fixture
def owner() -> User:
    """The account that records the medications."""
    return User.objects.create_user(
        email="ana.ribeiro@example.com",
        name="Ana Ribeiro",
        password="Blue-Kettle-42",
    )


@pytest.fixture
def other_account() -> User:
    """A second account, unrelated to the owner."""
    return User.objects.create_user(
        email="bruno.costa@example.com",
        name="Bruno Costa",
        password="Green-Lantern-17",
    )
