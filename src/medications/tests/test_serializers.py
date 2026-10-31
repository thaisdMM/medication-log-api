"""Tests for the medication serializer."""

from decimal import Decimal
from typing import Any

import pytest
from rest_framework.exceptions import ValidationError

from medications.models import DUPLICATE_MEDICATION_MESSAGE, Medication
from medications.serializers import MedicationSerializer
from users.models import User


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("0", id="zero"),
        pytest.param("-1", id="negative"),
        pytest.param("1.2345", id="more_than_three_decimal_places"),
    ],
)
@pytest.mark.django_db
def test_invalid_concentration_value_is_refused(
    medication_data: dict[str, str], owner_request_context: dict[str, Any], value: str
) -> None:
    """A value that is not positive with at most three decimals is an error."""
    serializer = MedicationSerializer(
        data={**medication_data, "concentration_value": value},
        context=owner_request_context,
    )

    assert not serializer.is_valid()
    assert "concentration_value" in serializer.errors


@pytest.mark.django_db
def test_smallest_concentration_value_is_accepted(
    medication_data: dict[str, str], owner_request_context: dict[str, Any]
) -> None:
    """The smallest value with three decimal places passes validation."""
    serializer = MedicationSerializer(
        data={**medication_data, "concentration_value": "0.001"},
        context=owner_request_context,
    )

    assert serializer.is_valid(), serializer.errors


@pytest.mark.parametrize(
    ("stored", "returned"),
    [
        pytest.param("25.000", "25", id="whole_number"),
        pytest.param("100.000", "100", id="whole_number_ending_in_zeros"),
        pytest.param("0.025", "0.025", id="three_decimal_places"),
        pytest.param("2.500", "2.5", id="trailing_zero_after_a_decimal"),
    ],
)
def test_concentration_value_is_returned_without_trailing_zeros(
    stored: str, returned: str
) -> None:
    """The output writes the value with no trailing zeros and no exponent."""
    medication = Medication(name="Dipirona", concentration_value=Decimal(stored))

    serializer = MedicationSerializer(instance=medication)

    assert serializer.data["concentration_value"] == returned


@pytest.mark.django_db
def test_owner_is_the_requester_even_when_another_is_sent(
    medication_data: dict[str, str],
    owner: User,
    other_account: User,
    owner_request_context: dict[str, Any],
) -> None:
    """An owner in the input is ignored and the requester owns the medication."""
    serializer = MedicationSerializer(
        data={**medication_data, "owner": other_account.id},
        context=owner_request_context,
    )

    assert serializer.is_valid(), serializer.errors
    assert serializer.save().owner == owner


@pytest.mark.django_db
def test_output_holds_the_medication_fields_without_the_owner(
    existing_medication: Medication,
) -> None:
    """Serialized output holds the medication's own fields and no owner."""
    serializer = MedicationSerializer(instance=existing_medication)

    assert serializer.data == {
        "id": existing_medication.id,
        "name": "Dipirona",
        "concentration_value": "500",
        "concentration_unit": "mg",
        "form": "tablet",
        "state": "in_use",
    }


@pytest.mark.django_db
def test_duplicate_is_refused_with_the_fixed_message(
    medication_data: dict[str, str],
    existing_medication: Medication,
    owner_request_context: dict[str, Any],
) -> None:
    """The same combination is an error outside any field, with no existing id."""
    serializer = MedicationSerializer(
        data=medication_data, context=owner_request_context
    )

    assert not serializer.is_valid()
    assert serializer.errors == {"non_field_errors": [DUPLICATE_MEDICATION_MESSAGE]}


@pytest.mark.django_db
def test_duplicate_with_the_name_in_another_case_is_refused(
    medication_data: dict[str, str],
    existing_medication: Medication,
    owner_request_context: dict[str, Any],
) -> None:
    """The same combination with the name in another case is a duplicate."""
    serializer = MedicationSerializer(
        data={**medication_data, "name": "DIPIRONA"}, context=owner_request_context
    )

    assert not serializer.is_valid()
    assert serializer.errors == {"non_field_errors": [DUPLICATE_MEDICATION_MESSAGE]}


