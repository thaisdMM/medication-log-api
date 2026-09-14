# Slice 0, task 0.12 — done

# User model behavior tests

- New task, not in the original slice 0 list (`0002`): closes the item
  carried forward from `0011`/`0012` as "user model behaviour tests —
  slice 1", appended to slice 0 instead, per the numbering rule in `0002`
- `src/users/models.py`: `objects` now declared as
  `objects: ClassVar[UserManager] = UserManager()`. Without the
  annotation, the type checker inferred the base `Model` class's
  declared type instead of `UserManager`
  (`django-stubs/db/models/base.pyi`, line 62), so
  `User.objects.create_user(...)` resolved to `Any`. Same pattern
  Django's own stubs use for `auth.User.objects` and that this file
  already used for `REQUIRED_FIELDS`
- `src/users/tests/test_models.py`: 16 tests added (2 → 18), with a
  `valid_user_data` fixture reused across them. Covers
  `UserManager.create_user` and `create_superuser`: persistence and
  database id, stored email and name, uniqueness enforced at the
  database level, email normalization, `ValueError` on missing email,
  name or password, Argon2 password hashing, default flags on a regular
  user, admin flags on a superuser, `__str__`, the `USERNAME_FIELD` /
  `REQUIRED_FIELDS` contract, and authentication through
  `django.contrib.auth.authenticate`
- Superuser flag assertions call `refresh_from_db()` before checking
  `is_staff`/`is_superuser`: `create_superuser` sets them with a second
  `save()` after `create_user`'s insert, so reading the in-memory object
  would not prove they reached the database
- `test_user_logs_in_with_email` (checks `USERNAME_FIELD` /
  `REQUIRED_FIELDS`) and `test_user_authenticates_with_email_and_password`
  (calls `authenticate()`) both kept: the first catches an accidental
  change to either constant, the second exercises the login itself
- `uv run pytest` — 18 passed. `users/models.py`: 100% coverage
  (34/34 statements). Project total: 82% (59/72 statements) — the 13
  missed lines are all outside `users` (`config/asgi.py`,
  `config/urls.py`, `config/wsgi.py`, `medication_log_api/__init__.py`),
  none touched by this task
- `uv run mypy` — `Success: no issues found in 16 source files`
- `uv run ruff format --check .` — `45 files already formatted`
- `uv run ruff check .` — `All checks passed!`

**What this locks in for the rest of the project:** the User model's
core behavior — persistence, uniqueness, mandatory fields, password
hashing, default and admin flags, and the authentication contract — is
covered by an automated suite, with `users/models.py` at 100% coverage.
Task 0.9 (health endpoint) is the next task to add tests, on top of this
baseline.

**Carried into later tasks:**

* `normalize_email` only lowercases the domain — `Ana@x.com` and
  `ana@x.com` would be two accounts. Still a product decision, not a
  defect in these tests — slice 1, alongside the invite flow (carried
  again from `0011`)
* Coverage threshold vs. report-only — still task 0.10's decision
  (carried again from `0012`)
