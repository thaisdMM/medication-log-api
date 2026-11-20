"""Tests for the Telegram link and the link code."""

import hashlib
import re

import pytest
from django.db import IntegrityError, transaction
from django.utils import timezone

from telegram.models import LINK_CODE_LIFETIME, TelegramLink, TelegramLinkCode
from users.models import User

CHAT_ID = 123456789
OTHER_CHAT_ID = 987654321
TELEGRAM_START_PARAMETER = re.compile(r"[A-Za-z0-9_-]{1,64}")


@pytest.mark.django_db
def test_a_chat_is_linked_to_one_account_only(
    account: User, other_account: User
) -> None:
    """A second link with a chat id already in use raises IntegrityError."""
    TelegramLink.objects.create(account=account, chat_id=CHAT_ID)

    with pytest.raises(IntegrityError), transaction.atomic():
        TelegramLink.objects.create(account=other_account, chat_id=CHAT_ID)

    assert TelegramLink.objects.count() == 1


@pytest.mark.django_db
def test_an_account_has_one_link_only(account: User) -> None:
    """A second link for the same account raises IntegrityError."""
    TelegramLink.objects.create(account=account, chat_id=CHAT_ID)

    with pytest.raises(IntegrityError), transaction.atomic():
        TelegramLink.objects.create(account=account, chat_id=OTHER_CHAT_ID)

    assert TelegramLink.objects.count() == 1


@pytest.mark.django_db
def test_deleting_the_account_deletes_its_link(account: User) -> None:
    """The account's link goes with the account."""
    TelegramLink.objects.create(account=account, chat_id=CHAT_ID)

    account.delete()

    assert not TelegramLink.objects.exists()


@pytest.mark.django_db
def test_deleting_the_account_deletes_its_link_codes(account: User) -> None:
    """The account's link codes go with the account."""
    TelegramLinkCode.objects.issue(account)

    account.delete()

    assert not TelegramLinkCode.objects.exists()


@pytest.mark.django_db
def test_issued_code_uses_only_the_characters_telegram_accepts(account: User) -> None:
    """The code fits the start parameter: letters, digits, _ and -, up to 64."""
    code, _ = TelegramLinkCode.objects.issue(account)

    assert TELEGRAM_START_PARAMETER.fullmatch(code)


@pytest.mark.django_db
def test_issued_code_is_stored_only_as_its_hash(account: User) -> None:
    """The database keeps the SHA-256 of the code, never the code itself."""
    code, _ = TelegramLinkCode.objects.issue(account)

    stored = TelegramLinkCode.objects.get(account=account)

    assert stored.code_hash == hashlib.sha256(code.encode()).hexdigest()


@pytest.mark.django_db
def test_issued_code_comes_with_the_row_stored_for_it(account: User) -> None:
    """Issuing returns, next to the code, the stored row that holds its hash."""
    code, link_code = TelegramLinkCode.objects.issue(account)

    assert link_code == TelegramLinkCode.objects.get(
        code_hash=hashlib.sha256(code.encode()).hexdigest()
    )


@pytest.mark.django_db
def test_issued_code_expires_after_the_link_code_lifetime(account: User) -> None:
    """The code is valid from the moment it is issued until its lifetime ends."""
    before = timezone.now()

    TelegramLinkCode.objects.issue(account)

    stored = TelegramLinkCode.objects.get(account=account)
    assert (
        before + LINK_CODE_LIFETIME
        <= stored.expires_at
        <= timezone.now() + LINK_CODE_LIFETIME
    )


@pytest.mark.django_db
def test_issuing_a_code_cancels_the_account_earlier_codes(account: User) -> None:
    """Only the newest code of the account stays in the database."""
    TelegramLinkCode.objects.issue(account)

    newest, _ = TelegramLinkCode.objects.issue(account)

    assert list(TelegramLinkCode.objects.values_list("code_hash", flat=True)) == [
        hashlib.sha256(newest.encode()).hexdigest()
    ]


@pytest.mark.django_db
def test_issuing_a_code_keeps_the_codes_of_other_accounts(
    account: User, other_account: User
) -> None:
    """A new code for one account leaves another account's code in place."""
    TelegramLinkCode.objects.issue(other_account)

    TelegramLinkCode.objects.issue(account)

    assert TelegramLinkCode.objects.filter(account=other_account).count() == 1


@pytest.mark.django_db
def test_link_string_representation_shows_the_class_name_with_the_id(
    account: User,
) -> None:
    """The link's string form is the class name and the ID, without the chat id."""
    link = TelegramLink.objects.create(account=account, chat_id=CHAT_ID)

    assert str(link) == f"TelegramLink (id={link.id})"


@pytest.mark.django_db
def test_link_code_string_representation_shows_the_class_name_with_the_id(
    account: User,
) -> None:
    """The code's string form is the class name and the ID, without the hash."""
    TelegramLinkCode.objects.issue(account)
    code = TelegramLinkCode.objects.get(account=account)

    assert str(code) == f"TelegramLinkCode (id={code.id})"
