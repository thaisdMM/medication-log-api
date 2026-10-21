"""Serializers for the user account."""

from typing import Any

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from rest_framework import serializers

from users.models import User

DUPLICATE_EMAIL_MESSAGE = "A user with this email address already exists."


class UserRegistrationSerializer(serializers.ModelSerializer[User]):
    """Validate sign-up data and create the account through the user manager.

    Attributes:
        email: Login identifier, with the domain normalized before the
            uniqueness check
        password: Plain text password, accepted on input and never returned
    """

    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("id", "email", "name", "password")

    def validate_email(self, value: str) -> str:
        """Normalize the email domain and refuse an address already in use.

        Args:
            value: Email address as sent, already trimmed and format-checked

        Returns:
            str: The email address with its domain in lowercase

        Raises:
            ValidationError: when an account with this email address exists
        """
        email = User.objects.normalize_email(value)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(DUPLICATE_EMAIL_MESSAGE)
        return email

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Run the project's password validators against the new account.

        Args:
            attrs: Field values that passed field-level validation

        Returns:
            dict[str, Any]: The same field values, unchanged

        Raises:
            ValidationError: when a password validator rejects the password
        """
        user = User(email=attrs["email"], name=attrs["name"])
        try:
            password_validation.validate_password(attrs["password"], user=user)
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                {"password": list(error.messages)}
            ) from error
        return attrs

    def create(self, validated_data: dict[str, Any]) -> User:
        """Create the account with a hashed password.

        The email check in validate_email cannot see an account saved by a
        concurrent sign-up, so the database's unique constraint is caught here
        and reported as the same duplicate email error.

        Args:
            validated_data: Email, name and password that passed validation

        Returns:
            User: The created user instance

        Raises:
            ValidationError: when the email was taken after validation
        """
        try:
            with transaction.atomic():
                return User.objects.create_user(
                    email=validated_data["email"],
                    name=validated_data["name"],
                    password=validated_data["password"],
                )
        except IntegrityError as error:
            raise serializers.ValidationError(
                {"email": [DUPLICATE_EMAIL_MESSAGE]}
            ) from error
