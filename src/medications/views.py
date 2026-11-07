"""Views for the medication."""

from http import HTTPStatus
from typing import Any

from django.db.models import QuerySet
from django.db.models.functions import Collate, Lower
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import generics

from config.mixins import OwnerFilterMixin
from config.schema import ErrorDetailSerializer
from medications.models import Medication
from medications.serializers import (
    MedicationListFilterSerializer,
    MedicationSerializer,
)

INVALID_INPUT = OpenApiResponse(
    OpenApiTypes.OBJECT,
    description="Each refused field with its messages; a duplicate under non_field_errors.",
)
MISSING_TOKEN = OpenApiResponse(
    ErrorDetailSerializer, description="The token is missing, invalid or expired."
)
NOT_FOUND = OpenApiResponse(
    ErrorDetailSerializer,
    description="No medication with this id belongs to the account.",
)


@extend_schema_view(
    get=extend_schema(
        summary="List the account's medications",
        parameters=[MedicationListFilterSerializer],
        responses={
            HTTPStatus.OK: MedicationSerializer(many=True),
            HTTPStatus.BAD_REQUEST: OpenApiResponse(
                OpenApiTypes.OBJECT, description="The state is outside the closed list."
            ),
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
        },
    ),
    post=extend_schema(
        summary="Create a medication",
        responses={
            HTTPStatus.CREATED: MedicationSerializer,
            HTTPStatus.BAD_REQUEST: INVALID_INPUT,
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
        },
    ),
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


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve a medication",
        responses={
            HTTPStatus.OK: MedicationSerializer,
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
            HTTPStatus.NOT_FOUND: NOT_FOUND,
        },
    ),
    put=extend_schema(
        summary="Update a medication",
        responses={
            HTTPStatus.OK: MedicationSerializer,
            HTTPStatus.BAD_REQUEST: INVALID_INPUT,
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
            HTTPStatus.NOT_FOUND: NOT_FOUND,
        },
    ),
    patch=extend_schema(
        summary="Update some fields of a medication",
        responses={
            HTTPStatus.OK: MedicationSerializer,
            HTTPStatus.BAD_REQUEST: INVALID_INPUT,
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
            HTTPStatus.NOT_FOUND: NOT_FOUND,
        },
    ),
    delete=extend_schema(
        summary="Delete a medication",
        responses={
            HTTPStatus.NO_CONTENT: None,
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
            HTTPStatus.NOT_FOUND: NOT_FOUND,
        },
    ),
)
class MedicationDetailView(
    OwnerFilterMixin, generics.RetrieveUpdateDestroyAPIView[Medication]
):
    """Retrieve, update and delete a medication of the requesting account.

    Attributes:
        owner_path: Lookup path from the medication to the owning account.
    """

    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    owner_path = "owner"
