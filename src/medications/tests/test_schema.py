"""Tests for how the API schema describes the medication endpoints."""

from typing import Any

import pytest
from django.test import Client
from django.urls import reverse

from medications.models import Medication
from medications.serializers import CONCENTRATION_VALUE_HELP_TEXT, MedicationSerializer
from users.models import User


def get_schema(client: Client) -> dict[str, Any]:
    """Return the schema served to the Swagger UI page."""
    response = client.get("/api/schema/?format=json")
    assert response.status_code == 200
    schema: dict[str, Any] = response.json()
    return schema


def only_example(body: dict[str, Any]) -> Any:
    """Return the value of the single example of a request or response body."""
    (example,) = body["content"]["application/json"]["examples"].values()
    return example["value"]


def named_example(answer: dict[str, Any], name: str) -> Any:
    """Return the value of the example shown with this name in a response."""
    examples = answer["content"]["application/json"]["examples"]
    return next(
        example["value"]
        for key, example in examples.items()
        if example.get("summary", key) == name
    )


@pytest.mark.parametrize(
    ("component", "values"),
    [
        ("ConcentrationUnitEnum", ["mg", "g", "ml", "other"]),
        (
            "FormEnum",
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
        ),
        ("StateEnum", ["in_use", "suspended"]),
    ],
)
def test_schema_lists_the_values_of_each_closed_list(
    client: Client, component: str, values: list[str]
) -> None:
    """Each closed list of the medication shows all of its values."""
    schema = get_schema(client)

    assert schema["components"]["schemas"][component]["enum"] == values


def test_schema_describes_the_concentration_value_limits(client: Client) -> None:
    """The concentration value says it must be above zero, with three decimals."""
    schema = get_schema(client)

    field = schema["components"]["schemas"]["Medication"]["properties"][
        "concentration_value"
    ]
    assert field["description"] == CONCENTRATION_VALUE_HELP_TEXT


def test_schema_lists_the_state_filter_of_the_medication_list(client: Client) -> None:
    """The list documents the optional state filter with its values."""
    schema = get_schema(client)

    parameters = schema["paths"]["/api/medications/"]["get"]["parameters"]
    assert [(p["name"], p["in"], p["schema"]["enum"]) for p in parameters] == [
        ("state", "query", ["in_use", "suspended"])
    ]


@pytest.mark.parametrize(
    ("path", "method", "statuses"),
    [
        ("/api/medications/", "get", {"200", "400", "401"}),
        ("/api/medications/", "post", {"201", "400", "401"}),
        ("/api/medications/{id}/", "get", {"200", "401", "404"}),
        ("/api/medications/{id}/", "put", {"200", "400", "401", "404"}),
        ("/api/medications/{id}/", "patch", {"200", "400", "401", "404"}),
        ("/api/medications/{id}/", "delete", {"204", "401", "404"}),
    ],
)
def test_schema_lists_the_responses_of_each_medication_operation(
    client: Client, path: str, method: str, statuses: set[str]
) -> None:
    """Each medication operation documents its success and its error responses."""
    schema = get_schema(client)

    assert set(schema["paths"][path][method]["responses"]) == statuses


@pytest.mark.django_db
def test_medication_request_example_is_accepted_by_the_serializer(
    client: Client, owner_request_context: dict[str, Any]
) -> None:
    """The medication in the request example passes the serializer validation."""
    body = get_schema(client)["paths"]["/api/medications/"]["post"]["requestBody"]

    serializer = MedicationSerializer(
        data=only_example(body), context=owner_request_context
    )

    assert serializer.is_valid(), serializer.errors


def test_medication_response_example_shows_every_returned_field(
    client: Client,
) -> None:
    """The medication in the response example has every field the API returns."""
    operation = get_schema(client)["paths"]["/api/medications/{id}/"]["get"]

    returned = {
        name
        for name, field in MedicationSerializer().fields.items()
        if not field.write_only
    }
    assert set(only_example(operation["responses"]["200"])) == returned


@pytest.mark.django_db
def test_not_found_example_matches_the_real_response(
    client: Client, other_account: User, owner_token: str
) -> None:
    """The not-found example is the body sent for another account's medication."""
    operation = get_schema(client)["paths"]["/api/medications/{id}/"]["get"]
    medication = Medication.objects.create(owner=other_account, name="Losartana")

    response = client.get(
        reverse("medication-detail", args=[medication.id]),
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 404
    assert response.json() == only_example(operation["responses"]["404"])


@pytest.mark.django_db
def test_invalid_state_example_matches_the_real_response(
    client: Client, owner_token: str
) -> None:
    """The invalid-state example is the body sent for a state outside the list."""
    operation = get_schema(client)["paths"]["/api/medications/"]["get"]

    response = client.get(
        reverse("medication-list"),
        {"state": "paused"},
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 400
    assert response.json() == only_example(operation["responses"]["400"])


@pytest.mark.parametrize(
    ("name", "body"),
    [
        pytest.param(
            "Refused field", {"concentration_value": "0"}, id="concentration-zero"
        ),
        pytest.param("Duplicate", {}, id="duplicate"),
    ],
)
@pytest.mark.django_db
def test_invalid_input_example_matches_the_real_response(
    client: Client,
    owner_token: str,
    medication_data: dict[str, str],
    existing_medication: Medication,
    name: str,
    body: dict[str, str],
) -> None:
    """Each invalid-input example is the body sent back for that refusal."""
    answer = get_schema(client)["paths"]["/api/medications/"]["post"]["responses"]
    response = client.post(
        reverse("medication-list"),
        {**medication_data, **body},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {owner_token}",
    )

    assert response.status_code == 400
    assert response.json() == named_example(answer["400"], name)
