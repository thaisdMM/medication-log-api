# Slice 1, task 1.5 — done

# Current user endpoint

- Before the code: ADR 0017 (minimal personal data in responses) and ADR
  0018 (fixed token expiry); `0017` row 1.5 says the endpoint returns the
  `id` and `name` behind the token, never the email
- `src/users/serializers.py`: `CurrentUserSerializer`, read-only, fields
  `id` and `name`
- `src/users/views.py`: `CurrentUserView`, a `RetrieveAPIView` whose
  `get_object()` returns `request.user`. It declares no authentication or
  permission classes, so it goes through the project defaults
- `src/users/urls.py`: `users/me/` (`user-me`). Public URL:
  `GET /api/users/me/`
- Tests, 39 → 44:
  - `src/users/tests/test_views.py`: with a token, `200` and exactly
    `{id, name}`; without a token, `401`; the token of one account never
    returns another account
  - `src/users/tests/test_auth_views.py`: the login token reaches
    `GET /api/users/me/`, replacing the stand-in `ProtectedView`; an expired
    token gets `401`; using the token does not move its `expiry`
- `uv run pytest` — 44 passed. Total coverage 94% (166 statements, 10
  missed), the same 10 lines as in `0021`
- `uv run mypy` — `Success: no issues found in 32 source files`
- `uv run ruff format --check .` and `uv run ruff check .` — passed
- `pre-commit run --all-files` — all passed
- Pull requests #7, #8 and #9, each with `CI` green; Render deployed each
  merge
- Production, from outside, with the account `id` 2:
  - `POST /api/auth/login/` — `200`, `{"expiry": ..., "token": ...}`
  - `GET /api/users/me/` with the token — `200`, `{"id":2,"name":"Prova Tarefa"}`
  - `GET /api/users/me/` without a token — `401`,
    `{"detail":"Authentication credentials were not provided."}`

**Deviations from the task text:**

- The login-token test also checks the `id` in the body, not only the
  status
- The test that the expiry does not move first asserts the `200`, so a
  refused request cannot pass it

**What this locks in for the rest of the project:** an endpoint about the
current account reads it from the token, never from the URL. Responses carry
the `id` and `name`, not the email. A token expires at a fixed time from the
login; using it does not extend it.

**Carried into later tasks:**

* Logout and logout-all (task 1.6) go into `users/urls.py` under `auth/`
* Rate limiting on login and sign-up: outside slice 1
* An email edited in the admin, or set directly on the model, keeps its
  case — slice 4, with the admin panel

Closes the item carried from `0021`: a token passing and a missing token
getting `401` are now proved in production.
