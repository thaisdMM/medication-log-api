# Slice 2, task 2.9 — done

# Account deletion

- `src/users/views.py`: `AccountDeletionView` checks the password through
  `AccountDeletionSerializer`, then deletes the account behind the token
- `src/users/urls.py`: `POST /api/users/me/delete/`
- `src/medications/models.py`: the owner foreign key changes from `PROTECT` to
  `CASCADE`; migration `0002_alter_medication_owner` runs no SQL. This reverses
  the earlier decision that an account with medications cannot be deleted
- The account's tokens leave with it, through knox's own `CASCADE`
- `docs/domain-model.md`: deleting an account deletes everything it owns
- Each new test seen failing against a deliberate break
- `uv run pytest` — 125 passed. Total coverage 97%. `ruff`, `mypy` and
  `pre-commit` pass
- Pull request merged with every CI check passing; Render deployed it
  automatically
- Production, from outside, with `curl`, on an account created for the check:
  - `POST /api/users/me/delete/` without a token — `401`
  - Wrong password — `400` with `WRONG_PASSWORD_MESSAGE`; missing password —
    `400`; the medication still listed afterwards
  - Right password — `204`; the old token on `GET /api/users/me/` — `401`
  - The same email signs up again — `201`, with no medications
  - The second account deleted the same way; a login afterwards — `400`
  - `GET /api/schema/` lists the route with the password and a `204`

**Deviations from the task text:** none.

**What this locks in for the rest of the project:** every table that belongs to
an account uses `CASCADE` on its account column.

**Carried into later tasks:**

* The interactive documentation shows the docstring `Args` and `Raises`
  sections of the deletion view as its public description
* A limit on password attempts, kept for a later release
* With `CASCADE` on the account, a `PROTECT` from the usage period to the
  medication would make account deletion fail; decided with the usage period
  model
