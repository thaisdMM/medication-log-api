"""The medication model: what an account records about one medication."""

from typing import ClassVar

from django.conf import settings
from django.db import models
from django.db.models import F
from django.db.models.functions import Lower

DUPLICATE_MEDICATION_MESSAGE = (
    "You already have this medication with the same concentration and form."
)


class ConcentrationUnit(models.TextChoices):
    """The units a concentration is written in."""

    MG = "mg"
    G = "g"
    ML = "ml"
    OTHER = "other"


class MedicationForm(models.TextChoices):
    """The ways a medication is presented."""

    TABLET = "tablet"
    CAPSULE = "capsule"
    DROP = "drop"
    ML = "ml"
    SACHET = "sachet"
    PATCH = "patch"
    SUPPOSITORY = "suppository"
    OINTMENT = "ointment"
    OTHER = "other"


class MedicationState(models.TextChoices):
    """Whether the account is currently taking a medication."""

    IN_USE = "in_use"
    SUSPENDED = "suspended"


class Medication(models.Model):
    """A medication an account records: a name, a concentration and a form.

    Attributes:
        owner: The account the medication belongs to
        name: Medication name, as typed
        concentration_value: Amount of active substance, when informed
        concentration_unit: Unit of the concentration, empty when not chosen
        form: How the medication is presented, empty when not chosen
        state: Whether the account takes the medication or suspended it
    """

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    concentration_value = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True
    )
    concentration_unit = models.CharField(
        max_length=5, choices=ConcentrationUnit, blank=True
    )
    form = models.CharField(max_length=20, choices=MedicationForm, blank=True)
    state = models.CharField(
        max_length=20, choices=MedicationState, default=MedicationState.IN_USE
    )

    class Meta:
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                F("owner"),
                Lower("name"),
                F("concentration_value"),
                F("concentration_unit"),
                F("form"),
                name="unique_medication_per_owner",
                nulls_distinct=False,
                violation_error_message=DUPLICATE_MEDICATION_MESSAGE,
            )
        ]

    def __str__(self) -> str:
        """String representation of the medication.

        Returns:
            str: string representation with class name and database ID.
        """
        return f"{self.__class__.__name__} (id={self.id})"
