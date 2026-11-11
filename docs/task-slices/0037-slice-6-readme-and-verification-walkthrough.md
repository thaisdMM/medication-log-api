# Slice 6 — done

# README and verification walkthrough

- No code changed: the suite is the one in `0035`
- The README holds two walkthroughs with the same steps:
  - "Trying it from the terminal", with `curl`: create an account, log in,
    see the account, record, list, get, edit with `PUT`, suspend with
    `PATCH`, filter by state, record the same medication again, create a
    second account, ask for the first account's medication, delete the
    medication, log out, delete both accounts
  - "Using the interactive documentation": the same step names, each with its
    operation on the Swagger UI page and where to set the token
- The `curl` block moved out of "Endpoints available today" into the terminal
  walkthrough; the Status table moves the walkthrough to done and the
  Telegram bot to next
- Production, from outside, with the README's commands in order, on two new
  accounts. Every response below is the one the API gave; ids and tokens are
  left out:
  - Sign-up — `201`, only the id; login — `200`, an expiry and a token;
    `GET /api/users/me/` — `200`, the id and the name
  - Record — `201`, `state` `in_use`; list and get — `200`
  - `PUT` with a new concentration — `200`; `PATCH {"state": "suspended"}` —
    `200`; `?state=suspended` — `200`, only that medication
  - The same medication again — `400`,
    `{"non_field_errors": [DUPLICATE_MEDICATION_MESSAGE]}`
  - The second account asks for the first account's medication — `404`, the
    same body as an id that does not exist
  - The first account deletes the medication — `204`; getting it — `404`
  - Logout of the second account — `204`; its old token — `401`
  - Both accounts deleted with their passwords — `204` each, the second after
    a new login; a login with either email afterwards — `400`
- The whole slice 2 was already proven in production in `0036`; this run
  proves the README's commands as written

**Deviations from the task text:** the roadmap asks for the sequence that
ends in another account's `404`. The walkthrough also edits and deletes a
medication, so every medication operation has an example, and ends by
deleting what it created.

**What this locks in for the rest of the project:** whoever gets the link can
run the whole flow alone, from the terminal or the Swagger UI page, and reach
the project's decisions and non-goals from the README. Slice 6 is closed.

**Carried into later tasks:**

* A path with no route, such as `/api/medications//`, still answers with
  Django's default HTML `404` page; JSON handlers for `404` and `500` are a
  follow-up in the first release map
* Expired tokens stay in the token table until their account authenticates
  again, when knox deletes them; a command that deletes them all is a possible
  later improvement
