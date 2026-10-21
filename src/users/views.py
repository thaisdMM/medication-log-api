"""Views for the user account."""

from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView[User]):
    """Create an account from sign-up data, open to anonymous requests.

    Attributes:
        permission_classes: Public, overriding the project's closed default
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
