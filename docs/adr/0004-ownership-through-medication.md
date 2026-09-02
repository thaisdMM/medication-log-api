---
status: accepted
date: 2026-08-26
decision-makers: Thaís
---

# Ownership discovered through the medication, no owner column

## Context and Problem Statement

A usage period points at the medication it records. The medication carries the
account it belongs to. Whether the usage period should carry that account as
well had to be settled.

## Considered Options

* **An owner column on the usage period**, linking the row to its account
  directly.
* **No owner column**, with ownership discovered by crossing to the medication.

## Decision Outcome

Chosen option: **no owner column**.

The account is already recorded on the medication, so a column on the usage
period would hold the same information twice, and nothing in the database would
stop the two from disagreeing: a usage period could be saved with one account
in its column and another account's medication beside it. The permission rule
would then have two answers to *whose data is this*.

Derivable information is not stored. It is the same reasoning that refused an
account-type flag (`docs/domain-model.md`).

### Consequences

* Ownership is one step away: every query on a usage period crosses to the
  medication to find out whose it is. ADR 0005 puts that path in a single
  point.
* No database constraint can guarantee that the medication a usage period
  points at belongs to the account creating it. The foreign key makes the link
  mandatory, not correct — that check is written by hand in input validation
  (`docs/api-behaviour.md`).

## More Information

Archive address: ESTADO_CORRENTE §17.1.
