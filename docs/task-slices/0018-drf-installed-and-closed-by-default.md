# Slice 1, task 1.1 — done

# DRF installed and configured, with every view closed by default

- Django raised from 6.1 to 6.1.2 with `uv lock --upgrade-package django`:
  one `Updated` line, `django v6.1 -> v6.1.2`, and only the `django` block
  of `uv.lock` changed. `pyproject.toml` stayed `django[argon2]>=6.1`, since
  6.1.2 is inside the range. `django.get_version()` printed `6.1.2` and the
  21 existing tests passed
- `djangorestframework` 3.18.3 added as a production dependency
  (`uv add djangorestframework`) and `djangorestframework-stubs[compatible-mypy]`
  3.18.1 added to the `dev` group (`uv add --dev`). `uv tree --depth 1`
  showed the DRF without `(group: dev)`, the stubs with it, and `mypy`
  unchanged at 2.3.1
- `mypy_drf_plugin.main` registered next to `mypy_django_plugin.main` in
  `[tool.mypy]`; `uv run mypy` passed on the 24 source files that existed
  at that point
- `"rest_framework"` added to `INSTALLED_APPS`, after the Django apps and
  before the project apps. `REST_FRAMEWORK` added at the end of
  `settings.py` with only `DEFAULT_PERMISSION_CLASSES`, set to
  `rest_framework.permissions.IsAuthenticated` as a dotted string
- `manage.py check`: no issues. `makemigrations --check --dry-run`:
  `No changes detected` — the DRF ships migrations only inside
  `rest_framework/authtoken/`, which is not installed
- `src/tests/` created, with an empty `__init__.py`, as the place for tests
  of project-wide configuration that belong to no app.
  `test_rest_framework_defaults.py` holds one test: a throwaway `APIView`
  that declares no `permission_classes`, called with an anonymous request
  through `APIRequestFactory`, answers `403` with
  `{"detail": "Authentication credentials were not provided."}`. It needs
  no `django_db` mark
- The test was seen failing on purpose: with the key spelled
  `DEFAULT_PERMISSIONS_CLASSES`, `manage.py check` reports no issues and
  `pytest src/tests` fails with `assert 200 == 403`. Key restored, suite
  green again
- Full local run: `ruff check` clean, `ruff format --check` clean on the
  project files, `mypy` passed on 26 source files, `pytest` 22 passed
  (21 before), total coverage 88% (86 statements, 10 uncovered; 85 and 10
  before), `makemigrations --check` no changes, `pre-commit run --all-files`
  all passed
- Production image measured with `docker compose build web` and
  `docker image ls medication-log-api-web`: 226MB on `main` before the
  task, 229MB after (Django 6.1 -> 6.1.2 and the DRF added). The 232MB
  recorded in `0009` is not the baseline for this comparison — it was
  measured at task 0.6, on an earlier `uv.lock`, and belongs to the
  `medication-log-api` image built then, not to the one `compose` builds
- Inside the image: `import django, rest_framework` printed `6.1.2 3.18.3`;
  `site-packages` holds no package with `stubs` in its name; `/app/src`
  lists no `tests` folder, so `.dockerignore`'s `src/**/tests/` covers
  `src/tests/` too
- Pull request #4, `chore: install django rest framework, closed by
  default`, merged with **Squash and merge** as commit `aeffbd7`. The
  `quality`, `tests` and `build` jobs ran green on the branch and again on
  `main`; Render deployed `aeffbd7` afterwards
- Render log of that deploy: `No migrations to apply.`,
  `Listening at: http://0.0.0.0:8000`, service live
- `curl -i https://medication-log-api.onrender.com/healthz/` from outside:
  `200`, `{"status": "ok", "checks": {"database": "ok"}}`
- Branch `chore/install-drf` deleted locally and on GitHub; local `main`
  matches `origin/main`

**Deviations from the task text:**

- Django ended at **6.1.2**, not 6.1.1: 6.1.2 had been released between the
  writing of the task and its execution, and `--upgrade-package` takes the
  newest release the range accepts
- The DRF ended at **3.18.3**, not 3.18.1, for the same reason; the stubs
  stayed at 3.18.1, the newest release of that package at install time
- The image baseline is **226MB**, measured on `main` before the task, and
  not the 232MB recorded in `0009` — see the measurement above. This closes
  the pending comparison `0009` left open for "once slice 1 adds DRF"

**What this locks in for the rest of the project:** any DRF view that
does not declare its own `permission_classes` refuses an anonymous
request; a public endpoint has to say so with `AllowAny`. The rule is
proved by a test that goes through a real `APIView`, so a misspelled
settings key — which Django's checks do not report — turns the suite red.
Tests of project-wide configuration live in `src/tests/`, outside any app.
The DRF is in the production image and the type stubs are not.

**Carried into later tasks:**

* The expected status in `test_rest_framework_defaults.py` changes from
  `403` to `401` when `simplejwt` becomes the first authentication class
  — task 1.4
* Whether the DRF browsable API page renders in production, where static
  files are not served — task 1.3, once the first endpoint exists
