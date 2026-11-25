"""Tests for which browser origins may call the API."""

import pytest
from django.test import Client
from django.urls import reverse

PREVIEW_ORIGIN = "https://feat-sign-in-medication-log-web.thaisdmm.workers.dev"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "origin",
    [
        PREVIEW_ORIGIN,
        "https://1a2b3c4d-medication-log-web.thaisdmm.workers.dev",
    ],
    ids=["branch-preview", "version-preview"],
)
def test_preview_address_of_the_interface_may_call_the_api(
    client: Client, origin: str
) -> None:
    """A preview address of the interface gets its origin allowed back."""
    response = client.get(reverse("healthz"), HTTP_ORIGIN=origin)

    assert response["Access-Control-Allow-Origin"] == origin


@pytest.mark.django_db
@pytest.mark.parametrize(
    "origin",
    [
        "https://example.com",
        "http://feat-sign-in-medication-log-web.thaisdmm.workers.dev",
        "https://feat-sign-in-medication-log-web.thaisdmm.workers.dev.example.com",
        "https://feat-sign-in-medication-log-web.another-account.workers.dev",
        "https://example.com.feat-sign-in-medication-log-web.thaisdmm.workers.dev",
    ],
    ids=[
        "another-site",
        "plain-http",
        "longer-domain",
        "another-account",
        "dotted-prefix",
    ],
)
def test_address_outside_the_interface_may_not_call_the_api(
    client: Client, origin: str
) -> None:
    """An origin that only looks like the interface gets no CORS header."""
    response = client.get(reverse("healthz"), HTTP_ORIGIN=origin)

    assert "Access-Control-Allow-Origin" not in response


def test_preflight_before_an_api_call_allows_the_interface(client: Client) -> None:
    """The browser's check before an API call gets the interface's origin allowed."""
    response = client.options(
        reverse("user-me"),
        HTTP_ORIGIN=PREVIEW_ORIGIN,
        HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        HTTP_ACCESS_CONTROL_REQUEST_HEADERS="authorization",
    )

    assert response["Access-Control-Allow-Origin"] == PREVIEW_ORIGIN


def test_path_the_interface_does_not_use_gets_no_cors_header(client: Client) -> None:
    """The admin site answers an allowed origin without a CORS header."""
    response = client.get(reverse("admin:login"), HTTP_ORIGIN=PREVIEW_ORIGIN)

    assert "Access-Control-Allow-Origin" not in response
