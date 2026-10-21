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
| 1.4 | `knox` and the login endpoint | `POST /api/auth/login/` exchanges an email and password for a token that expires 10 hours later; knox's own migrations create its token table. Branch and pull request | knox becomes the authentication class for every endpoint that follows |
| 1.5 | "My account" endpoint | `GET /api/users/me/` returns the id, email and name behind the token — 200 with one, 401 without | without it, nothing in slice 1 proves a token authenticates anything |
| 1.6 | Logout through knox | `POST /api/auth/logout/` deletes the token in use and `POST /api/auth/logoutall/` deletes every token of the account; a request with a deleted token is refused. Branch and pull request | a logout that does not delete the token leaves it valid until it expires |
| 1.7 | Interactive API documentation | `drf-spectacular` serves the schema and a public Swagger UI page listing every slice 1 endpoint, with token authorization. Branch and pull request | the page inherits 1.1's closed default unless explicitly public — the link gives a 401 |
| 1.8 | Slice proven in production | register, login, me and logout run against the public address; the slice closes in its record | without it, "slice 1 is live" is opinion |

## Decisions

* Token: `django-rest-knox` (ADR 0007).
* Logout through knox's logout and logout-all views. The token is deleted on
  the server, so it stops working at once — no blacklist.
* The whole email is stored in lowercase: one account per address, whatever
  the case it is typed in, and login and the slice 5 invitations compare the
  same form.
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
