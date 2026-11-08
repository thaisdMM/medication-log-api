"""Serializers for the user account."""

from typing import Any

from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from users.models import User

DUPLICATE_EMAIL_MESSAGE = "A user with this email address already exists."
INVALID_CREDENTIALS_MESSAGE = "Unable to log in with the provided credentials."
WRONG_PASSWORD_MESSAGE = "The password is incorrect."

ACCOUNT_EXAMPLE = {
    "email": "ana.ribeiro@example.com",
    "name": "Ana Ribeiro",
    "password": "Blue-Kettle-42",
}


@extend_schema_serializer(
    examples=[
        OpenApiExample("Account", value=ACCOUNT_EXAMPLE, request_only=True),
        OpenApiExample("Account", value={"id": 1}, response_only=True),
    ]
)
class UserRegistrationSerializer(serializers.ModelSerializer[User]):
    """Validate sign-up data and create the account through the user manager.

    Only the id is returned: email and name are accepted on input and never
    echoed back, so a response carries no personal data it does not need.

    Attributes:
        email: Login identifier, stored in lowercase and checked for
            uniqueness in that form.
        name: Account holder's name, accepted on input and never returned.
        password: Plain text password, accepted on input and never returned.
    """

    email = serializers.EmailField(max_length=255, write_only=True)
    name = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("id", "email", "name", "password")

    def validate_email(self, value: str) -> str:
        """Lowercase the email and refuse an address already in use.

        Args:
            value: Email address as sent, already trimmed and format-checked.

        Returns:
            str: The whole email address in lowercase, as the manager stores it.

        Raises:
            ValidationError: When an account with this email address exists.
        """
        email = User.objects.canonical_email(value)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(DUPLICATE_EMAIL_MESSAGE)
        return email

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Run the project's password validators against the new account.

        Args:
            attrs: Field values that passed field-level validation.

        Returns:
            dict[str, Any]: The same field values, unchanged.

        Raises:
            ValidationError: When a password validator rejects the password.
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
            validated_data: Email, name and password that passed validation.

        Returns:
            User: The created user instance.

        Raises:
            ValidationError: When the email was taken after validation.
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


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Account",
            value={"id": 1, "name": ACCOUNT_EXAMPLE["name"]},
            response_only=True,
        ),
    ]
)
class CurrentUserSerializer(serializers.ModelSerializer[User]):
    """Represent the account behind the token.

    Attributes:
        id: Account identifier.
        name: Account holder's name.
    """

    class Meta:
        model = User
        fields = ("id", "name")
        read_only_fields = fields


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Credentials",
            value={
                "email": ACCOUNT_EXAMPLE["email"],
                "password": ACCOUNT_EXAMPLE["password"],
            },
            request_only=True,
        ),
    ]
)
class LoginSerializer(serializers.Serializer[User]):
    """Check an email and password pair and resolve the account behind it.

    Attributes:
        email: Login identifier, compared in its canonical form.
        password: Plain text password, accepted on input and never returned.
    """

    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Authenticate the credentials and add the account to the data.

        Unknown email, wrong password and inactive account all fail with the
        same message, so a login attempt cannot tell which accounts exist.

        Args:
            attrs: Email and password that passed field-level validation.

        Returns:
            dict[str, Any]: The same field values, plus the account as "user".

        Raises:
            ValidationError: When the credentials do not match an active account.
        """
        user = authenticate(
            self.context.get("request"),
            email=User.objects.canonical_email(attrs["email"]),
            password=attrs["password"],
        )
        if user is None:
            raise serializers.ValidationError(INVALID_CREDENTIALS_MESSAGE)
        return {**attrs, "user": user}


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Token",
            value={
                "expiry": "2026-11-08T22:15:30.123456Z",
                "token": "3f9a1c7e5b2d8f4a6c0e9b1d7f3a5c8e2b4d6f0a9c1e3b5d7f9a2c4e6b8d0f1a",
            },
            response_only=True,
        ),
    ]
)
class LoginResponseSerializer(serializers.Serializer[Any]):
    """Describe the body of a successful login, for the API schema only.

    The body itself is built by knox; this class is never used to validate or
    produce a response.

    Attributes:
        token: The token to send in the Authorization header.
        expiry: When the token stops working.
    """

    token = serializers.CharField()
    expiry = serializers.DateTimeField()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Password",
            value={"password": ACCOUNT_EXAMPLE["password"]},
            request_only=True,
        ),
    ]
)
class AccountDeletionSerializer(serializers.Serializer[User]):
    """Check the password of the account behind the token before it is deleted.

    Attributes:
        password: Plain text password, accepted on input and never returned.
    """

    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate_password(self, value: str) -> str:
        """Refuse a password that does not match the account behind the token.

        Args:
            value: Password as sent.

        Returns:
            str: The same password, unchanged.

        Raises:
            ValidationError: When the password does not match the account.
        """
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError(WRONG_PASSWORD_MESSAGE)
        return value
