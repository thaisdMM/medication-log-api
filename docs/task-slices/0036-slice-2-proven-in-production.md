# Slice 2, task 2.8 — done

# Slice 2 proven in production

- No code changed: the suite is the one in `0035`, 170 tests
- Production, from outside, with `curl`, on two new accounts, A and B. Every
  response below is the one the API gave; ids and tokens are left out:
  - `GET /healthz/` — `200`, `{"status": "ok", "checks": {"database": "ok"}}`
  - `POST /api/users/` for A and for B — `201`, only the id
  - `POST /api/auth/login/` for A and for B — `200`, an expiry and a token
  - A creates a medication — `201`, `state` `in_use` without being sent, no
    owner in the body; a second one sent with `"500.000"` comes back `"500"`
  - A lists — `200`, `amoxicilina` before `Losartana`, so the order ignores case
  - A retrieves each one — `200`; an id that does not exist — `404`,
    `{"detail":"No Medication matches the given query."}`
  - `PUT` with a new concentration and no `state` — `200`
  - `PATCH {"state": "suspended"}` — `200`; `PATCH {"state": "BANANA"}` — `400`,
    `{"state":["\"BANANA\" is not a valid choice."]}`, and the medication is
    unchanged afterwards
  - `?state=suspended` lists only the suspended one and `?state=in_use` only
    the other; `?state=paused` — `400`
  - `PATCH {"state": "in_use"}` — `200`
  - The same medication again, with the name in capitals and spaces around it —
    `400`, `{"non_field_errors": [DUPLICATE_MEDICATION_MESSAGE]}`; a form
    written `TABLET` and a unit written `MG` — `400` each, on its own field
  - B records the same medication A has — `201`; B lists — only its own
  - B retrieves, patches and deletes A's medication — `404` each, the same body
    as an id that does not exist; A's medication is unchanged afterwards
  - A list without a token — `401`,
    `{"detail":"Authentication credentials were not provided."}`
  - A deletes a medication — `204`; retrieving it — `404`; the list holds only
    the other one
  - A deletes the account with the password — `204`; the old token on
    `GET /api/users/me/` — `401`; a login with that email — `400`
  - The same email signs up again — `201` with a new id; a login — `200`; the
    medication list — `[]`; `GET /api/users/me/` — `200`, the id and the name
  - B logs in a second time; both tokens answer `GET /api/users/me/` with
    `200`; `GET /api/medications/` with the second token lists B's medication
  - B records a medication with only a name — `201`, with
    `"concentration_value": null`, `"concentration_unit": ""` and `"form": ""`
  - `POST /api/auth/logout/` with the second token — `204`; that token on
    `GET /api/users/me/` — `401`; the first token — `200`
  - A third login, then `POST /api/auth/logoutall/` with the first token —
    `204`; the first and the third token — `401`
  - A fourth login — `200`; B's medications are all still listed
- The production database, read in the Neon SQL editor with `SELECT` on the
  user, medication and token tables:
  - Before the clean-up: the two accounts, B's two medications and one token
    per account, with the first A account (deleted earlier) and the tokens
    removed by the logouts missing
  - After deleting both accounts with their passwords — `204` each: no row
    left for them in any of the three tables
- On the Swagger UI page, on a new account, with a token set in "Authorize":
  login, several tokens on one account, logout and logout all, and create,
  edit and delete of a medication gave the same results as with `curl`
  - `PATCH {"state": "suspended"}` — `200`; then a `PUT` with the name, a
    concentration of `100.000`, the unit and the form, and no `state` — `200`,
    the concentration returned as `"100"` and the state still `suspended`

**Deviations from the task text:** the task listed create, list, retrieve,
update, delete, the duplicate `400` and another account's `404`. The run also
covered the filter by state, account deletion followed by a new sign-up with
the same email, logout and logout all with several tokens, a database check
and the same flows on the Swagger UI page, so the proof covers the whole
slice and the accounts behind it.

**What this locks in for the rest of the project:** an account records,
changes and deletes its own medications against the public address, never sees
another account's, and cannot hold the same medication twice. Slice 2 is
closed; the next slice builds on it.

**Carried into later tasks:**

* A path with no route, such as `/api/medications//`, answers with Django's
  default HTML `404` page, while an id that does not exist answers with JSON
* Two expired tokens from earlier checks were still in the token table
