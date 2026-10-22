---
status: accepted
date: 2026-08-24
decision-makers: Thaís
---

# Interactive API documentation published

## Context and Problem Statement

The project has no user interface (non-goals item 1): it is a REST API and
nothing else. An API without a screen still has to be usable by whoever looks
at it — a recruiter or anyone trying the project — without a frontend.

## Decision Outcome

The project publishes **interactive API documentation**. The published address
opens a single page listing every endpoint, with each one's fields and possible
responses, and requests can be sent from it.

The page is served by the Django already live: no new service, no permanent
process, no conflict with free hosting (ADR 0001).

### Consequences

* Anyone can exercise the backend from the browser, with no client of their
  own.
* The README adds a short verification walkthrough (two accounts, the second
  gets 404 on the first one's medication) on top of this page.

## More Information

Archive address: ESTADO_CORRENTE §14.1, §14.2, §16.
