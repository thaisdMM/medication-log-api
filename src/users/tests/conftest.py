"""Shared fixtures for the user account tests."""

import pytest


@pytest.fixture
def registration_data() -> dict[str, str]:
    """Valid sign-up data that every password validator accepts."""
    return {
        "email": "ana.ribeiro@example.com",
        "name": "Ana Ribeiro",
        "password": "Blue-Kettle-42",
    }
