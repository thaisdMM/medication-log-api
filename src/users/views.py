"""Views for the user account."""

from http import HTTPStatus

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutAllView as KnoxLogoutAllView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from config.schema import MISSING_TOKEN
from users.models import User
from users.serializers import (
    AccountDeletionSerializer,
    CurrentUserSerializer,
    LoginResponseSerializer,
    LoginSerializer,
    UserRegistrationSerializer,
)

INVALID_SIGN_UP = OpenApiResponse(
    OpenApiTypes.OBJECT,
    description="Each refused field with its messages, an email in use included.",
)
INVALID_LOGIN = OpenApiResponse(
    OpenApiTypes.OBJECT,
    description="Refused fields by name; wrong credentials under non_field_errors.",
)
INVALID_PASSWORD = OpenApiResponse(
    OpenApiTypes.OBJECT,
    description="The password is missing or does not match the account.",
)


@extend_schema_view(
    post=extend_schema(
        summary="Create an account",
        responses={
            HTTPStatus.CREATED: UserRegistrationSerializer,
            HTTPStatus.BAD_REQUEST: INVALID_SIGN_UP,
        },
    ),
)
class UserRegistrationView(generics.CreateAPIView[User]):
    """Create an account from sign-up data, open to anonymous requests.

    Attributes:
        authentication_classes: Empty, so a stale or invalid token sent along
            with a sign-up does not turn it into a 401.
        permission_classes: Public, overriding the project's closed default.
    """

    serializer_class = UserRegistrationSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)


@extend_schema_view(
    get=extend_schema(
        summary="Return the current account",
        responses={
            HTTPStatus.OK: CurrentUserSerializer,
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
        },
    ),
)
class CurrentUserView(generics.RetrieveAPIView[User]):
    """Return the account behind the token in use."""

    serializer_class = CurrentUserSerializer

    def get_object(self) -> User:
        """Return the authenticated account instead of looking one up by URL.

        Returns:
            User: The account the token belongs to.
        """
        user = self.request.user
        assert isinstance(user, User)
        return user


class LoginView(KnoxLoginView):  # type: ignore[misc]
    """Issue a token in exchange for an email and password.

    Knox's own view expects request.user to be authenticated already; here the
    credentials are checked by LoginSerializer instead, and no Django session
    is created.

    Attributes:
        authentication_classes: Empty, so a stale or invalid token sent along
            with a login does not turn it into a 401.
        permission_classes: Public, overriding the project's closed default.
    """

    authentication_classes = ()
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Log in and get a token",
        request=LoginSerializer,
        responses={
            HTTPStatus.OK: LoginResponseSerializer,
            HTTPStatus.BAD_REQUEST: INVALID_LOGIN,
        },
    )
    def post(self, request: Request, format: str | None = None) -> Response:
        """Validate the credentials, then let knox create the token.

        Args:
            request: The incoming API request, with email and password.
            format: Format suffix from the URL, if any.

        Returns:
            Response: 200 with the token and its expiry.

        Raises:
            ValidationError: When the credentials do not match an active account.
        """
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        request.user = serializer.validated_data["user"]
        response: Response = super().post(request, format=format)
        return response


@extend_schema_view(
    post=extend_schema(
        summary="Log out this token",
        request=None,
        responses={
            HTTPStatus.NO_CONTENT: None,
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
        },
    ),
)
class LogoutView(KnoxLogoutView):  # type: ignore[misc]
    """Delete the token used in the request, so it stops working at once."""


@extend_schema_view(
    post=extend_schema(
        summary="Log out every token",
        request=None,
        responses={
            HTTPStatus.NO_CONTENT: None,
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
        },
    ),
)
class LogoutAllView(KnoxLogoutAllView):  # type: ignore[misc]
    """Delete every token of the account, so none of them works any more."""


@method_decorator(sensitive_post_parameters("password"), name="dispatch")
class AccountDeletionView(generics.GenericAPIView[User]):
    """Delete the account behind the token, once its password is confirmed."""

    serializer_class = AccountDeletionSerializer

    @extend_schema(
        summary="Delete the account",
        responses={
            HTTPStatus.NO_CONTENT: None,
            HTTPStatus.BAD_REQUEST: INVALID_PASSWORD,
            HTTPStatus.UNAUTHORIZED: MISSING_TOKEN,
        },
    )
    def post(self, request: Request) -> Response:
        """Check the password, then delete the account and everything it owns.

        Args:
            request: The incoming API request, with the account's password.

        Returns:
            Response: 204 with no body.

        Raises:
            ValidationError: When the password is missing or does not match.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        assert isinstance(user, User)
        user.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
