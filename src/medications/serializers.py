"""Serializers for the medication."""

from copy import copy
from decimal import Decimal
from typing import Any, ClassVar

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from rest_framework import serializers

from medications.models import DUPLICATE_MEDICATION_MESSAGE, Medication


class MedicationSerializer(serializers.ModelSerializer[Medication]):
    """Validate a medication of the requesting account and represent it.

    Attributes:
        owner: The requesting account, accepted from no input and never returned.
    """

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Medication
        fields = (
            "id",
            "owner",
            "name",
            "concentration_value",
            "concentration_unit",
            "form",
            "state",
        )
        extra_kwargs: ClassVar[dict[str, dict[str, Any]]] = {
            "concentration_value": {
                "min_value": Decimal("0.001"),
                "normalize_output": True,
            }
        }

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Refuse a combination the account already holds in another medication.

        Args:
            attrs: Field values that passed field-level validation.

        Returns:
            dict[str, Any]: The same field values, unchanged.

        Raises:
            ValidationError: When the duplicate constraint rejects the values.
        """
        candidate = copy(self.instance) if self.instance else Medication()
        for field, value in attrs.items():
            setattr(candidate, field, value)
        try:
            candidate.validate_constraints()
        except DjangoValidationError as error:
            raise self._duplicate_error() from error
        return attrs

    def create(self, validated_data: dict[str, Any]) -> Medication:
        """Create the medication.

        Args:
            validated_data: Field values that passed validation, with the owner.

        Returns:
            Medication: The created medication.

        Raises:
            ValidationError: When the duplicate was saved after validation.
        """
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError as error:
            raise self._duplicate_error() from error

    def update(
        self, instance: Medication, validated_data: dict[str, Any]
    ) -> Medication:
        """Update the medication.

        Args:
            instance: The medication being edited.
            validated_data: Field values that passed validation.

        Returns:
            Medication: The updated medication.

        Raises:
            ValidationError: When the duplicate was saved after validation.
        """
        try:
            with transaction.atomic():
                return super().update(instance, validated_data)
        except IntegrityError as error:
            raise self._duplicate_error() from error

    def _duplicate_error(self) -> serializers.ValidationError:
        """Build the error of a duplicate caught by the database.

        Returns:
            ValidationError: The duplicate message outside any field.
        """
        return serializers.ValidationError(
            {"non_field_errors": [DUPLICATE_MEDICATION_MESSAGE]}
        )
