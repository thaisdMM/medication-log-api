# Slice 1, task 1.8 — done

# Slice 1 proven in production

- No code changed: the suite is the one in `0024`, 53 tests
- Production, from outside, with `curl`, on a new account:
  - `GET /healthz/` — `200`, `{"status": "ok", "checks": {"database": "ok"}}`
  - `POST /api/users/` — `201`, `{"id":3}`
  - `POST /api/auth/login/` — `200`, `{"expiry": ..., "token": ...}` (token A)
  - `GET /api/users/me/` with A — `200`, `{"id":3,"name":"Prova Slice 3"}`;
    without a token — `401`,
    `{"detail":"Authentication credentials were not provided."}`
  - a second login gives token B; `POST /api/auth/logout/` with A — `204`
  - `GET /api/users/me/` with A — `401`, `{"detail":"Invalid token."}`;
    with B — `200`
  - a third login gives token C; `POST /api/auth/logoutall/` with B — `204`
  - `GET /api/users/me/` with C — `401`; with B — `401`
- `GET /api/docs/` and `GET /api/schema/` answer without a token, as checked
  in `0024`
- The run showed one account holding several valid tokens at once; that
  choice is recorded in the ADR on several tokens per account

**Deviations from the task text:** none.

**What this locks in for the rest of the project:** an account signs up,
logs in, uses its token and logs out against the public address, and the
interactive API documentation is public. Slice 1 is closed; medication starts
from here.
