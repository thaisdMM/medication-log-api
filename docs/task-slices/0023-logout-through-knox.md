# Slice 1, task 1.6 — done

# Logout through knox

- `src/users/urls.py`: `auth/logout/` (`auth-logout`) and `auth/logoutall/`
  (`auth-logoutall`), routed to knox's own `LogoutView` and `LogoutAllView`,
  unchanged. Public URLs: `POST /api/auth/logout/` and
  `POST /api/auth/logoutall/`
- `include("knox.urls")` is not used: it would also route knox's login,
  which the project replaced in `0021`
- Tests, 44 → 48, in `src/users/tests/test_auth_views.py`:
  - after a logout, the token used gets `401` on `GET /api/users/me/`
  - a logout keeps the account's other tokens working
  - after a logout-all, every token of the account gets `401`
  - a logout-all keeps the tokens of other accounts working
- `src/users/tests/conftest.py`: `second_account_token`, a second token for
  the same account
- `uv run pytest` — 48 passed. Total coverage 94% (167 statements, 10
  missed), the same 10 lines as in `0022`
- `uv run mypy` — `Success: no issues found in 32 source files`
- `uv run ruff format --check .` and `uv run ruff check .` — passed
- `pre-commit run --all-files` — all passed
- Pull request #18, `CI` green; Render deployed the merge
- Production, from outside, with the account `id` 2:
  - two logins give tokens A and B; `POST /api/auth/logout/` with A —
    `204`
  - `GET /api/users/me/` with A — `401`, `{"detail":"Invalid token."}`;
    with B — `200`
  - a third login gives token C; `POST /api/auth/logoutall/` with B — `204`
  - `GET /api/users/me/` with B — `401`; with C — `401`

**Deviations from the task text:** none.

**What this locks in for the rest of the project:** a logout deletes the
token on the server, so it stops working at once. Logout ends one token;
logout-all ends every token of the account and no other account's.
