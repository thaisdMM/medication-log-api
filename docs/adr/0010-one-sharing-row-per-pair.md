---
status: accepted
date: 2026-08-24
decision-makers: Thaís
---

# One sharing row per pair of accounts

## Context and Problem Statement

A sharing links the account that invites to the account that is invited. Two
integrity questions were open: can more than one invitation exist between the
same two accounts, and can a declined invitation be remade?

## Considered Options

* Several sharing rows per pair of accounts.
* At most one sharing row per pair, guaranteed by a uniqueness constraint.

## Decision Outcome

Chosen option: **at most one row per pair** (inviter, invitee), guaranteed by a
uniqueness constraint, because it answers both questions with no further rule
written:

* A pending invitation cannot be resent: the row already exists.
* A declined invitation can be remade: the same row returns to pending.
* Different pairs are independent: Pedro→Maria and João→Maria coexist.

### Consequences

* The constraint does not stop an account from inviting itself — the pair of
  one account twice is as unique as any other. ADR 0011 covers it.
* How often a declined invitation may be remade is not limited (non-goals
  item 8).

## More Information

Archive address: ESTADO_CORRENTE §6 (23/08 open questions), §6.2.
