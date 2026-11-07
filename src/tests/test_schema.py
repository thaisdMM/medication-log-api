"""Tests for the clean-up applied to the API schema before it is served."""

from typing import Any

import pytest
from django.test import Client

DOCSTRING_SECTIONS = ["Args:", "Attributes:", "Raises:", "Returns:"]


def schema_descriptions(schema: dict[str, Any]) -> list[str]:
    """Collect the description of every operation and component of the schema."""
    items = [
        operation
        for path_item in schema["paths"].values()
        for operation in path_item.values()
    ]
    items += list(schema["components"]["schemas"].values())
    return [item["description"] for item in items if "description" in item]


@pytest.mark.parametrize("section", DOCSTRING_SECTIONS)
def test_schema_descriptions_leave_out_the_docstring_sections(
    client: Client, section: str
) -> None:
    """No description in the schema carries a docstring section."""
    response = client.get("/api/schema/?format=json")

    descriptions = schema_descriptions(response.json())
    assert descriptions
    assert not [text for text in descriptions if section in text.splitlines()]


def test_schema_descriptions_keep_the_text_above_the_sections(client: Client) -> None:
    """A description keeps the docstring text written before its first section."""
    response = client.get("/api/schema/?format=json")

    operation = response.json()["paths"]["/api/medications/"]["get"]
    assert operation["description"] == (
        "List the medications of the requesting account and create new ones."
    )
