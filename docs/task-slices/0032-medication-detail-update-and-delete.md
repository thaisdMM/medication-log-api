# Slice 2, task 2.6 — done

# Medication detail, update and delete

- `src/medications/views.py`: `MedicationDetailView` retrieves, edits and
  deletes a medication of the requesting account, through `OwnerFilterMixin`
  with `owner_path = "owner"`
- `src/medications/urls.py`: `/api/medications/<id>/`
- A `PUT` that omits an optional field keeps its stored value; the question
  left open in `0030` is closed
- Delete removes the row
- `src/medications/tests/test_views.py`: each test seen failing against a
  deliberate break
- `uv run pytest` — 118 passed. Total coverage 97%, `medications/views.py` at
  100%. `ruff`, `mypy` and `pre-commit` pass
- Pull request merged with every CI check passing; Render deployed it
  automatically
- Production, from outside, with `curl`:
  - `GET /healthz/` — `200`, `{"status": "ok", "checks": {"database": "ok"}}`
  - `GET /api/docs/` — `200`
  - `GET /api/medications/<id>/` without a token — `401`
  - `GET` by the owner — `200`, without the owner
  - `PATCH {"state": "suspended"}`, then `{"state": "in_use"}` — `200` each
  - `PUT` with only the name — `200`, concentration and form kept
  - `PATCH` into another medication of the account — `400` with
    `DUPLICATE_MEDICATION_MESSAGE`
  - Another account: `GET`, `PUT`, `PATCH` and `DELETE` — `404`; the medication
    unchanged afterwards
  - `DELETE` by the owner — `204`; a `GET` afterwards — `404`

**Deviations from the task text:** none.

**What this locks in for the rest of the project:** an account reads, edits and
deletes only its own medications; another account's medication answers as
missing.

**Carried into later tasks:**

* What deleting a medication does to its usage periods is decided with the
  usage period model, kept for a later release
* An account cannot be deleted through the API — decided before the
  interactive documentation
