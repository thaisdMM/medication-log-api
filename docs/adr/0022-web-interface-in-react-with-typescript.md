---
status: accepted
date: 2026-11-23
decision-makers: Thaís
---

# A web interface in React with TypeScript

## Context and Problem Statement

The project was built as a REST API with no user interface (non-goals item 1),
explored through the interactive API documentation (ADR 0014). With the first
release live, a web interface shows the backend integrated with a frontend.

## Considered Options

* React with TypeScript (Vite)
* Angular with TypeScript
* Vue with TypeScript
* Django templates with HTMX

## Decision Outcome

Chosen option: "React with TypeScript (Vite)", because it is the stack already
used in an earlier project, TypeScript adds static types in the same line as
mypy in strict mode on the backend, and it is a frontend framework, which
Django templates with HTMX are not.

The interface lives in a `frontend/` folder of this repository, not in a
repository of its own, so the project stays in one place and the API's Docker
image is unchanged.

## More Information

Revokes non-goals item 1. Amends ADR 0014: the interactive documentation stays
published, but the project is no longer without a user interface.
