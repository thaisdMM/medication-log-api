"""The user model: a user is identified by its email address."""

from typing import ClassVar

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager["User"]):
    """Custom Manager for creating and managing User's instances."""

    use_in_migrations = True

    def create_user(
        self,
        email: str,
        name: str,
        password: str,
    ) -> User:
        """Create and save a regular user with hashed password.

        Args:
            email: User's email address (will be the login identifier)
            name: User's name
            password: Plain text password

        Returns:
            User: The created user instance

        Raises:
            ValueError: when email, name or password are not provided
        """
        if not email:
            raise ValueError("Email must be provided to create an account.")
        if not name:
            raise ValueError("Name must be provided to create an account.")
        if not password:
            raise ValueError("Password must be provided to create an account.")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, name: str, password: str) -> User:
        """Create and save a superuser (admin with all permissions).

        Args:
            email: User's email address (will be the login identifier)
            name: User's name
            password: Plain text password

        Returns:
            User: The created user instance

        Raises:
            ValueError: when email, name or password are not provided
        """
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Model representing the system User.

    Attributes:
        email: Unique email address used for authentication
        name: User's name
        is_active: User's activation status
        is_staff: Permission to access Django admin
    """

    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name=_("email address"),
        help_text=_("Email address used for login."),
    )
    name = models.CharField(max_length=255, verbose_name=_("user name"))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
        help_text=_("Designates whether this user should be treated as active."),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("staff status"),
        help_text=_("Designates whether the user can log into this Django admin site."),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["name"]

    def __str__(self) -> str:
        """String representation of the user.

        Returns:
            str: string representation with class name and database ID.
        """
        return f"{self.__class__.__name__} (id={self.id})"
