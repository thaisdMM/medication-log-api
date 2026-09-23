"""Temporary test that fails on purpose to turn the tests job red."""

import pytest


def test_fails_on_purpose_to_prove_the_merge_block() -> None:
    """Fails on purpose so the pull request shows the tests check red."""
    pytest.fail("Fails on purpose: proves the rule blocks a red tests check")
