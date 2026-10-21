"""Views for the user account."""

from knox.views import LoginView as KnoxLoginView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from users.models import User
from users.serializers import LoginSerializer, UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView[User]):
    """Create an account from sign-up data, open to anonymous requests.

    Attributes:
        authentication_classes: Empty, so a stale or invalid token sent along
            with a sign-up does not turn it into a 401
        permission_classes: Public, overriding the project's closed default
    """

    serializer_class = UserRegistrationSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)


class LoginView(KnoxLoginView):  # type: ignore[misc]
    """Issue a token in exchange for an email and password.

    Knox's own view expects request.user to be authenticated already; here the
    credentials are checked by LoginSerializer instead, and no Django session
    is created.

    Attributes:
        authentication_classes: Empty, so a stale or invalid token sent along
            with a login does not turn it into a 401
        permission_classes: Public, overriding the project's closed default
    """

    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request: Request, format: str | None = None) -> Response:
        """Validate the credentials, then let knox create the token.

        Args:
            request: The incoming API request, with email and password
            format: Format suffix from the URL, if any

        Returns:
            Response: 200 with the token and its expiry

        Raises:
            ValidationError: when the credentials do not match an active account
        """
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        request.user = serializer.validated_data["user"]
        response: Response = super().post(request, format=format)
        return response
