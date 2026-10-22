---
status: accepted
date: 2026-10-22
decision-makers: Thaís
---

# Responses carry only the personal data the endpoint needs

## Context and Problem Statement

The account's own endpoint (`GET /api/users/me/`) was planned to return the
account's id, email and name. Every endpoint that returns account data faces
the same question: which personal data goes into the response.

## Considered Options

* **Return id, email and name.** Rejected: the email is personal data the
  project prefers not to expose.
* **Decide per endpoint, with no project rule.** Rejected: the same question
  returns with every new endpoint.
* **A project rule: the account is identified by its id; the name appears only
  when the endpoint's function needs it; the email never appears.**

## Decision Outcome

Chosen option: **the project rule**, because the project avoids exposing
personal data it does not need: LGPD art. 6, III (necessity: processing
limited to the minimum needed for its purposes) and OWASP API Security 2023,
API3 ("Keep returned data structures to the bare minimum").

An endpoint that needs the email in a response does so only through an ADR of
its own that justifies the exception.
