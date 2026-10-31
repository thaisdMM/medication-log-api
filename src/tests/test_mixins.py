"""Tests for the owner filter that restricts a view's queries to the requester."""

import pytest
from django.core.exceptions import ImproperlyConfigured
from rest_framework import generics, serializers
from rest_framework.test import APIRequestFactory, force_authenticate

from config.mixins import MISSING_OWNER_PATH_MESSAGE, OwnerFilterMixin
from medications.models import Medication
from users.models import User


class MedicationIdSerializer(serializers.ModelSerializer[Medication]):
    """Expose only the id, enough to tell which rows a view returned."""

    class Meta:
        model = Medication
        fields = ("id",)


class ViewWithoutOwnerPath(OwnerFilterMixin, generics.ListAPIView[Medication]):
    """Stands in for an endpoint that forgets to declare its path to the owner."""

    queryset = Medication.objects.all()
    serializer_class = MedicationIdSerializer


class ViewWithOwnerPath(OwnerFilterMixin, generics.ListAPIView[Medication]):
    """Stands in for an endpoint that declares its path to the owner."""

    queryset = Medication.objects.all()
    serializer_class = MedicationIdSerializer
    owner_path = "owner"


@pytest.fixture
def requester() -> User:
    """The account that makes the request."""
    return User.objects.create_user(
        email="ana.ribeiro@example.com",
        name="Ana Ribeiro",
        password="Blue-Kettle-42",
    )


@pytest.fixture
def other_account() -> User:
    """A second account, unrelated to the requester."""
    return User.objects.create_user(
        email="bruno.costa@example.com",
        name="Bruno Costa",
        password="Green-Lantern-17",
    )


@pytest.mark.django_db
def test_view_without_owner_path_fails_on_its_first_call(requester: User) -> None:
    """A view that declares no owner path raises a message saying what is missing."""
    request = APIRequestFactory().get("/")
    force_authenticate(request, user=requester)

    with pytest.raises(ImproperlyConfigured) as raised:
        ViewWithoutOwnerPath.as_view()(request)

    assert str(raised.value) == MISSING_OWNER_PATH_MESSAGE.format(
        view="ViewWithoutOwnerPath"
    )


@pytest.mark.django_db
def test_view_with_owner_path_returns_only_the_requesters_rows(
    requester: User, other_account: User
) -> None:
    """A row that belongs to another account is left out of the response."""
    own_medication = Medication.objects.create(owner=requester, name="Losartan")
    Medication.objects.create(owner=other_account, name="Losartan")
    request = APIRequestFactory().get("/")
    force_authenticate(request, user=requester)

    response = ViewWithOwnerPath.as_view()(request)

    assert response.status_code == 200
    assert response.data == [{"id": own_medication.id}]
