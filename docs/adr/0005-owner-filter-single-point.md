---
status: accepted
date: 2026-08-26
decision-makers: Thaís
---

# Owner filter in a single point of the code

## Context and Problem Statement

Every query an endpoint makes is restricted to the account that made the
request. That restriction can be written by hand in each place that queries, or
it can live in a single point every query passes through.

## Considered Options

* The filter written by hand in each place that queries.
* The filter in a single point every query passes through, with each endpoint
  declaring only its path to the owner.

## Decision Outcome

Chosen option: **the filter in a single point**. Every query of an endpoint is
already filtered by the requesting account, and nobody writes the filter by
hand; each endpoint declares only what its path to the owner is — the usage
period's path is the one ADR 0004 decides.

An endpoint written without that declaration fails on its first call, with a
message saying what is missing. Written by hand, a forgotten filter produced an
endpoint that worked and leaked another account's data in silence, passing the
tests written with a single account.

It is the same reasoning as the duplicate constraint (ADR 0007): instead of
trusting that nobody will get it wrong, the mistake is made impossible to go
unnoticed.

## More Information

Archive address: ESTADO_CORRENTE §17.2.
