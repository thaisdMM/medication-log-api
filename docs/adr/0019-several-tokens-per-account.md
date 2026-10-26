---
status: accepted
date: 2026-10-26
decision-makers: Thaís
---

# Several valid tokens per account, one per login

## Context and Problem Statement

knox creates a new token at every login, and each token stays valid until it
expires.

## Considered Options

* **Several tokens, one per login.** knox's default: each device signs in
  with its own token; logout ends that token only, and logout-all ends every
  token of the account.
* **A limit per account (`TOKEN_LIMIT_PER_USER`).** Once the account holds
  that many valid tokens, knox refuses the next login; it does not free an
  older token.
* **A new login deletes the account's previous tokens.** One token per
  account at a time. knox has no setting for this, so the project would own
  that authentication code.

## Decision Outcome

Chosen option: **several tokens, one per login**, so a person can sign in
from a phone and other devices at once, each with its own token, and end one
device's access without ending the others. Every token still expires (ADR
0007, ADR 0018), so none stays valid for ever. It also keeps the project
simple and focused on delivery.

### Confirmation

`test_logout_keeps_the_other_tokens_of_the_account_working` proves that
ending one token leaves the account's other tokens working.
