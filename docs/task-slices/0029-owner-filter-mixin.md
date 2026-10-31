# Slice 2, task 2.3 — done

# Owner filter mixin

- `src/config/mixins.py`: `OwnerFilterMixin` filters a view's queryset by the
  requesting account through a declared `owner_path`
- A view without `owner_path` raises `ImproperlyConfigured` on its first call,
  with `MISSING_OWNER_PATH_MESSAGE` naming the view
- The mixin inherits from `GenericAPIView`: as a plain class, `mypy --strict`
  rejects `super().get_queryset()` and `self.request`
- `src/tests/test_mixins.py`: 2 tests with stand-in views, each seen failing
  against a deliberate break
- `uv run pytest` — 69 passed. Total coverage 96%, `config/mixins.py` at 100%.
  `ruff`, `mypy` and `pre-commit` pass
- Pull request merged with every CI check passing; Render deployed it
  automatically
- Production, from outside, with `curl`:
  - `GET /healthz/` — `200`, `{"status": "ok", "checks": {"database": "ok"}}`
  - `GET /api/docs/` — `200`
  - `GET /api/medications/` — `404`: no medication endpoint exists yet

**Deviations from the task text:** none.

**What this locks in for the rest of the project:** a view that inherits the
mixin reads only the requester's rows, and one that forgets its path to the
owner fails on its first call.

**Carried into later tasks:**

* Using the mixin and testing the 404 on another account's medication — the list
  and detail endpoints
* A view without a docstring inherits the mixin's text as its Swagger
  description — the list and detail endpoints
