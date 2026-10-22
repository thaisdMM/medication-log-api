---
status: accepted
date: 2026-08-24
decision-makers: Thaís
---

# Email to console in every environment, production included

## Context and Problem Statement

Creating an invitation asks for an email notice. Email is not the project's
external integration — that is Telegram (ADR 0012) — and real delivery in
production would make it a second one.

## Considered Options

* A real email provider in production.
* The console backend in production, as in local development.

## Decision Outcome

Chosen option: **the console in every environment, production included**.
Nobody receives email.

Sending sits behind an abstraction, with the backend chosen by an
environment variable; the code does not know the provider.

| Environment | Backend |
|---|---|
| tests | in-memory — a test that really sends is slow and unstable |
| local development | console |
| production | console |

### Consequences

* The invitation works identically with no provider configured.
* The README declares that no email is delivered.
* If email ever sends for real in production, the project has two external
  integrations, and the one-integration constraint must be revoked explicitly
  first (non-goals item 4).

## More Information

Archive address: ESTADO_CORRENTE §8, §6.7.
