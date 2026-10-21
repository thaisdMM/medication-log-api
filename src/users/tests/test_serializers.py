"""Tests for the user registration serializer."""

import pytest
from rest_framework.exceptions import ValidationError

from users.models import User
from users.serializers import DUPLICATE_EMAIL_MESSAGE, UserRegistrationSerializer


@pytest.mark.django_db
def test_password_is_saved_hashed(registration_data: dict[str, str]) -> None:
    """Saved password is a hash that matches the one sent."""
    serializer = UserRegistrationSerializer(data=registration_data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    user.refresh_from_db()

    assert user.check_password("Blue-Kettle-42")


def test_output_holds_only_the_id() -> None:
    """Serialized output holds the id, and no password, email or name."""
    user = User(id=1, email="ana.ribeiro@example.com", name="Ana Ribeiro")
    user.set_password("Blue-Kettle-42")

    serializer = UserRegistrationSerializer(instance=user)

    assert serializer.data == {"id": 1}


@pytest.mark.django_db
def test_duplicate_email_with_uppercase_domain_is_rejected(
    registration_data: dict[str, str],
) -> None:
    """Same address with the domain in uppercase is a duplicate, not a crash."""
    User.objects.create_user(
        email="ana.ribeiro@example.com", name="Other Name", password="Other-Pass-77"
    )
    serializer = UserRegistrationSerializer(
        data={**registration_data, "email": "ana.ribeiro@EXAMPLE.COM"}
    )

    assert not serializer.is_valid()
    assert serializer.errors["email"] == [
        "A user with this email address already exists."
    ]


@pytest.mark.django_db
def test_duplicate_email_with_uppercase_local_part_is_rejected(
    registration_data: dict[str, str],
) -> None:
    """Same address with the local part in uppercase is a duplicate."""
    User.objects.create_user(
        email="ana.ribeiro@example.com", name="Other Name", password="Other-Pass-77"
    )
    serializer = UserRegistrationSerializer(
        data={**registration_data, "email": "ANA.RIBEIRO@example.com"}
    )

    assert not serializer.is_valid()
    assert serializer.errors["email"] == [DUPLICATE_EMAIL_MESSAGE]


@pytest.mark.django_db
def test_password_similar_to_name_is_rejected(
    registration_data: dict[str, str],
) -> None:
    """A password close to the name is rejected."""
    serializer = UserRegistrationSerializer(
        data={
            **registration_data,
            "email": "kettle@example.com",
            "password": "anaribeiro1",
        }
    )

    assert not serializer.is_valid()
    assert (
        "The password is too similar to the user name." in serializer.errors["password"]
    )


@pytest.mark.django_db
def test_password_similar_to_email_is_rejected(
    registration_data: dict[str, str],
) -> None:
    """A password close to the email address is rejected."""
    serializer = UserRegistrationSerializer(
        data={
            **registration_data,
            "email": "kettlebell@example.com",
            "password": "kettlebell99",
        }
    )

    assert not serializer.is_valid()
    assert (
        "The password is too similar to the email address."
        in serializer.errors["password"]
    )


@pytest.mark.django_db
def test_email_taken_after_validation_is_rejected_on_create(
    registration_data: dict[str, str],
) -> None:
    """An email saved between validation and create is a 400, not a crash."""
    User.objects.create_user(
        email="ana.ribeiro@example.com", name="Other Name", password="Other-Pass-77"
    )

    with pytest.raises(ValidationError) as error:
        UserRegistrationSerializer().create(registration_data)

    assert error.value.detail == {"email": [DUPLICATE_EMAIL_MESSAGE]}
    assert User.objects.count() == 1
