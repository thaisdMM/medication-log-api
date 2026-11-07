"""Tests for how the API schema describes the medication endpoints."""

from typing import Any

import pytest
from django.test import Client

from medications.serializers import CONCENTRATION_VALUE_HELP_TEXT


def get_schema(client: Client) -> dict[str, Any]:
    """Return the schema served to the Swagger UI page."""
    response = client.get("/api/schema/?format=json")
    assert response.status_code == 200
    schema: dict[str, Any] = response.json()
    return schema


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
