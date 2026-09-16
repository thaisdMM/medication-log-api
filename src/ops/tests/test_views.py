"""Tests for the operational endpoints."""

import pytest
from django.db import OperationalError
from django.test import Client


class BrokenConnection:
    """Stands in for the database connection when the database is unreachable."""

    def cursor(self) -> None:
        """Raise what a refused connection raises.

        Raises:
            OperationalError: always.
        """
        raise OperationalError("connection refused")


@pytest.mark.django_db
def test_healthz_returns_200_when_the_database_answers(client: Client) -> None:
    """Endpoint reports the system as healthy when the database responds."""
    response = client.get("/healthz/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "checks": {"database": "ok"}}


def test_healthz_returns_503_when_the_database_is_unreachable(
    client: Client,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Endpoint reports the database as failing when the connection is refused."""
    monkeypatch.setattr("ops.views.connection", BrokenConnection())

    response = client.get("/healthz/")

    assert response.status_code == 503
    assert response.json() == {
        "status": "unavailable",
        "checks": {"database": "failing"},
    }


def test_healthz_without_trailing_slash_redirects(client: Client) -> None:
    """A request without the trailing slash is redirected, not answered."""
    response = client.get("/healthz")

    assert response.status_code == 301
    assert response["Location"] == "/healthz/"
