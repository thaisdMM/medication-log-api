---
status: accepted
date: 2026-08-24
decision-makers: Thaís
---

# Custom user model before the first migration

## Context and Problem Statement

An account is identified by its email address, not by a username
(`docs/domain-model.md`). Django's built-in user model identifies an account by
username, and replacing the user model after data exists is one of the most
destructive migrations in Django.

## Considered Options

* Django's built-in user model.
* A user model of the project's own.

## Decision Outcome

Chosen option: **a user model of the project's own**, inheriting from
`AbstractBaseUser` and `BaseUserManager`, with `AUTH_USER_MODEL` configured
before the first migration.

Authenticating by email address requires substituting the user model — it is
the case Django's documentation names for overriding the default. And
`AUTH_USER_MODEL` is configured before the first migration because changing it
afterwards, with data already in the database, is expensive.

## More Information

Archive address: ESTADO_CORRENTE §12.1, with §12.2 for authentication by email.
