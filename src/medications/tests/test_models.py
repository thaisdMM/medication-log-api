"""Tests for the medication model and its duplicate constraint."""

from decimal import Decimal

import pytest
from django.db import IntegrityError, models, transaction
from django.db.models import ProtectedError

from medications.models import (
    ConcentrationUnit,
    Medication,
    MedicationForm,
    MedicationState,
)
from users.models import User


@pytest.mark.django_db
def test_same_medication_with_only_a_name_is_refused(owner: User) -> None:
    """A second row blank except for the same name raises IntegrityError."""
    Medication.objects.create(owner=owner, name="Dipirona")

    with pytest.raises(IntegrityError), transaction.atomic():
        Medication.objects.create(owner=owner, name="Dipirona")

    assert Medication.objects.count() == 1


@pytest.mark.django_db
def test_name_differing_only_in_case_is_refused(owner: User) -> None:
    """The same combination with the name in another case raises IntegrityError."""
    details = {
        "concentration_value": "500",
        "concentration_unit": "mg",
        "form": "tablet",
    }
    Medication.objects.create(owner=owner, name="Dipirona", **details)

    with pytest.raises(IntegrityError), transaction.atomic():
        Medication.objects.create(owner=owner, name="dipirona", **details)

    assert Medication.objects.count() == 1


@pytest.mark.django_db
def test_two_accounts_can_record_the_same_medication(
    owner: User, other_account: User
) -> None:
    """The same name is saved once for each account."""
    Medication.objects.create(owner=owner, name="Dipirona")
    Medication.objects.create(owner=other_account, name="Dipirona")

    assert Medication.objects.count() == 2


@pytest.mark.parametrize(
    "difference",
    [
        pytest.param({"concentration_value": "250"}, id="concentration_value"),
        pytest.param({"concentration_unit": "g"}, id="concentration_unit"),
        pytest.param({"form": "capsule"}, id="form"),
    ],
)
@pytest.mark.django_db
def test_same_name_with_one_different_detail_is_another_medication(
    owner: User, difference: dict[str, str]
) -> None:
    """A row that differs in one column of the combination is saved."""
    details = {
        "concentration_value": "500",
        "concentration_unit": "mg",
        "form": "tablet",
    }
    Medication.objects.create(owner=owner, name="Dipirona", **details)
    Medication.objects.create(owner=owner, name="Dipirona", **details | difference)

    assert Medication.objects.count() == 2


@pytest.mark.django_db
def test_unchosen_unit_and_form_are_stored_as_empty_text(owner: User) -> None:
    """Unit and form left out are read back from the database as empty text."""
    medication = Medication.objects.create(owner=owner, name="Dipirona")

    stored = Medication.objects.values("concentration_unit", "form").get(
        id=medication.id
    )

    assert stored == {"concentration_unit": "", "form": ""}


@pytest.mark.django_db
def test_state_not_sent_is_stored_as_in_use(owner: User) -> None:
    """A medication created without a state is read back as in use."""
    medication = Medication.objects.create(owner=owner, name="Dipirona")

    stored = Medication.objects.values_list("state", flat=True).get(id=medication.id)

    assert stored == "in_use"


@pytest.mark.django_db
def test_concentration_value_is_stored_with_three_decimal_places(owner: User) -> None:
    """A strength written in micrograms is read back without being rounded."""
    medication = Medication.objects.create(
        owner=owner, name="Levotiroxina", concentration_value="0.025"
    )

    stored = Medication.objects.values_list("concentration_value", flat=True).get(
        id=medication.id
    )

    assert stored == Decimal("0.025")


@pytest.mark.parametrize(
    ("closed_list", "expected"),
    [
        pytest.param(
            ConcentrationUnit, ["mg", "g", "ml", "other"], id="concentration_unit"
        ),
        pytest.param(
            MedicationForm,
            [
                "tablet",
                "capsule",
                "drop",
                "ml",
                "sachet",
                "patch",
                "suppository",
                "ointment",
                "other",
            ],
            id="form",
        ),
        pytest.param(MedicationState, ["in_use", "suspended"], id="state"),
    ],
)
def test_closed_list_holds_the_agreed_values(
    closed_list: type[models.TextChoices], expected: list[str]
) -> None:
    """Each closed list offers exactly the values of the domain model."""
    assert closed_list.values == expected


@pytest.mark.django_db
def test_string_representation_shows_the_class_name_with_the_id(owner: User) -> None:
    """The string form is the class name and the ID, without the medication name."""
    medication = Medication.objects.create(owner=owner, name="Dipirona")

    assert str(medication) == f"Medication (id={medication.id})"


@pytest.mark.django_db
def test_deleting_an_account_with_medications_is_refused(owner: User) -> None:
    """Deleting the owner raises ProtectedError and keeps the medication."""
    Medication.objects.create(owner=owner, name="Dipirona")

    with pytest.raises(ProtectedError):
        owner.delete()

    assert Medication.objects.filter(owner=owner).exists()
