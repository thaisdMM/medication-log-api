# Slice 2, task 2.2 — done

# Medication model and duplicate constraint

- App `medications` created with `startapp`, registered in `INSTALLED_APPS`.
  `admin.py` and `views.py` removed, since nothing uses them yet; `tests.py`
  replaced by a `tests/` package
- `src/medications/models.py`: `ConcentrationUnit` (four values),
  `MedicationForm` (nine), `MedicationState` (two) and `Medication`
- `Medication`: `owner` (`PROTECT`), `name` (`max_length=255`),
  `concentration_value` (`max_digits=10`, `decimal_places=3`, nullable),
  `concentration_unit` and `form` (`blank=True`, never `NULL`), `state`
  (default `in_use`)
- `unique_medication_per_owner`: owner, `Lower("name")`, concentration value,
  unit and form, with `nulls_distinct=False` and
  `DUPLICATE_MEDICATION_MESSAGE` as its `violation_error_message`
- `__str__` answers the class name and the id, as on the user model: the
  medication name is health data and `__str__` can reach logs
- `src/medications/migrations/0001_initial.py`: one `CreateModel`, previewed
  with `makemigrations --dry-run` before being generated. No existing table
  changes
- `src/medications/tests/test_models.py`: 10 tests, 14 cases, each seen failing
  against a deliberate break. Fixtures stay in the file: no other test file
  uses them yet
- `uv run pytest` — 67 passed. Total coverage 95%, `medications/models.py` at
  100%. `ruff`, `mypy` and `pre-commit` pass
- Pull request merged with every CI check passing; Render deployed it
  automatically
- Render deploy log: `Applying medications.0001_initial... OK`, then the service
  live
- Production, from outside, with `curl`:
  - `GET /healthz/` — `200`, `{"status": "ok", "checks": {"database": "ok"}}`
  - `GET /api/docs/` — `200`
  - `GET /api/medications/` — `404`: no medication endpoint exists yet

**Deviations from the task text:** none. Five tests beyond those first planned,
added after review: a different concentration value, unit or form is another
medication; the state default; three decimal places stored; the closed lists;
the string form.

**What this locks in for the rest of the project:** the database refuses a
duplicate medication, even with every optional field blank, and an account with
medications cannot be deleted. Without a serializer, a duplicate still ends in
an `IntegrityError`.

**Carried into later tasks:**

* Duplicate answered as a validation error, greater-than-zero, trimmed name and
  the value returned without trailing zeros (`"25"`, not `"25.000"`) — the
  serializer task
