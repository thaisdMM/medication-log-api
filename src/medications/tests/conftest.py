"""Shared fixtures for the medication tests."""

from types import SimpleNamespace
from typing import Any

import pytest

from medications.models import Medication
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


@pytest.fixture
def medication_data() -> dict[str, str]:
    """Valid medication input with a concentration and a form."""
    return {
        "name": "Dipirona",
        "concentration_value": "500",
        "concentration_unit": "mg",
        "form": "tablet",
    }


@pytest.fixture
def owner_request_context(owner: User) -> dict[str, Any]:
    """Serializer context of a request made by the owner."""
    return {"request": SimpleNamespace(user=owner)}


@pytest.fixture
def existing_medication(owner: User, medication_data: dict[str, str]) -> Medication:
    """A medication the owner already recorded from the medication data."""
    return Medication.objects.create(owner=owner, **medication_data)
