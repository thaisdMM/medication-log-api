# Slice 2, task 2.5 — done

# Medication list and create

- `src/medications/views.py`: `MedicationListCreateView` lists and creates the
  requesting account's medications, through `OwnerFilterMixin` with
  `owner_path = "owner"`
- The list is unpaginated and ordered by `Collate(Lower("name"), "und-x-icu")`,
  then `id`: case and accents do not move a name, and equal names come oldest
  first. The production database uses the `C.UTF-8` collation, which places
  accented names after "Z"
- `src/medications/serializers.py`: `MedicationListFilterSerializer` validates
  `?state` against `MedicationState`; a value outside the list, empty included,
  answers 400 on `state`
- `src/medications/urls.py`: `/api/medications/`, included in `config/urls.py`
- `src/medications/tests/test_views.py`: each test seen failing against a
  deliberate break
- `uv run pytest` — 102 passed. Total coverage 97%, `medications/views.py` at
  100%. `ruff`, `mypy` and `pre-commit` pass
- Pull request merged with every CI check passing; Render deployed it
  automatically
- Production, from outside, with `curl`:
  - `GET /healthz/` — `200`, `{"status": "ok", "checks": {"database": "ok"}}`
  - `GET /api/docs/` — `200`
  - `GET /api/medications/` without a token — `401`
  - `POST /api/medications/` — `201` for four medications, without the owner;
    `"0.025"` returned as sent
  - `GET /api/medications/` — `200`, in the order "Ácido fólico",
    "amoxicilina", "Levotiroxina", "Zolpidem"
  - `?state=suspended` — only the suspended medication; `?state=banana` — `400`
  - The same name in capitals — `400` with `DUPLICATE_MEDICATION_MESSAGE`

**Deviations from the task text:** the ordering gained the `und-x-icu`
collation and an `id` tie-break, and an empty or invalid `?state` answers 400.

**What this locks in for the rest of the project:** an account lists only its
own medications, in dictionary order in production whatever the database's
collation.

**Carried into later tasks:**

* The test database uses `en_US.utf8`, so removing only the `Collate` passes the
  tests; production is the proof — the slice proven in production
* `?state` and its 400 are missing from the interactive documentation — the
  interactive documentation
* The class docstring, `Attributes` included, shows as the public description of
  both operations — the interactive documentation
* A repeated `state` uses its last value, and an unknown query parameter is
  ignored
