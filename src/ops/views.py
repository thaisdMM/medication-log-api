"""Operational endpoints: they report on the system, never on its data."""

from django.db import Error, connection
from django.http import HttpRequest, JsonResponse


def healthz(request: HttpRequest) -> JsonResponse:
    """Report whether the application can reach its database.

    The response body names which check failed, never why: this endpoint
    is public and unauthenticated, and a database exception message caries
    the host, the port and the database user.

    Args:
        request: The incomming HTTP request. Unused, required by Django.

    Returns:
        JsonResponse: 200 when every check passes,
        503 when the database is unreachable.
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

    except Error:
        return JsonResponse(
            {"status": "unavailable", "checks": {"database": "failing"}}, status=503
        )

    return JsonResponse({"status": "ok", "checks": {"database": "ok"}})
