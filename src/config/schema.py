"""Clean-up applied to the API schema before it is served."""

from typing import Any

from drf_spectacular.generators import SchemaGenerator
from rest_framework import serializers
from rest_framework.request import Request

DOCSTRING_SECTIONS = frozenset({"Args:", "Attributes:", "Raises:", "Returns:"})


def strip_docstring_sections(
    result: dict[str, Any],
    generator: SchemaGenerator,
    request: Request | None,
    public: bool,
) -> dict[str, Any]:
    """Remove the docstring sections from every description in the schema.

    Args:
        result: The schema built by drf-spectacular.
        generator: The generator that built the schema.
        request: The request for the schema, when served over HTTP.
        public: Whether the schema ignores the requester's permissions.

    Returns:
        dict[str, Any]: The same schema, with each description cut at its first
            docstring section.
    """
    for path_item in result.get("paths", {}).values():
        for operation in path_item.values():
            _strip_description(operation)
    for component in result.get("components", {}).get("schemas", {}).values():
        _strip_description(component)
    return result


def _strip_description(item: dict[str, Any]) -> None:
    """Cut a description at its first docstring section, in place.

    Args:
        item: An operation or component of the schema.
    """
    description = item.get("description")
    if not description:
        return
    kept: list[str] = []
    for line in description.splitlines():
        if line.strip() in DOCSTRING_SECTIONS:
            break
        kept.append(line)
    item["description"] = "\n".join(kept).strip()


class ErrorDetailSerializer(serializers.Serializer[dict[str, str]]):
    """Describe an error body with a single message, for the API schema only.

    Attributes:
        detail: The message saying why the request was refused.
    """

    detail = serializers.CharField()
