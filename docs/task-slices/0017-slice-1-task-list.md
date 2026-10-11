# Slice 1 — the task list

**Written:** 2026-09-28

The tasks of slice 1, in order, with what each delivers and what breaks if
it goes wrong. Not a step-by-step — each task's step-by-step lives in its
own completion record.

## What the slice delivers

From `0001`: an account signs up, requests a token, and uses it to
authenticate — with the interactive API documentation live from here on.
The slice ends only when this whole flow runs in production.

## Numbering rule

Same as `0002`: tasks are never inserted mid-list or renumbered. A new task
enters inside an existing one, or appended at the end (1.9 onward).

## The list

| # | Task | Delivers | Breaks if wrong |
|---|---|---|---|
| 1.1 | DRF installed and configured | DRF in `INSTALLED_APPS`, with authenticated-only as the default permission; CI green, `/healthz/` still 200 in production. Branch and pull request | an open default leaves any endpoint that forgets its own permission public |
| 1.2 | Registration serializer | validates email, name and password, runs Django's password validators, creates the account through `create_user` — tested without HTTP | `create_user` does not run password validators; if the serializer doesn't, any password is accepted, silently |
| 1.3 | Registration endpoint | `POST /api/users/`, public: 201 on success, 400 naming the problem on a duplicate email or a weak password, never a 500; the password never appears in a response | a public endpoint inside a closed default returns 401 to everyone trying to sign up |
| 1.4 | `simplejwt` and the token endpoints | `POST /api/token/` returns an access and a refresh token; `POST /api/token/refresh/` issues a new access token. Access 15 minutes, refresh 1 day. Branch and pull request | JWT becomes the authentication class for every endpoint that follows |
| 1.5 | "My account" endpoint | `GET /api/users/me/` returns the id, email and name behind the token — 200 with one, 401 without | without it, nothing in slice 1 proves a token authenticates anything |
| 1.6 | Logout through the token blacklist | `POST /api/token/blacklist/` invalidates a refresh token, and refreshing with it afterwards is refused; the blacklist tables are created in production by the migrate-on-start command. Branch and pull request | the app installed without its migration makes login itself fail, not just logout |
| 1.7 | Interactive API documentation | `drf-spectacular` serves the schema and a public Swagger UI page listing every slice 1 endpoint, with token authorization. Branch and pull request | the page inherits 1.1's closed default unless explicitly public — the link gives a 401 |
| 1.8 | Slice proven in production | register, token, me, refresh and logout run against the public address; the slice closes in its record | without it, "slice 1 is live" is opinion |

## Decisions

* Token: `djangorestframework-simplejwt`, verified against this project's
  versions before adoption.
* Logout through the blacklist app. It invalidates refresh tokens only; an
  issued access token stays valid until it expires — 15 minutes.
* Email case is kept as Django normalizes it (domain only): invitations in
  slice 5 must match the email exactly.
* Minimum password length: Django's default, 8.
* Documentation: `drf-spectacular` — DRF's built-in schema generation is
  deprecated in its favour.
* Default permission is authenticated-only; public endpoints declare it.
* A duplicate email on registration is reported as such — a neutral
  response needs real email delivery, a non-goal.
* Sign-in with Google or GitHub stays out of scope (non-goals item 4).

## Carried, not part of this slice

* Converting `/healthz/` to DRF (`0014`).
* Static files in production (`0016`) — slice 4, with the admin panel.
* `docs/definition-of-done.md` (`0015`).
* Logging configuration. ETAPA2 B4 holds meanwhile: no project code
  writes logs.
