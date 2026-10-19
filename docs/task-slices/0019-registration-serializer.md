# Slice 1, task 1.2 — done

# Registration serializer

- `src/users/serializers.py`: `UserRegistrationSerializer`, a
  `ModelSerializer[User]` with fields `id`, `email`, `name` and `password`
  - `email` and `password` declared by hand. `password` is `write_only`, so
    it is accepted on input and never serialized; it carries no
    `max_length`, because the one generated from the model would copy 128,
    the size of the hash. `email` repeats the model's `max_length=255`
  - `validate_email` normalizes the domain with `User.objects.normalize_email`
    before looking for a duplicate, and returns the normalized address. The
    check generated from the model's `unique=True` is gone with the declared
    field, so there is one check and one message:
    `A user with this email address already exists.`
  - `validate` builds an unsaved `User(email=..., name=...)` and passes it to
    `password_validation.validate_password(..., user=user)`. Without the
    user, the similarity validator configured in `settings.py` accepts any
    password. Django's `ValidationError` is converted to
    `{"password": [...]}` so the error names the field
  - `create` calls `User.objects.create_user`. The `ModelSerializer` default
    would store the typed password as plain text
- Name and password are trimmed by the DRF default (`trim_whitespace=True`);
  trimming the password was Thaís' decision, and the login serializer of
  `simplejwt` trims too. No test of their own
- `src/users/tests/test_serializers.py`: 5 tests added (22 → 27), with a
  `registration_data` fixture. None goes through HTTP:
  `test_password_is_saved_hashed` (the stored hash matches the typed
  password), `test_output_never_contains_password` (a `User` built in memory,
  no database), `test_duplicate_email_with_uppercase_domain_is_rejected`,
  `test_password_similar_to_name_is_rejected` and
  `test_password_similar_to_email_is_rejected`
- Seen failing on purpose, each break undone with `git restore`: without
  `create`, `test_password_is_saved_hashed` fails; without the declared
  `email` and `validate_email`,
  `test_duplicate_email_with_uppercase_domain_is_rejected` fails
- `uv run pytest` — 27 passed. `users/serializers.py`: 100% coverage (25/25
  statements). Project total: 91% (101/111 statements), up from 88% (76/86)
  in `0018` — the 10 missed lines are all outside `users` (`config/asgi.py`,
  `config/wsgi.py`, `medication_log_api/__init__.py`)
- `uv run mypy` — `Success: no issues found in 28 source files`
- `uv run ruff format --check .` — `62 files already formatted`
- `uv run ruff check .` — `All checks passed!`
- `makemigrations --check --dry-run` — `No changes detected`
- Committed straight to `main`: no `settings.py`, `pyproject.toml` or
  `uv.lock` change. `quality`, `tests` and `build` green on `main`;
  `/healthz/` in production still `200`

**Deviations from the task text:**

- **5 tests, not 16.** The task planned 16 and the suite going from 22 to 38.
  Eleven of them only re-checked what the DRF, Django or an existing test
  already guarantees (required fields, email format, trimming, blank name,
  minimum length, domain normalization already in `test_models.py`, exact
  duplicate, a plain valid sign-up), so the suite was cut to the tests that
  fail when a line of this serializer is wrong. The hash test lost its
  `argon2$` prefix assertion, which `test_models.py` already makes. The
  duplicate test lost its `count() == 1`, which `is_valid()` cannot change.
  The output test no longer saves anything, since the output shape depends
  only on `write_only` and `Meta.fields`

**What this locks in for the rest of the project:** any account created
through a serializer goes through `create_user`, so the password is hashed
with Argon2, and goes through the project's four password validators with
the email and name in hand. A duplicate email in a different case is refused
with a message instead of reaching the database. The password never appears
in the serializer's output.

**Carried into later tasks:**

* Two sign-ups with the same email at the same moment both pass
  `validate_email`, and the second one raises `IntegrityError` at the
  database. It has to become a `400`, not a `500` — task 1.3
* Login with an uppercase email domain: `simplejwt` hands the email to
  `authenticate` without normalizing it, so an account saved as `ana@x.com`
  may be refused when the user types `ana@X.COM` — to be checked in task 1.4
* The user fixtures are repeated in `test_models.py` and
  `test_serializers.py`. A shared `conftest.py` is worth it once a third
  test file needs them
