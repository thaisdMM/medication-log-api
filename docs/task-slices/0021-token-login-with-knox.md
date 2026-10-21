# Slice 1, task 1.4 — done

# Token login with knox

- Before the task, in its own pull request: the whole email is stored in
  lowercase. `UserManager.canonical_email` holds the rule
  (`normalize_email(email).lower()`); `create_user`, the registration
  serializer's `validate_email` and the login serializer all use it. No
  migration: the only production account was already lowercase
- `django-rest-knox` 5.1.0 added as a production dependency. knox ships no
  `py.typed`, so `[[tool.mypy.overrides]]` sets `ignore_missing_imports` for
  `knox.*`; the rest stays strict
- `src/config/settings.py`:
  - `"knox"` in `INSTALLED_APPS`. Its own migrations create the
    `knox_authtoken` table; `makemigrations --check --dry-run` reports no
    migration of ours
  - `DEFAULT_AUTHENTICATION_CLASSES` = `knox.auth.TokenAuthentication` only.
    An anonymous request is now `401` with `WWW-Authenticate: Token`
  - `DEFAULT_RENDERER_CLASSES` = `JSONRenderer` only, which turns the
    browsable API page off
  - `REST_KNOX`: `TOKEN_TTL` 10 hours, `USER_SERIALIZER` `None`
- `src/users/serializers.py`: `LoginSerializer` takes `email` and
  `password`, passes the canonical email to `authenticate`, and adds the
  account to the validated data. Unknown email, wrong password and inactive
  account all fail with one message,
  `Unable to log in with the provided credentials.` Django's `login()` is
  not called, so no session is created
- `src/users/views.py`: `LoginView` subclasses knox's `LoginView`, with
  `authentication_classes = ()` and `permission_classes = (AllowAny,)`. Its
  `post` validates the credentials, puts the account on `request.user` and
  hands over to knox, which creates the token. The class line carries
  `# type: ignore[misc]`, because strict mypy refuses a subclass of an
  untyped class
- Sign-up: `UserRegistrationView` gets `authentication_classes = ()`, so a
  stale or invalid token sent along with it does not turn it into a `401`.
  `email` and `name` become `write_only`: the response is only `{"id": ...}`
- Routes: `src/config/urls.py` includes `users.urls` at `api/`, and
  `src/users/urls.py` holds `users/` (`user-register`) and `auth/login/`
  (`auth-login`). Public URLs: `POST /api/users/` and
  `POST /api/auth/login/`
- Tests, 30 → 39:
  - `src/users/tests/test_auth_views.py`: valid login answers exactly
    `{expiry, token}`; unknown email, wrong password and inactive account get
    the same `400` (one parametrized test); a mixed-case email logs in; the
    login token reaches a protected view; `expiry` is 10 hours after the
    login
  - `src/tests/test_rest_framework_defaults.py`: anonymous request `401` with
    `WWW-Authenticate: Token`; `Accept: text/html` gets `406`
  - `src/users/tests/test_views.py`: sign-up returns only the `id`; sign-up
    with an invalid token returns `201`
  - `src/users/tests/conftest.py`: `existing_account` and `login_data`
    fixtures
- Seen failing on purpose, each break undone afterwards:
  - `USER_SERIALIZER` pointed at a serializer — the body gains a `user` key
  - a distinct message for an unknown email, and `AllowAllUsersModelBackend`
    letting an inactive account in — different body, `200` instead of `400`
  - the login without `canonical_email` — `400` instead of `200`
  - knox removed from the authentication classes — `403` instead of `200`
    and of `401`
  - `TOKEN_TTL` at 11 hours — `expiry` outside the window
  - the browsable renderer back — `400` instead of `406`
  - sign-up without `authentication_classes = ()` — `401` instead of `201`
- `uv run pytest` — 39 passed. Total coverage 94% (155 statements, 10
  missed), up from 92% in `0020`. The 10 missed lines are the same ones,
  outside `users`
- `uv run mypy` — `Success: no issues found in 32 source files`
- `uv run ruff format --check .` — `68 files already formatted`
- `uv run ruff check .` — `All checks passed!`
- `pre-commit run --all-files` — all passed
- `quality`, `tests` and `build` green on the pull request; Render deployed
  the merge and went live. The deploy log shows `Apply all migrations:`
  listing `knox`, then `Applying knox.0001_initial... OK` through
  `knox.0009_extend_authtoken_field... OK`
- Production, from outside:
  - `curl -i https://medication-log-api.onrender.com/healthz/` — `200`
  - `POST /api/users/` with `prova.tarefa14@example.com` — `201`,
    `{"id":2}`, no `email` or `name` in the body
  - `POST /api/auth/login/` with `Prova.Tarefa14@Example.com` — `200`,
    `{"expiry": ..., "token": ...}`, expiry 10 hours after the request
  - the same login with a wrong password — `400`,
    `{"non_field_errors":["Unable to log in with the provided credentials."]}`
  - `POST /api/users/` with `Accept: text/html` — `406`
- Documents: ADR 0007 records the choice of knox; ADR 0002 now points to it
  instead of "not decided"; `0017` rows 1.4, 1.6 and 1.8 and the Token and
  Logout decisions rewritten for knox

**Deviations from the task text:**

- **knox, not `simplejwt`.** `0017` planned `simplejwt` with access and
  refresh tokens. The choice changed before the task started (ADR 0007), and
  `0017` was rewritten in this task: one token, 10 hours, no refresh
  endpoint
- **One route file per app.** The plan had a separate `auth_urls.py` for the
  `api/auth/` prefix. All the app's routes went into `users/urls.py`
  instead, included at `api/`; the public URLs are the ones planned
- **The sign-up response changed.** Task 1.3 returned `id`, `email` and
  `name`; it now returns only `id`

**What this locks in for the rest of the project:** every endpoint is
authenticated by a knox token, sent as `Authorization: Token ...`, and an
anonymous request is a `401`. The API speaks JSON only. A public endpoint
declares both `AllowAny` and an empty `authentication_classes`. The email is
compared and stored through `canonical_email`. Responses carry no personal
data they do not need. A failed login never says which part was wrong.

**Carried into later tasks:**

* Logout and logout-all (task 1.6) go into `users/urls.py` under `auth/`
* Rate limiting on login and sign-up: outside slice 1
* An email edited in the admin, or set directly on the model, keeps its
  case: the model does not lowercase — slice 4, with the admin panel
* A request with the token passing, and one without it getting `401`, are
  not proved in production: no protected endpoint exists there yet. Task
  1.5, with `GET /api/users/me/`
* The account `prova.tarefa14@example.com` (`id` 2) now exists in the
  production database, created by the proof above
