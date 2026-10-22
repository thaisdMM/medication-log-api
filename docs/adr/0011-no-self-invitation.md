---
status: accepted
date: 2026-08-25
decision-makers: Thaís
---

# An account cannot invite itself

## Context and Problem Statement

The one-row-per-pair constraint (ADR 0010) accepts a sharing whose inviter and
invitee are the same account. With such a sharing accepted, the account would
reach its own data by two paths: as owner, unrestricted, and as guest, limited
by the sharing's scope — two answers to the same permission question.

## Considered Options

* Allow it.
* Refuse it in Python validation only.
* Refuse it in Python validation and declare the refusal in the database.

## Decision Outcome

Chosen option: **declare the refusal in the database**, not only in Python
validation. It is the same class of guarantee as the duplicate constraint
(ADR 0008).

The project is for personal use: an account already reaches its own data, and
sharing it with itself has no purpose.

## More Information

Archive address: ESTADO_CORRENTE §6.10.
