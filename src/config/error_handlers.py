"""JSON answers for the errors raised outside the API views."""

from http import HTTPStatus

from django.http import HttpRequest, JsonResponse

BAD_REQUEST_MESSAGE = "Bad request."
PERMISSION_DENIED_MESSAGE = "You do not have permission to perform this action."
NOT_FOUND_MESSAGE = "Not found."
SERVER_ERROR_MESSAGE = "A server error occurred."


class JsonErrorHandler:
    """Answer an error raised outside the API views with a JSON message.

    Attributes:
        status: The HTTP status of the response.
        message: The message sent under detail.
    """

    def __init__(self, status: HTTPStatus, message: str) -> None:
        """Keep the status and the message that every response carries.

        Args:
            status: The HTTP status of the response.
            message: The message sent under detail.
        """
        self.status = status
        self.message = message

    def __call__(
        self, request: HttpRequest, exception: Exception | None = None
    ) -> JsonResponse:
        """Build the JSON response for the error.

        Args:
            request: The request that raised the error. Unused, required by Django.
            exception: The error raised, when Django passes one. Unused, required
                by Django.

        Returns:
            JsonResponse: The status, with the message under detail as the body.
        """
        return JsonResponse({"detail": self.message}, status=self.status)
