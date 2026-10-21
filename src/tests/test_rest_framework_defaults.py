"""Tests for the project-wide Django REST framework configuration."""

import pytest
from django.test import Client
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView


class ViewWithoutPermissionClasses(APIView):
    """Stands in for any endpoint that forgets to declare its own permission."""

    def get(self, request: Request) -> Response:
        """Return a body that only an allowed request can reach.

        Args:
            request: The incoming API request.

        Returns:
            Response: 200 with a fixed body.
        """
        return Response({"reached": True})


def test_view_without_permission_classes_refuses_anonymous_request() -> None:
    """An endpoint that declares no permission is closed, not open, by default."""
    request = APIRequestFactory().get("/")

    response = ViewWithoutPermissionClasses.as_view()(request)

    assert response.status_code == 401
    assert response["WWW-Authenticate"].startswith("Token")
    assert response.data == {"detail": "Authentication credentials were not provided."}


@pytest.mark.django_db
def test_html_is_not_an_available_format(client: Client) -> None:
    """Only JSON is rendered: the browsable API page is turned off."""
    response = client.post(reverse("user-register"), HTTP_ACCEPT="text/html")

    assert response.status_code == 406
