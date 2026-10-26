# Slice 1, task 1.7 — done

# Interactive API documentation

- `pyproject.toml`: `drf-spectacular`, with a floor like the other packages;
  `uv.lock` holds the exact version
- `src/config/settings.py`: `drf_spectacular` in `INSTALLED_APPS`, its
  `AutoSchema` as `DEFAULT_SCHEMA_CLASS`, and a `SPECTACULAR_SETTINGS` block
  with the title, description and version, `SERVE_PERMISSIONS` written
  explicitly as `AllowAny`, and the Swagger UI files loaded from the jsDelivr
  CDN with the version pinned in the URL, never `@latest`
- `src/config/urls.py`: `api/schema/` (`schema`) and `api/docs/`
  (`api-docs`), next to `healthz/`. Public URLs: `GET /api/schema/` and
  `GET /api/docs/`
- `src/users/serializers.py`: `LoginResponseSerializer`, which only describes
  the login response (token and expiry) in the schema
- `src/users/views.py`: `LoginView.post` annotated with `extend_schema`;
  `LogoutView` and `LogoutAllView`, empty subclasses of knox's views that
  only carry the schema annotation (`204`, no body)
- `src/users/urls.py`: `auth/logout/` and `auth/logoutall/` now point to
  those subclasses instead of knox's views. Paths, names and behaviour are
  the same as in `0023`
- Tests, 48 → 53, in `src/ops/tests/test_api_docs.py`:
  - the Swagger UI page opens without a token
  - the schema opens without a token
  - the schema lists the account and token endpoints
  - the schema documents logout and logout-all as `204` with no body
- The four logout tests in `src/users/tests/test_auth_views.py` pass
  unchanged
- `uv run pytest` — 53 passed. Total coverage 94% (180 statements, 10
  missed), the same 10 lines as in `0023`
- `uv run mypy` — `Success: no issues found in 33 source files`
- `uv run ruff format --check .` and `uv run ruff check .` — passed
- `manage.py spectacular --validate --fail-on-warn` — no errors or warnings
- `pre-commit run --all-files` — all passed
- Pull requests #19 and #20, each with `CI` green; Render deployed each
  merge
- Production, from outside:
  - `GET /api/docs/` without a token — `200`, `text/html`
  - `GET /api/schema/` without a token — `200`, OpenAPI 3.0.3, with the five
    account and token endpoints and the `knoxApiToken` scheme (`apiKey` on
    the `Authorization` header, prefix `Token`)
  - in the browser, "Authorize" with `Token <value>` for the account `id` 2,
    then `GET /api/users/me/` from the page — `200`,
    `{"id":2,"name":"Prova Tarefa"}`

**Deviations from the task text:**

- The test that the schema lists the account and token endpoints moved from
  the first pull request to the second: until login and logout carried their
  schema annotations, the schema left them out
- The second pull request also tests that both logouts are documented as
  `204` with no body

**What this locks in for the rest of the project:** the schema and the
Swagger UI page are public; every other route stays closed by default. A new
endpoint appears in the schema on its own, and one whose view the generator
cannot read gets an `extend_schema` annotation. The Swagger UI version only
changes through a commit.
