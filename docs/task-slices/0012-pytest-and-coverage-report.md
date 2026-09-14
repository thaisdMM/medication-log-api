# Slice 0, task 0.8 — done

# `pytest` with a coverage report

- `pytest`, `pytest-django` and `pytest-cov` installed as dev dependencies
  (`uv add --dev pytest pytest-django pytest-cov`): `pytest` 9.1.1,
  `pytest-django` 4.14.0, `pytest-cov` 7.1.0, pulling in `coverage` 7.16.0
- Configuration in `pyproject.toml`, in the native `[tool.pytest]` table
  (available since pytest 9.0), not `[tool.pytest.ini_options]`:
  `DJANGO_SETTINGS_MODULE = "config.settings"`, `pythonpath = ["src"]`,
  `testpaths = ["src"]`,
  `addopts = ["--strict-markers", "-v", "--cov", "--cov-report=term-missing"]`
- `-v` added to `addopts`, not in the planned configuration: without it the
  output shows neither test names nor individual results. `--tb=short` was
  tried and not kept — it only changes how failures are printed
- `[tool.coverage.run]`: `source = ["src"]`,
  `omit = ["*/migrations/*", "*/tests/*", "src/manage.py"]`. No branch
  coverage, no minimum percentage
- No `pytest.ini` created
- `src/users/tests.py` removed (`git rm`) and replaced by a `src/users/tests/`
  package with an empty `__init__.py`, so each test module gets a unique
  import name (`users.tests.test_models`) once other apps add their own
  `tests/test_models.py`
- `src/users/tests/test_models.py`:
  `test_user_is_the_model_django_authenticates_with` and
  `test_user_table_starts_empty_in_the_test_database` (marked `django_db`).
  Both check the setup, not user behaviour
- `uv run pytest` — `configfile: pyproject.toml`,
  `django: version: 6.1, settings: config.settings (from ini)`, `2 passed`.
  Coverage baseline: 58% total (72 statements, 30 missed), `users/models.py`
  at 50%
- Without `@pytest.mark.django_db`, the database test fails with
  `RuntimeError: Database access not allowed, use the "django_db" mark, or the
  "db" or "transactional_db" fixtures to enable it.`
- `.gitignore` gained `.coverage`. `.pytest_cache/` left out: pytest writes its
  own `.gitignore` (`*`) inside that directory
- `.dockerignore` gained `src/**/tests/`: the `Dockerfile` copies `src/`
  unfiltered, so without it the tests reach the production image
- `.dockerignore`: `__pycache__/`, `*.pyc`, `*.pyo` and `*.pyd` now prefixed
  with `**/`. A pattern without `**` matches only at the root of the build
  context, so `src/users/__pycache__` was being copied into the image
- `docker compose build web` tags the image `medication-log-api-web`, since
  `compose.yaml` sets no `image:` key. The image checks ran against that tag —
  `medication-log-api` is the older image from task 0.6's `docker build -t`
- `docker run --rm medication-log-api-web ls /app/src/users` — no `tests`, no
  `__pycache__`
- `docker run --rm medication-log-api-web ls /app/.venv/bin` — no `pytest`
- `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy` (16
  source files) and `uv run pre-commit run --all-files` — all pass
- The test suite is not a `pre-commit` hook: tests that touch the database are
  slow, and a slow hook gets bypassed with `--no-verify`. Running the suite on
  every push is task 0.10
- Item carried from task 0.3 closed with no change: tests live under `src`,
  already covered by `files = ["src"]` in `[tool.mypy]`

**What this locks in for the rest of the project:** one command runs the test
suite against a separate test database created by `pytest-django`, and reports
coverage with the lines no test exercised. The production image carries
neither the tests nor `pytest`. Task 0.10 now has a command to gate on.

**Carried into later tasks:**

* Coverage: report only, or fail below a threshold — task 0.10
* Branch coverage (`branch = true`) — open, Thaís' choice
* `--reuse-db`, once the suite gets slow enough to matter — no task assigned
* `client` fixture and the first endpoint test — task 0.9
* User model behaviour tests — slice 1
