---
status: accepted
date: 2026-10-22
decision-makers: Thaís
---

# Fixed token expiry, counted from login

## Context and Problem Statement

ADR 0007 sets the token lifetime from the login. knox can also renew a token's
expiry each time it is used (`AUTO_REFRESH`), which ADR 0007 did not consider.

## Considered Options

* **Fixed expiry.** The token stops working once the lifetime set in ADR 0007
  has passed since the login, however much it is used.
* **Sliding expiry.** Each use pushes the expiry forward.

## Decision Outcome

Chosen option: **fixed expiry**, because the project prioritises delivery time
and simplicity, and sliding expiry would add another rule and more tests.

### Confirmation

A test proves that using a token does not move its expiry.
