"""Tests for the project-wide Django REST framework configuration."""

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

    assert response.status_code == 403
    assert response.data == {"detail": "Authentication credentials were not provided."}
