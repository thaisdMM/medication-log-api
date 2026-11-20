"""Views for the Telegram bot."""

from http import HTTPStatus

from django.conf import settings
from django.db import transaction
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework.exceptions import APIException, NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from config.schema import MISSING_TOKEN, ErrorDetailSerializer
from telegram.models import TelegramLink, TelegramLinkCode
from telegram.permissions import HasTelegramWebhookSecret
from telegram.serializers import TelegramLinkCodeSerializer, TelegramLinkSerializer
from users.models import User

LINK_NOT_FOUND_MESSAGE = "No Telegram link for this account."
BOT_NOT_CONFIGURED_MESSAGE = "The Telegram bot is not configured."

LINK_NOT_FOUND = OpenApiResponse(
    ErrorDetailSerializer,
    description="The account has no link with the bot.",
    examples=[OpenApiExample("No link", value={"detail": LINK_NOT_FOUND_MESSAGE})],
)
NO_LINK_TO_UNDO = OpenApiResponse(
    ErrorDetailSerializer,
    description="The account had no link; its link codes are deleted all the same.",
    examples=[OpenApiExample("No link", value={"detail": LINK_NOT_FOUND_MESSAGE})],
)
BOT_NOT_CONFIGURED = OpenApiResponse(
    ErrorDetailSerializer,
    description="The bot's user name is not configured, so there is no link to give.",
    examples=[
        OpenApiExample(
            "Bot not configured", value={"detail": BOT_NOT_CONFIGURED_MESSAGE}
        )
    ],
)


class BotNotConfigured(APIException):
    """Raised when the bot's user name, which the deep link needs, is not set."""

    status_code = HTTPStatus.SERVICE_UNAVAILABLE
    default_detail = BOT_NOT_CONFIGURED_MESSAGE


def bot_username() -> str:
    """Return the bot's user name, which the deep link points to.

    Returns:
        str: The user name set in the environment.

    Raises:
        BotNotConfigured: When the bot's user name is not set.
    """
    username: str = settings.TELEGRAM_BOT_USERNAME
    if not username:
        raise BotNotConfigured
    return username


def requesting_account(request: Request) -> User:
    """Return the account behind the token of an authenticated request.

    Args:
        request: An incoming API request that passed authentication.

    Returns:
        User: The account the token belongs to.
    """
    account = request.user
    assert isinstance(account, User)
    return account


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


class TelegramLinkView(APIView):
    """Ask for, read and undo the link between the account and the bot."""

    @extend_schema(
        summary="Ask for a link to the bot",
        request=None,
        responses={
            HTTPStatus.CREATED: TelegramLinkCodeSerializer,
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
            HTTPStatus.SERVICE_UNAVAILABLE: BOT_NOT_CONFIGURED,
        },
    )
    def post(self, request: Request) -> Response:
        """Issue a new link code and return the deep link that carries it.

        Args:
            request: The incoming API request, with no body.

        Returns:
            Response: 201 with the deep link and when its code expires.

        Raises:
            BotNotConfigured: When the bot's user name is not set.
        """
        username = bot_username()
        code, link_code = TelegramLinkCode.objects.issue(requesting_account(request))
        serializer = TelegramLinkCodeSerializer(
            {
                "link": f"https://t.me/{username}?start={code}",
                "expires_at": link_code.expires_at,
            }
        )
        return Response(serializer.data, status=HTTPStatus.CREATED)

    @extend_schema(
        summary="Show the link to the bot",
        responses={
            HTTPStatus.OK: TelegramLinkSerializer,
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
            HTTPStatus.NOT_FOUND: LINK_NOT_FOUND,
        },
    )
    def get(self, request: Request) -> Response:
        """Return when the account was linked to the bot.

        Args:
            request: The incoming API request.

        Returns:
            Response: 200 with the moment the link was made.

        Raises:
            NotFound: When the account has no link.
        """
        try:
            link = TelegramLink.objects.get(account=requesting_account(request))
        except TelegramLink.DoesNotExist as error:
            raise NotFound(LINK_NOT_FOUND_MESSAGE) from error
        return Response(TelegramLinkSerializer(link).data)

    @extend_schema(
        summary="Undo the link to the bot",
        responses={
            HTTPStatus.NO_CONTENT: None,
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
            HTTPStatus.NOT_FOUND: NO_LINK_TO_UNDO,
        },
    )
    def delete(self, request: Request) -> Response:
        """Delete the account's link and every link code it asked for.

        The codes are deleted even when there is no link, so a link asked for
        and not used yet stops working.

        Args:
            request: The incoming API request.

        Returns:
            Response: 204 with no body.

        Raises:
            NotFound: When the account had no link.
        """
        account = requesting_account(request)
        with transaction.atomic():
            TelegramLinkCode.objects.filter(account=account).delete()
            deleted, _ = TelegramLink.objects.filter(account=account).delete()
        if not deleted:
            raise NotFound(LINK_NOT_FOUND_MESSAGE)
        return Response(status=HTTPStatus.NO_CONTENT)
