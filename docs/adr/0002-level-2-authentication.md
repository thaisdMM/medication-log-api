---
status: accepted
date: 2026-08-21
decision-makers: Thaís
---

# Level-2 authentication: multiple users with isolated data

## Context and Problem Statement

How many people the system serves had to be settled before any model existed:
one person, or many, each reaching only their own data.

## Considered Options

* **Level 1 — a single user.** The system serves one person and nobody else
  signs up. Solved with a simple secret key or with the Django admin panel.
  Low cost.
* **Level 2 — multiple users with isolated data.** Anyone signs up, logs in,
  and sees only what is theirs. Significantly higher cost.

## Decision Outcome

Chosen option: **Level 2 — multiple users with isolated data**.

Isolation per account is the system's central business rule, not a checklist
item: it is the reason the system exists, rather than a filter applied to a
query.

### Consequences

The cost of level 2 over level 1 was accepted when it was chosen. It is not
authentication itself — Django ships a user system — but the three things that
come with it:

* **Token authentication on the API.** A REST API carries no browser session,
  so the client sends a token on every request. Which library is not decided
  (`docs/open-questions.md`).
* **Owner filtering in every query.** Forgetting it in a single view leaks one
  account's data to another (ADR 0005).
* **Doubled tests.** Every endpoint needs one test as the data owner and one as
  an account with no relation to it (ADR 0006).

## More Information

Archive address: ETAPA2 B1, with the option table of the block B preamble.

Date: Phase 1, decision D6. 2026-08-21 is the Phase 1 date the archive records.
