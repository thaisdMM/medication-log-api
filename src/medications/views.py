"""Views for the medication."""

from typing import Any

from django.db.models import QuerySet
from django.db.models.functions import Collate, Lower
from rest_framework import generics

from config.mixins import OwnerFilterMixin
from medications.models import Medication
from medications.serializers import (
    MedicationListFilterSerializer,
    MedicationSerializer,
)


class MedicationListCreateView(
    OwnerFilterMixin, generics.ListCreateAPIView[Medication]
):
    """List the medications of the requesting account and create new ones.

    Attributes:
        owner_path: Lookup path from the medication to the owning account.
    """

    queryset = Medication.objects.order_by(Collate(Lower("name"), "und-x-icu"), "id")
    serializer_class = MedicationSerializer
    owner_path = "owner"

    def filter_queryset(self, queryset: QuerySet[Any]) -> QuerySet[Any]:
        """Keep only the medications in the state asked for in the query.

        Args:
            queryset: The medications of the requesting account.

        Returns:
            QuerySet: The medications in that state, or all of them when none is asked.

        Raises:
            ValidationError: When the state is outside the closed list.
        """
        filters = MedicationListFilterSerializer(data=self.request.query_params.dict())
        filters.is_valid(raise_exception=True)
        state = filters.validated_data.get("state")
        if state is None:
            return queryset
        return queryset.filter(state=state)
