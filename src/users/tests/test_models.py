"""Test for the user moddel setup and database."""

import pytest
from django.contrib.auth import get_user_model

from users.models import User


def test_user_is_the_model_django_authenticates_with() -> None:
    """Django resolves the custom User as the authentication model."""
    assert get_user_model() is User


@pytest.mark.django_db
def test_user_table_starts_empty_in_the_test_database() -> None:
    """Database is created, migrated and starts empty."""
    assert User.objects.count() == 0
