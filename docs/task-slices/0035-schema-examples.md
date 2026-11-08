# Slice 2, task 2.10 — done

# Examples in the API schema

- `src/tests/test_api_docs.py`: moved from `src/ops/tests/`; the `ops` app
  holds only the health endpoint, and these tests cover the whole schema
- `src/config/schema.py`: `FIELD_ERRORS_SCHEMA`, the `400` body as an object
  whose keys are fields and whose values are lists of messages; the
  missing-token response shows "No token" and "Invalid or expired token"
- `src/medications/serializers.py`: a full medication in the request and in
  the response of the six medication operations
- `src/medications/views.py`: `400` examples ("Refused field", "Duplicate",
  "Invalid state") and the `404` example
- `src/users/views.py`: `400` examples on sign-up ("Refused field", "Email in
  use"), login ("Refused field", "Wrong credentials") and account deletion
  ("Missing password", "Wrong password")
- `src/users/serializers.py`: one example account, with generic values, feeds
  the request examples of sign-up, login and account deletion and the response
  examples of sign-up and the current account; the login response shows a
  fictitious 64-character token and an ISO 8601 UTC expiry
- `src/users/tests/conftest.py`: fixtures for the account shown in the
  examples and its token
- `docs/conventions.md`: every error response has an example; project
  messages enter it through their constants, library messages as the real
  response writes them
- Each new test seen failing:
  - 401 examples removed — the every-error-response test and both token
    example tests failed
  - Sign-up 400 described as a free-form object — the messages-by-field test
    failed
  - Wrong text in each 401, 404 and invalid-state example, one at a time —
    only the comparison of that example failed
  - Medication request example with a form outside the closed list — the
    validation test failed
  - Medication response example without the state — the returned-fields test
    failed
  - Wrong body in each of the eight 400 examples, one at a time — only the
    case of that example failed
  - Sign-up request example with an invalid email — the sign-up request test
    failed
  - Login and account deletion request examples with a wrong password — only
    the request test of that operation failed
  - Sign-up, login and current account response examples without the id, the
    expiry and the name — only the response test of that operation failed
- `uv run pytest` — 170 passed. Total coverage 97%. `ruff`, `mypy`,
  `spectacular --validate --fail-on-warn` and `pre-commit` pass
- Three pull requests merged with every CI check passing; Render deployed each
  automatically
- Production, from outside, with `curl`:
  - `GET /api/docs/` — `200`
  - `GET /api/schema/` — all 21 error responses carry an example; every `400`
    maps each field to a list of messages
  - The sign-up, login and account deletion requests show the example account;
    the sign-up, login and current account responses show their fields
  - `GET /api/users/me/` without a token and with an invalid one answers the
    exact bodies of the two `401` examples

**Deviations from the task text:** the task asked for error examples and the
medication example. The account and token request and response examples were
added too, so no request on the page shows `"string"` in its fields.

**What this locks in for the rest of the project:** a new endpoint with an
error response and no example fails the schema-wide test. Examples are
checked against real responses, so a changed message or field fails a test.

**Carried into later tasks:**

* The schema test helpers (`get_schema`, `named_example`, `only_example`) are
  copied across the test files; moving them to one shared module is left for
  its own pull request
* The response examples are compared by field names only, so a change in a
  value's format, such as the expiry, is not caught
* The decimal pattern drf-spectacular generates for `concentration_value`
  stays as it is; the field description states the limits
