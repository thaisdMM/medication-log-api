"""Mixins shared by the views of every app."""

from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from rest_framework.generics import GenericAPIView

MISSING_OWNER_PATH_MESSAGE = (
    "{view} must declare owner_path, the path from its model to the owning account."
)


class OwnerFilterMixin(GenericAPIView[Any]):
    """Restrict every query of a view to the account that made the request.

    Attributes:
        owner_path: Lookup path from the view's model to the owning account.
    """

    owner_path: str | None = None

    def get_queryset(self) -> QuerySet[Any]:
        """Return the view's rows that belong to the requesting account.

        Returns:
            QuerySet: The view's queryset filtered by the requesting account.

        Raises:
            ImproperlyConfigured: When the view declares no owner path.
        """
        if self.owner_path is None:
            raise ImproperlyConfigured(
                MISSING_OWNER_PATH_MESSAGE.format(view=type(self).__name__)
            )
        return super().get_queryset().filter(**{self.owner_path: self.request.user})
