# Slice 1, task 1.3 — done

# Registration endpoint

- `src/users/views.py`: `UserRegistrationView`, a
  `generics.CreateAPIView[User]` with `serializer_class =
  UserRegistrationSerializer` and `permission_classes = (AllowAny,)`. The
  `AllowAny` overrides the closed default from `0018` for this view only
- `src/users/urls.py` created, with one route: `path("",
  UserRegistrationView.as_view(), name="user-register")`.
  `src/config/urls.py` includes it with `path("api/users/",
  include("users.urls"))`, so the endpoint is `POST /api/users/`. Each app
  keeps its own `urls.py`; `healthz` stays imported directly in
  `config/urls.py`
- `src/users/serializers.py`:
  - `create` wraps `User.objects.create_user` in `transaction.atomic()` and
    catches `IntegrityError`, raising `ValidationError({"email": [...]})`. Two
    sign-ups with the same email at the same moment both pass
    `validate_email`; the loser now gets a `400` instead of a `500`. The
    `atomic()` keeps the surrounding transaction usable after the database
    refuses the insert
  - `DUPLICATE_EMAIL_MESSAGE` extracted as a constant, used by
    `validate_email` and by `create`, so the two messages cannot diverge
- `src/users/tests/conftest.py` created, holding the `registration_data`
  fixture, removed from `test_serializers.py`. Both test files use it
- `src/users/tests/test_views.py`:
  `test_registration_without_authentication_returns_201` posts the fixture
  data as JSON through `reverse("user-register")` with no login and expects
  `201`
- `src/users/tests/test_serializers.py`:
  `test_email_taken_after_validation_is_rejected_on_create` saves the account
  first, then calls `create()` directly, skipping `is_valid()`, which is what
  the losing request does. It expects the `{"email": [...]}` error and
  `User.objects.count() == 1`
- Seen failing on purpose, each break undone with `git restore`: without
  `permission_classes = (AllowAny,)`, the view test fails with
  `assert 403 == 201`; without `with transaction.atomic():`, the serializer
  test fails with `TransactionManagementError` on the `count()` line, after
  `pytest.raises` has already passed
- `uv run pytest` — 29 passed (27 before). Total coverage 92% (127
  statements, 10 missed), up from 91% (101/111) in `0019`. The 10 missed lines
  are all outside `users` (`config/asgi.py`, `config/wsgi.py`,
  `medication_log_api/__init__.py`)
- `uv run mypy` — `Success: no issues found in 31 source files`
- `uv run ruff format --check .` — `66 files already formatted`
- `uv run ruff check .` — `All checks passed!`
- `makemigrations --check --dry-run` — `No changes detected`
- `pre-commit run --all-files` — all passed
- Committed straight to `main` in two separate commits: the shared fixture,
  then the endpoint. No `settings.py`, `pyproject.toml` or `uv.lock` change.
  `quality`, `tests` and `build` green on `main`; Render deployed the commit
  and it went live
- Production, from outside:
  - `curl -i https://medication-log-api.onrender.com/healthz/` — `200`,
    `{"status": "ok", "checks": {"database": "ok"}}`
  - `POST /api/users/` with `prova.tarefa13@example.com` — `201`,
    `{"id":1,"email":"prova.tarefa13@example.com","name":"Prova Tarefa"}`, no
    `password` in the body
  - the same `POST` again — `400`,
    `{"email":["A user with this email address already exists."]}`

**Deviations from the task text:**

- **The fixture moved to `conftest.py` in this task.** `0019` left it for
  when a third test file needed it. The view test uses the same sign-up data
  as the serializer tests, and Thaís decided that two users are enough to
  justify a shared fixture. It went in its own commit, before the endpoint.
  It is the reason `mypy` counts 31 files, not the 30 planned
- **`403`, not `401`, when a view forgets `AllowAny`.** The task list (`0017`,
  task 1.3) says `401`. Without a token authentication class, the DRF answers
  an anonymous request with `403`. It becomes `401` when `simplejwt` enters in
  task 1.4, as `0018` already records

**What this locks in for the rest of the project:** a public endpoint
declares `AllowAny` on its own view; everything else stays closed. Each app
owns its routes in its `urls.py`, and `config/urls.py` only points at the
prefix with `include`. A duplicate email is a `400` naming the `email` field
in every case, including two sign-ups at the same moment. Any serializer that
catches a database error does it around a `transaction.atomic()` block.

**Carried into later tasks:**

* The browsable API page stays on until task 1.4, which sets
  `DEFAULT_RENDERER_CLASSES` to `JSONRenderer` only, in the same pull request
  that edits `settings.py`, with a test of its own. This closes the question
  `0018` left open about that page in production
* A sign-up sent with an expired token in the `Authorization` header: to be
  checked in task 1.4, when `simplejwt` enters
* Rate limiting on sign-up: no decision file covers it. It stays outside slice
  1
* The account `prova.tarefa13@example.com` (`id` 1) now exists in the
  production database, created by the proof above
