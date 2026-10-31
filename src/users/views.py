"""Views for the user account."""

from http import HTTPStatus

from drf_spectacular.utils import extend_schema, extend_schema_view
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutAllView as KnoxLogoutAllView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from users.models import User
from users.serializers import (
    CurrentUserSerializer,
    LoginResponseSerializer,
    LoginSerializer,
    UserRegistrationSerializer,
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

    @extend_schema(request=LoginSerializer, responses=LoginResponseSerializer)
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
    post=extend_schema(request=None, responses={HTTPStatus.NO_CONTENT: None}),
)
class LogoutView(KnoxLogoutView):  # type: ignore[misc]
    """Delete the token used in the request, so it stops working at once."""


@extend_schema_view(
    post=extend_schema(request=None, responses={HTTPStatus.NO_CONTENT: None}),
)
class LogoutAllView(KnoxLogoutAllView):  # type: ignore[misc]
    """Delete every token of the account, so none of them works any more."""
