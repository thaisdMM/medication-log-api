"""Tests for the medication endpoints."""

from decimal import Decimal

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


@pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
@pytest.mark.django_db
def test_detail_request_without_a_token_is_refused(
    client: Client, existing_medication: Medication, method: str
) -> None:
    """A detail request with no token is not authenticated and changes nothing."""
    response = getattr(client, method)(
        reverse("medication-detail", args=[existing_medication.id]),
        {"name": "Losartana", "state": "suspended"},
        content_type="application/json",
    )

    assert response.status_code == 401
    assert Medication.objects.filter(
        id=existing_medication.id, name="Dipirona", state="in_use"
    ).exists()


@pytest.mark.django_db
def test_retrieving_answers_with_the_medication_without_the_owner(
    client: Client, owner_token: str, existing_medication: Medication
) -> None:
    """A medication of the account is returned with its fields and no owner."""
    response = client.get(
        reverse("medication-detail", args=[existing_medication.id]),
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": existing_medication.id,
        "name": "Dipirona",
        "concentration_value": "500",
        "concentration_unit": "mg",
        "form": "tablet",
        "state": "in_use",
    }


@pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
@pytest.mark.django_db
def test_medication_of_another_account_is_not_found(
    client: Client, other_account: User, owner_token: str, method: str
) -> None:
    """Another account's medication answers as missing and is left unchanged."""
    medication = Medication.objects.create(owner=other_account, name="Losartana")

    response = getattr(client, method)(
        reverse("medication-detail", args=[medication.id]),
        {"name": "Dipirona", "state": "suspended"},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 404
    assert Medication.objects.filter(
        id=medication.id, name="Losartana", state="in_use"
    ).exists()


@pytest.mark.parametrize(
    ("stored", "sent"),
    [
        pytest.param("in_use", "suspended", id="suspend"),
        pytest.param("suspended", "in_use", id="resume"),
    ],
)
@pytest.mark.django_db
def test_patching_the_state_changes_it(
    client: Client,
    owner: User,
    owner_token: str,
    medication_data: dict[str, str],
    stored: str,
    sent: str,
) -> None:
    """A partial edit of the state alone saves the new state."""
    medication = Medication.objects.create(
        owner=owner, **{**medication_data, "state": stored}
    )

    response = client.patch(
        reverse("medication-detail", args=[medication.id]),
        {"state": sent},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 200
    assert response.json()["state"] == sent
    medication.refresh_from_db()
    assert medication.state == sent


@pytest.mark.django_db
def test_patching_into_a_duplicate_answers_a_validation_error_with_the_fixed_message(
    client: Client,
    owner: User,
    owner_token: str,
    existing_medication: Medication,
    medication_data: dict[str, str],
) -> None:
    """An edit into a medication the account already holds is refused unsaved."""
    medication = Medication.objects.create(
        owner=owner, **{**medication_data, "form": "capsule"}
    )

    response = client.patch(
        reverse("medication-detail", args=[medication.id]),
        {"form": "tablet"},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 400
    assert response.json() == {"non_field_errors": [DUPLICATE_MEDICATION_MESSAGE]}
    medication.refresh_from_db()
    assert medication.form == "capsule"


@pytest.mark.django_db
def test_putting_into_a_duplicate_answers_a_validation_error_with_the_fixed_message(
    client: Client,
    owner: User,
    owner_token: str,
    existing_medication: Medication,
    medication_data: dict[str, str],
) -> None:
    """A full edit into a medication the account already holds is refused unsaved."""
    medication = Medication.objects.create(
        owner=owner, **{**medication_data, "form": "capsule"}
    )

    response = client.put(
        reverse("medication-detail", args=[medication.id]),
        medication_data,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 400
    assert response.json() == {"non_field_errors": [DUPLICATE_MEDICATION_MESSAGE]}
    medication.refresh_from_db()
    assert medication.form == "capsule"


@pytest.mark.django_db
def test_putting_replaces_the_fields_sent(
    client: Client, owner_token: str, existing_medication: Medication
) -> None:
    """A full edit saves every field sent."""
    response = client.put(
        reverse("medication-detail", args=[existing_medication.id]),
        {
            "name": "Losartana",
            "concentration_value": "0.025",
            "concentration_unit": "g",
            "form": "capsule",
            "state": "suspended",
        },
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": existing_medication.id,
        "name": "Losartana",
        "concentration_value": "0.025",
        "concentration_unit": "g",
        "form": "capsule",
        "state": "suspended",
    }
    existing_medication.refresh_from_db()
    assert existing_medication.name == "Losartana"
    assert existing_medication.concentration_value == Decimal("0.025")
    assert existing_medication.concentration_unit == "g"
    assert existing_medication.form == "capsule"
    assert existing_medication.state == "suspended"


@pytest.mark.django_db
def test_putting_without_the_optional_fields_keeps_them(
    client: Client, owner: User, owner_token: str, medication_data: dict[str, str]
) -> None:
    """A full edit with only the name keeps the stored optional fields."""
    medication = Medication.objects.create(
        owner=owner, **{**medication_data, "state": "suspended"}
    )

    response = client.put(
        reverse("medication-detail", args=[medication.id]),
        {"name": "Losartana"},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": medication.id,
        "name": "Losartana",
        "concentration_value": "500",
        "concentration_unit": "mg",
        "form": "tablet",
        "state": "suspended",
    }


@pytest.mark.django_db
def test_deleting_removes_the_medication(
    client: Client, owner_token: str, existing_medication: Medication
) -> None:
    """A deleted medication answers with no content and leaves the database."""
    response = client.delete(
        reverse("medication-detail", args=[existing_medication.id]),
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 204
    assert not Medication.objects.filter(id=existing_medication.id).exists()
