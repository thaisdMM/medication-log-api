"""Tests for the errors answered outside the API views."""

import pytest
from django.core.exceptions import PermissionDenied
from django.test import Client

from config.error_handlers import (
    BAD_REQUEST_MESSAGE,
    NOT_FOUND_MESSAGE,
    PERMISSION_DENIED_MESSAGE,
    SERVER_ERROR_MESSAGE,
)


class RefusingConnection:
    """Stands in for the database connection when the request is not allowed."""

    def cursor(self) -> None:
        """Raise what a refused permission raises.

        Raises:
            PermissionDenied: Always.
        """
        raise PermissionDenied


class FailingConnection:
    """Stands in for the database connection when an unexpected error happens."""

    def cursor(self) -> None:
        """Raise an error that no view handles.

        Raises:
            RuntimeError: Always.
        """
        raise RuntimeError("unexpected failure")


def test_path_with_no_route_answers_not_found_as_json(client: Client) -> None:
    """A path that matches no route answers with a JSON message."""
    response = client.get("/api/medications//")

    assert response.status_code == 404
    assert response.json() == {"detail": NOT_FOUND_MESSAGE}


def test_unknown_host_answers_bad_request_as_json(client: Client) -> None:
    """A request for a host outside the allowed list answers with a JSON message."""
    response = client.get("/healthz/", HTTP_HOST="unknown.example")

    assert response.status_code == 400
    assert response.json() == {"detail": BAD_REQUEST_MESSAGE}


def test_permission_denied_outside_the_api_answers_as_json(
    client: Client,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A refused permission outside the API views answers with a JSON message."""
    monkeypatch.setattr("ops.views.connection", RefusingConnection())

    response = client.get("/healthz/")

    assert response.status_code == 403
    assert response.json() == {"detail": PERMISSION_DENIED_MESSAGE}


def test_unhandled_error_answers_server_error_as_json(
    client: Client,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An error no view handles answers with a JSON message and nothing of the error."""
    monkeypatch.setattr("ops.views.connection", FailingConnection())
    client.raise_request_exception = False

    response = client.get("/healthz/")

    assert response.status_code == 500
    assert response.json() == {"detail": SERVER_ERROR_MESSAGE}