@pytest.mark.django_db
def test_duplicate_with_only_a_name_is_refused(
    owner: User, owner_request_context: dict[str, Any]
) -> None:
    """A second medication blank except for the same name is a duplicate."""
    Medication.objects.create(owner=owner, name="Dipirona")
    serializer = MedicationSerializer(
        data={"name": "Dipirona"}, context=owner_request_context
    )

    assert not serializer.is_valid()
    assert serializer.errors == {"non_field_errors": [DUPLICATE_MEDICATION_MESSAGE]}


@pytest.mark.django_db
def test_medication_of_another_account_is_not_a_duplicate(
    medication_data: dict[str, str],
    other_account: User,
    owner_request_context: dict[str, Any],
) -> None:
    """The same combination held by another account does not block the requester."""
    Medication.objects.create(owner=other_account, **medication_data)
    serializer = MedicationSerializer(
        data=medication_data, context=owner_request_context
    )

    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_edit_that_keeps_the_combination_is_accepted(
    existing_medication: Medication, owner_request_context: dict[str, Any]
) -> None:
    """A medication is not a duplicate of itself when only its state changes."""
    serializer = MedicationSerializer(
        instance=existing_medication,
        data={"state": "suspended"},
        partial=True,
        context=owner_request_context,
    )

    assert serializer.is_valid(), serializer.errors
    assert serializer.save().state == "suspended"


@pytest.mark.django_db
def test_edit_into_another_medication_is_refused(
    medication_data: dict[str, str],
    owner: User,
    existing_medication: Medication,
    owner_request_context: dict[str, Any],
) -> None:
    """Editing a medication into the combination of another one is a duplicate."""
    medication = Medication.objects.create(
        owner=owner, **{**medication_data, "form": "capsule"}
    )
    serializer = MedicationSerializer(
        instance=medication,
        data={"form": "tablet"},
        partial=True,
        context=owner_request_context,
    )

    assert not serializer.is_valid()
    assert serializer.errors == {"non_field_errors": [DUPLICATE_MEDICATION_MESSAGE]}


@pytest.mark.django_db
def test_refused_edit_leaves_the_medication_in_memory_unchanged(
    medication_data: dict[str, str],
    owner: User,
    existing_medication: Medication,
    owner_request_context: dict[str, Any],
) -> None:
    """Validation of a refused edit does not write the values on the instance."""
    medication = Medication.objects.create(
        owner=owner, **{**medication_data, "form": "capsule"}
    )
    serializer = MedicationSerializer(
        instance=medication,
        data={"form": "tablet"},
        partial=True,
        context=owner_request_context,
    )

    assert not serializer.is_valid()
    assert medication.form == "capsule"


@pytest.mark.django_db
def test_duplicate_saved_after_validation_is_refused_on_create(
    medication_data: dict[str, str], owner: User, existing_medication: Medication
) -> None:
    """A duplicate saved between validation and create is an error, not a crash."""
    with pytest.raises(ValidationError) as error:
        MedicationSerializer().create({**medication_data, "owner": owner})

    assert error.value.detail == {"non_field_errors": [DUPLICATE_MEDICATION_MESSAGE]}
    assert Medication.objects.count() == 1


@pytest.mark.django_db
def test_duplicate_saved_after_validation_is_refused_on_update(
    medication_data: dict[str, str], owner: User, existing_medication: Medication
) -> None:
    """A duplicate saved between validation and update is an error, not a crash."""
    medication = Medication.objects.create(
        owner=owner, **{**medication_data, "form": "capsule"}
    )

    with pytest.raises(ValidationError) as error:
        MedicationSerializer().update(medication, {"form": "tablet"})

    assert error.value.detail == {"non_field_errors": [DUPLICATE_MEDICATION_MESSAGE]}
    medication.refresh_from_db()
    assert medication.form == "capsule"
