---
status: accepted
date: 2026-08-24
decision-makers: Thaís
---

# Sharing with scope, not all-or-nothing

## Context and Problem Statement

A data owner invites another account to see their data. The owner chooses what
is shared: only medications, only diseases, or both.

## Considered Options

* **Invitation with scope.** Permission stops being a filter and becomes a real
  business rule. Every query checks two questions, and the tests multiply:
  owner, guest with access, guest without access, stranger.
* **All-or-nothing invitation.** Simpler and delivered sooner, but it loses the
  most interesting permission case.

## Decision Outcome

Chosen option: **invitation with scope**. The invitation carries medications,
diseases, or both; "nothing" does not exist — with nothing to share there is no
invitation.

### Consequences

* Permission asks two questions: does the requester have access, and to what.
* The scope is frozen while the sharing exists (non-goals item 7).

## More Information

Archive address: ESTADO_CORRENTE §6 (23/08, superseded), §6.3.
