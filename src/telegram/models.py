"""The models that link an account to its conversation with the bot."""

import hashlib
import secrets
from datetime import timedelta
from typing import ClassVar

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

from users.models import User

LINK_CODE_LIFETIME = timedelta(minutes=10)
LINK_CODE_BYTES = 32


def hash_link_code(code: str) -> str:
    """Return the form in which a link code is stored and looked up.

    Args:
        code: The link code as sent in the deep link.

    Returns:
        str: The SHA-256 of the code, in hexadecimal.
    """
    return hashlib.sha256(code.encode()).hexdigest()


class TelegramLink(models.Model):
    """The conversation with the bot that an account linked to itself.

    Attributes:
        account: The account the conversation belongs to, at most one link each.
        chat_id: The conversation id Telegram assigns, linked to one account only.
        linked_at: When the link was made.
    """

    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat_id = models.BigIntegerField(unique=True)
    linked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """String representation of the link.

        Returns:
            str: String representation with class name and database ID.
        """
        return f"{self.__class__.__name__} (id={self.id})"


class TelegramLinkCodeManager(models.Manager["TelegramLinkCode"]):
    """Manager that issues the link codes of an account."""

    def issue(self, account: User) -> tuple[str, TelegramLinkCode]:
        """Create a new link code for the account and delete its earlier ones.

        Args:
            account: The account that asks to link its conversation.

        Returns:
            tuple[str, TelegramLinkCode]: The new code, made of the characters
                Telegram accepts in the start parameter, and the stored row,
                which holds only its hash.
        """
        code = secrets.token_urlsafe(LINK_CODE_BYTES)
        with transaction.atomic():
            self.filter(account=account).delete()
            link_code = self.create(
                account=account,
                code_hash=hash_link_code(code),
                expires_at=timezone.now() + LINK_CODE_LIFETIME,
            )
        return code, link_code


class TelegramLinkCode(models.Model):
    """A one-time code that links an account to a conversation with the bot.

    Attributes:
        account: The account that asked for the code.
        code_hash: The SHA-256 of the code; the code itself is never stored.
        expires_at: When the code stops being accepted.
    """

    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code_hash = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()

    objects: ClassVar[TelegramLinkCodeManager] = TelegramLinkCodeManager()

    def __str__(self) -> str:
        """String representation of the link code.

        Returns:
            str: String representation with class name and database ID.
        """
        return f"{self.__class__.__name__} (id={self.id})"
