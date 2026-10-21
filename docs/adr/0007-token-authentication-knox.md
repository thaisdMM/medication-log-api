---
status: accepted
date: 2026-10-21
decision-makers: Thaís
---

# Token authentication with django-rest-knox

## Context and Problem Statement

The API authenticates every request with a token (ADR 0002), and the library
that provides it was left undecided.

## Considered Options

* **djangorestframework-simplejwt 5.5.1.** No release since 5.5.1
  (2025-07-21); declares Django up to 5.2 and Python up to 3.13; a known fix —
  refreshing the token of a deleted user returns 500 — is on master but
  unreleased.
* **django-rest-knox 5.1.0.** Released 2026-07-12. Tokens expire, are stored
  as SHA-512 digests rather than in plaintext, and are deleted on the server at
  logout, so they stop working at once.
* **DRF's built-in `authtoken`.** Tokens never expire, each user has a single
  token, and the key is stored in plaintext.
* **An implementation of our own on PyJWT.** The project would own
  authentication security code: account enumeration, revocation, inactive
  users.

## Decision Outcome

Chosen option: **django-rest-knox**, with tokens that expire 10 hours after
login, because simplejwt has gone without a release since 2025-07-21 while
knox is maintained, and knox's tokens expire, are stored hashed and are deleted
at logout.

## More Information

Sources, checked 2026-10-21: the PyPI JSON of both libraries; the knox GitHub
release 5.1.0 (2026-07-12) and its `docs/settings.md`; the DRF authentication
guide; the simplejwt repository (last release v5.5.1, commits on master up to
2026-05).
