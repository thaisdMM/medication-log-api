"""URL configuration for the medication endpoints."""

from django.urls import path

from medications.views import MedicationListCreateView

urlpatterns = [
    path("medications/", MedicationListCreateView.as_view(), name="medication-list"),
]
