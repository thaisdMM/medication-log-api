"""URL configuration for the medication endpoints."""

from django.urls import path

from medications.views import MedicationDetailView, MedicationListCreateView

urlpatterns = [
    path("medications/", MedicationListCreateView.as_view(), name="medication-list"),
    path(
        "medications/<int:pk>/",
        MedicationDetailView.as_view(),
        name="medication-detail",
    ),
]
