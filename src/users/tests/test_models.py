"""Test for the user model setup, database and behavior."""

import pytest
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError, transaction

from users.models import User


@pytest.fixture
def valid_user_data() -> dict[str, str]:
    """Valid data to create a generic user."""
    return {"email": "testuser@email.com", "name": "User Name", "password": "Strong#01"}


def test_user_is_the_model_django_authenticates_with() -> None:
    """Django resolves the custom User as the authentication model."""
    assert get_user_model() is User


@pytest.mark.django_db
def test_user_table_starts_empty_in_the_test_database() -> None:
    """Database is created, migrated and starts empty."""
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_create_user_saves_to_database(valid_user_data: dict[str, str]) -> None:
    """Valid user is persisted and receives a database ID."""
    user = User.objects.create_user(**valid_user_data)

    assert user.id is not None
    assert User.objects.filter(id=user.id).exists()


@pytest.mark.django_db
def test_database_stores_correct_email(
    valid_user_data: dict[str, str],
) -> None:
    """Valid email is stored in the database."""
    user = User.objects.create_user(**valid_user_data)
    stored_user = User.objects.get(id=user.id)

    assert stored_user.email == "testuser@email.com"


@pytest.mark.django_db
def test_database_stores_correct_name(
    valid_user_data: dict[str, str],
) -> None:
    """Valid name is stored in the database."""
    user = User.objects.create_user(**valid_user_data)
    stored_user = User.objects.get(id=user.id)

    assert stored_user.name == "User Name"


@pytest.mark.django_db
def test_user_email_uniqueness_enforced_at_database_level(
    valid_user_data: dict[str, str],
) -> None:
    """Creating user with the same email raises IntegrityError."""
    User.objects.create_user(**valid_user_data)
    with pytest.raises(IntegrityError), transaction.atomic():
        User.objects.create_user(
            email="testuser@email.com", name="New User", password="Securty$pass321"
        )
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_create_user_normalizes_email(valid_user_data: dict[str, str]) -> None:
    """Email is normalized at user creation."""
    user = User.objects.create_user(
        **{**valid_user_data, "email": "NORMAlized@EMAIL.COM"}
    )

    assert user.email == "NORMAlized@email.com"


@pytest.mark.django_db
def test_empty_email_raises_value_error(valid_user_data: dict[str, str]) -> None:
    """Empty email raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        User.objects.create_user(**{**valid_user_data, "email": ""})

    assert "Email" in str(exc_info.value)


@pytest.mark.django_db
def test_empty_name_raises_value_error(valid_user_data: dict[str, str]) -> None:
    """Empty name raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        User.objects.create_user(**{**valid_user_data, "name": ""})

    assert "Name" in str(exc_info.value)


@pytest.mark.django_db
def test_empty_password_raises_value_error(valid_user_data: dict[str, str]) -> None:
    """Empty password raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        User.objects.create_user(**{**valid_user_data, "password": ""})

    assert "Password" in str(exc_info.value)


@pytest.mark.django_db
def test_create_user_hashes_password(valid_user_data: dict[str, str]) -> None:
    """Password is hashed and never stored as plain text."""
    user = User.objects.create_user(**valid_user_data)

    assert user.password != valid_user_data["password"]
    assert check_password(valid_user_data["password"], user.password)


@pytest.mark.django_db
def test_password_is_hashed_with_argon2(valid_user_data: dict[str, str]) -> None:
    """Stored hash carries the configurated algorithm prefix."""
    user = User.objects.create_user(**valid_user_data)

    assert user.password.startswith("argon2$")


@pytest.mark.django_db
def test_create_user_default_flags(valid_user_data: dict[str, str]) -> None:
    """Create user is active by default and has no staff and superuser privileges."""
    user = User.objects.create_user(**valid_user_data)

    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_superuser_saves_to_database(valid_user_data: dict[str, str]) -> None:
    """Valid superuser data is persisted and receives a database ID."""
    superuser = User.objects.create_superuser(**valid_user_data)

    assert superuser.id is not None


@pytest.mark.django_db
def test_create_superuser_has_correct_admin_flags(
    valid_user_data: dict[str, str],
) -> None:
    """Create superuser is active by default and has the staff and superuser privileges."""
    superuser = User.objects.create_superuser(**valid_user_data)
    superuser.refresh_from_db()

    assert superuser.is_active is True
    assert superuser.is_staff is True
    assert superuser.is_superuser is True


@pytest.mark.django_db
def test_str_representation(valid_user_data: dict[str, str]) -> None:
    """__str__ returns class name and id."""
    user = User.objects.create_user(**valid_user_data)

    assert str(user) == f"User (id={user.id})"


def test_user_logs_in_with_email() -> None:
    """Login identifier and extra prompts are the expected ones."""
    assert User.USERNAME_FIELD == "email"
    assert User.REQUIRED_FIELDS == ["name"]


@pytest.mark.django_db
def test_user_authenticates_with_email_and_password(
    valid_user_data: dict[str, str],
) -> None:
    """Django authenticates a user by email and password."""
    user = User.objects.create_user(**valid_user_data)

    authenticated_user = authenticate(
        email=valid_user_data["email"], password=valid_user_data["password"]
    )

    assert authenticated_user == user
