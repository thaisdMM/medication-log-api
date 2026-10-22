---
status: accepted
date: 2026-08-24
decision-makers: Thaís
---

# Disease list in the database, not in code

## Context and Problem Statement

An account marks its diseases from a closed list. Where that list lives is a
structural choice, not a choice of its contents.

## Considered Options

* A table in the database.
* A constant written in the code.

## Decision Outcome

Chosen option: **a table in the database**. The link between account and
disease is many-to-many.

### Consequences

* Only the admin adds diseases, through Django's admin panel. An account
  chooses from the list and never adds to it.
* How many diseases the list holds is populating the database, not design.

## More Information

Archive address: ESTADO_CORRENTE §5.2, §5.3.
