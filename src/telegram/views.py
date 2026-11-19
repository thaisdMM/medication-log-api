"""Views for the Telegram bot."""

from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram.permissions import HasTelegramWebhookSecret


@extend_schema(exclude=True)
class TelegramWebhookView(APIView):
    """Receive the updates Telegram delivers to the bot.

    Attributes:
        authentication_classes: Empty, because Telegram sends no account token.
        permission_classes: Only requests carrying the webhook secret get in.
    """

    authentication_classes = ()
    permission_classes = (HasTelegramWebhookSecret,)

    def post(self, request: Request) -> Response:
        """Accept an update without replying to it.

        Args:
            request: The update Telegram delivers.

        Returns:
            Response: 200 with an empty body.
        """
        return Response()
