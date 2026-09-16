# Slice 0, task 0.9 — done

# Health endpoint, with tests

- New app `ops`, created with `startapp` and registered in
  `INSTALLED_APPS` (`src/config/settings.py`), after `users`. No model,
  no migration: `models.py` and `admin.py` left empty, `apps.py`
  untouched
- `src/ops/views.py`: `healthz(request: HttpRequest) -> JsonResponse`.
  Opens `connection.cursor()` and runs a trivial query (`SELECT 1`,
  touches no project table) inside a `try`/`except Error`. `Error` is
  `django.db`'s base exception (PEP 249) — covers `OperationalError`
  and `InterfaceError` alike, without catching an unrelated bug in the
  view itself
- Response body carries only `status` and `checks`, never exception
  detail: this is the first public, unauthenticated endpoint in the
  project, and a database exception message carries host, port and
  database user
- `200` on success (default), `503` explicit on failure — not `500`,
  since the application itself is up
- `src/config/urls.py`: route `path("healthz/", healthz, name="healthz")`,
  imported directly, no `include()`. Trailing slash deliberate:
  `CommonMiddleware`'s `APPEND_SLASH` redirects a slash-less request
  with `301`, which a deployment platform's health check may not follow
- `src/ops/tests/test_views.py`: 3 tests added (18 → 21):
  `test_healthz_returns_200_when_the_database_answers` (real database,
  `@pytest.mark.django_db`), `test_healthz_returns_503_when_the_database_is_unreachable`
  (`monkeypatch.setattr("ops.views.connection", BrokenConnection())`,
  no real database touched), `test_healthz_without_trailing_slash_redirects`
  (asserts both the `301` and the `Location` header)
- `uv run pytest` — 21 passed. `ops/views.py`: 100% coverage (9/9
  statements). Project total: 88% (75/85 statements), up from 82%
  (59/72) in `0013` — the 10 missed lines are all outside `ops`
  (`config/asgi.py`, `config/wsgi.py`,
  `medication_log_api/__init__.py`), none touched by this task
- `uv run mypy` — `Success: no issues found in 24 source files`
- `uv run ruff format --check .` — `54 files already formatted`
- `uv run ruff check .` — `All checks passed!`

**What this locks in for the rest of the project:** a public URL that
proves the system reaches PostgreSQL — `200` when it does, `503` with a
named failing check when it doesn't — backed by tests for both cases
and for the trailing-slash redirect. Task 0.11 depends on this to prove
a deployment is actually live.

**Carried into later tasks:**

* Converting the view to Django REST Framework, so it appears in the
  interactive API docs — slice 1
* Whether Render uses this path to fail a deployment or restart the
  service, and with what time tolerance (Neon takes seconds to wake
  up) — task 0.11, to check against Render's documentation
* Registering `/healthz/` in the Render dashboard, with the trailing
  slash — task 0.11
* Documenting where the `healthz` convention comes from, in the
  README — slice 6
* Coverage threshold vs. report-only — still task 0.10's decision
  (carried again from `0012`/`0013`)
* Whether the `ops` app takes on other endpoints later, and under what
  criteria — open until a first candidate appears
* `--reuse-db`, once the suite's run time becomes noticeable — not yet
