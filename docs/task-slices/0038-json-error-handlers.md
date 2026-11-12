# First release follow-up — done

# JSON answers for errors outside the API views

- `src/config/error_handlers.py`: `JsonErrorHandler` answers
  `{"detail": <message>}` with its status; nothing of the error reaches the
  body. Messages: "Bad request.", "You do not have permission to perform this
  action.", "Not found." and "A server error occurred."
- `src/config/urls.py`: `handler400`, `handler403`, `handler404` and
  `handler500`, each an instance of `JsonErrorHandler`
- `src/tests/test_error_handlers.py`: one test per handler, through the
  project's real routes
- Each new test seen failing against the code before this change, every
  response Django's HTML page:
  - All four handlers absent — all four tests failed
  - Bad request handler removed — the unknown host test failed
  - Permission denied handler removed — the permission refused test failed
  - Not found handler removed — the path with no route test failed
  - Server error handler removed — the unhandled error test failed
- `uv run pytest` — 174 passed. Total coverage 97%. `ruff`, `mypy`,
  `manage.py check` and `pre-commit` pass
- Pull request merged with every CI check passing; Render deployed it
  automatically
- Production, from outside, with `curl`:
  - `GET /api/medications//` — `404`, `{"detail": "Not found."}`, JSON
  - `GET /healthz/` — `200`; `GET /api/medications/` without a token — `401`,
    the same body as before
  - `GET /healthz/` with an unknown `Host` — `403` HTML from Render's edge;
    the request never reaches Django, so the bad request handler is proven
    by its test only

**Deviations from the task text:** the follow-up asked for `404` and `500`.
The bad request and permission denied handlers were added too, so no error
raised outside the API views answers with HTML.

**What this locks in for the rest of the project:** every error that Django
answers outside the API views is JSON with a `detail` message, like the API
views. Removing a handler fails its test.

**Carried into later tasks:**

* A CSRF failure answers with Django's HTML page, through its own setting
  (`CSRF_FAILURE_VIEW`); it happens only on the admin login form, which the
  first release does not use
