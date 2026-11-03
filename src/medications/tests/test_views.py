"""Tests for the medication list and create endpoint."""

import pytest
from django.test import Client
from django.urls import reverse

from medications.models import DUPLICATE_MEDICATION_MESSAGE, Medication
from users.models import User


@pytest.mark.django_db
def test_listing_without_a_token_is_refused(client: Client) -> None:
    """A list request with no token is not authenticated."""
    response = client.get(reverse("medication-list"))

    assert response.status_code == 401


@pytest.mark.django_db
def test_creating_without_a_token_is_refused(
    client: Client, medication_data: dict[str, str]
) -> None:
    """A create request with no token is not authenticated and saves nothing."""
    response = client.post(
        reverse("medication-list"), medication_data, content_type="application/json"
    )

    assert response.status_code == 401
    assert not Medication.objects.exists()


@pytest.mark.django_db
def test_list_holds_only_the_medications_of_the_account(
    client: Client, owner: User, other_account: User, owner_token: str
) -> None:
    """A medication of another account is left out of the list."""
    medication = Medication.objects.create(owner=owner, name="Dipirona")
    Medication.objects.create(owner=other_account, name="Losartana")

    response = client.get(
        reverse("medication-list"), HTTP_AUTHORIZATION=f"Token {owner_token}"
    )

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [medication.id]


@pytest.mark.django_db
def test_list_is_alphabetical_ignoring_case(
    client: Client, owner: User, owner_token: str
) -> None:
    """Names are ordered by their letters, whatever their case."""
    for name in ("Zolpidem", "amoxicilina", "Dipirona"):
        Medication.objects.create(owner=owner, name=name)

    response = client.get(
        reverse("medication-list"), HTTP_AUTHORIZATION=f"Token {owner_token}"
    )

    assert [item["name"] for item in response.json()] == [
        "amoxicilina",
        "Dipirona",
        "Zolpidem",
    ]


@pytest.mark.django_db
def test_list_places_accented_names_among_the_other_letters(
    client: Client, owner: User, owner_token: str
) -> None:
    """A name with an accented first letter is ordered with its plain letter."""
    for name in ("Zolpidem", "Éter", "amoxicilina", "Ácido"):
        Medication.objects.create(owner=owner, name=name)

    response = client.get(
        reverse("medication-list"), HTTP_AUTHORIZATION=f"Token {owner_token}"
    )

    assert [item["name"] for item in response.json()] == [
        "Ácido",
        "amoxicilina",
        "Éter",
        "Zolpidem",
    ]


@pytest.mark.django_db
def test_names_differing_only_in_case_are_listed_in_creation_order(
    client: Client, owner: User, owner_token: str
) -> None:
    """Names equal when case is ignored are ordered by the oldest first."""
    Medication.objects.create(owner=owner, name="Dipirona", form="tablet")
    Medication.objects.create(owner=owner, name="dipirona", form="capsule")

    response = client.get(
        reverse("medication-list"), HTTP_AUTHORIZATION=f"Token {owner_token}"
    )

    assert [item["name"] for item in response.json()] == ["Dipirona", "dipirona"]


@pytest.mark.django_db
def test_list_without_a_state_holds_every_state(
    client: Client, owner: User, owner_token: str
) -> None:
    """With no state in the query, in use and suspended medications are listed."""
    Medication.objects.create(owner=owner, name="Dipirona", state="in_use")
    Medication.objects.create(owner=owner, name="Losartana", state="suspended")

    response = client.get(
        reverse("medication-list"), HTTP_AUTHORIZATION=f"Token {owner_token}"
    )

    assert [item["state"] for item in response.json()] == ["in_use", "suspended"]


@pytest.mark.parametrize("state", ["in_use", "suspended"])
@pytest.mark.django_db
def test_list_with_a_state_holds_only_that_state(
    client: Client, owner: User, owner_token: str, state: str
) -> None:
    """The state in the query leaves out the medications in the other state."""
    Medication.objects.create(owner=owner, name="Dipirona", state="in_use")
    Medication.objects.create(owner=owner, name="Losartana", state="suspended")

    response = client.get(
        reverse("medication-list"),
        {"state": state},
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert [item["state"] for item in response.json()] == [state]


@pytest.mark.parametrize(
    "state",
    [
        pytest.param("banana", id="outside_the_closed_list"),
        pytest.param("", id="empty"),
    ],
)
@pytest.mark.django_db
def test_list_with_an_invalid_state_is_refused(
    client: Client, owner_token: str, state: str
) -> None:
    """A state outside the closed list is an error on the state field."""
    response = client.get(
        reverse("medication-list"),
        {"state": state},
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 400
    assert "state" in response.json()


@pytest.mark.django_db
def test_creating_answers_with_the_medication_without_the_owner(
    client: Client, owner_token: str, medication_data: dict[str, str]
) -> None:
    """A created medication is returned with its fields and no owner."""
    response = client.post(
        reverse("medication-list"),
        medication_data,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": Medication.objects.get().id,
        "name": "Dipirona",
        "concentration_value": "500",
        "concentration_unit": "mg",
        "form": "tablet",
        "state": "in_use",
    }


@pytest.mark.django_db
def test_created_medication_belongs_to_the_account_of_the_token(
    client: Client,
    owner: User,
    other_account: User,
    owner_token: str,
    medication_data: dict[str, str],
) -> None:
    """An owner sent in the body is ignored in favour of the token's account."""
    response = client.post(
        reverse("medication-list"),
        {**medication_data, "owner": other_account.id},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 201
    assert Medication.objects.get().owner == owner


@pytest.mark.django_db
def test_creating_a_duplicate_answers_a_validation_error_with_the_fixed_message(
    client: Client, owner: User, owner_token: str
) -> None:
    """A duplicate blank except for the name is refused and nothing is saved."""
    Medication.objects.create(owner=owner, name="Dipirona")

    response = client.post(
        reverse("medication-list"),
        {"name": "Dipirona"},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 400
    assert response.json() == {"non_field_errors": [DUPLICATE_MEDICATION_MESSAGE]}
    assert Medication.objects.count() == 1
