---
status: accepted
date: 2026-11-23
decision-makers: Thaís
---

# The web interface keeps the token in sessionStorage

## Context and Problem Statement

The web interface (ADR 0022) sends the account's token (ADR 0007) with every
request, so it keeps the token in the browser. Wherever JavaScript can read
it, a script injected into the page (XSS) can read it too.

## Considered Options

* localStorage
* sessionStorage
* Page memory

## Decision Outcome

Chosen option: "sessionStorage", because the token survives a page reload and
is deleted when the tab closes. In localStorage it stays on the computer until
it expires (ADR 0018); in page memory it is lost on every reload and the
person signs in again. The public environment holds fictitious data only
(non-goals item 19).

An HttpOnly cookie, which JavaScript cannot read, is left out: it would change
the API's authentication (ADR 0007).
