# Slice 0, task 0.6 (part 1 of 2) — done

# Production image built with Granian, no database yet

- `granian` and `psycopg[binary]` installed as production dependencies
  (`uv add granian "psycopg[binary]"`): `granian` 2.8.2, `psycopg` 3.3.5,
  `psycopg-binary` 3.3.5 — neither in the `dev` group
- `uv tree --depth 1` confirmed the `dev` group unchanged: `django-stubs`,
  `mypy`, `pre-commit`, `ruff`
- `uv --version`: 0.12.6 — used as the tag on
  `COPY --from=ghcr.io/astral-sh/uv:0.12.6`, so the `uv` that builds the
  image matches the one that generated `uv.lock`
- `.dockerignore` created, with the three lines that matter most (`.env`,
  `.venv`, `src/db.sqlite3`) plus general hygiene entries (`venv/`, `env/`,
  `.pytest_cache/`, `htmlcov/`, `.coverage`, `.DS_Store`); also excludes
  `CLAUDE.local.md` and `.claude/skills/django-mentor/task-format.md` —
  same reasoning as `.env`, neither should ever be able to reach an image
- `Dockerfile` created: two-stage build, `python:3.14.7-slim-trixie` in
  both stages, `uv` binaries copied from `ghcr.io/astral-sh/uv:0.12.6`,
  `uv sync --locked --no-install-project` with the `dev` group excluded via
  `UV_NO_DEV=1`, `src/` copied as source with `PYTHONPATH=/app/src` (the
  installable package is `medication_log_api`, not `config`, so the project
  itself is never installed), non-root `app` user, `CMD` runs Granian with
  `--interface wsgi --host 0.0.0.0 --port 8000`
- `docker build -t medication-log-api .` — succeeded, 19/19 steps
- `docker run` tested with `-p 8001:8000` instead of `8000:8000` — host
  port 8000 was already taken locally by an unrelated project's container
  (`skillbridge-web-1`); the container's own port stays 8000, only the
  host-side mapping changed
- `curl -i http://localhost:8001/` → `HTTP/1.1 404 Not Found` — the full
  stack answered: Granian, then Django, then `urls.py` with no route for
  `/`
- `docker run --rm medication-log-api ls /app/.venv/bin` — has `granian`
  and `django-admin` (and `dotenv`, from `environs`); no `ruff`, `mypy`, or
  `pre-commit` — `UV_NO_DEV=1` confirmed working
- `docker image ls medication-log-api` — 232MB, recorded as the baseline
  for comparison once slice 1 adds DRF
- Committed: `.dockerignore` and `Dockerfile` as new files, `pyproject.toml`
  and `uv.lock` modified

**What this locks in for the rest of the project:** the application builds
into a production image without `runserver`, without dev tooling, and
without any secret or local artifact baked in — configured entirely by
environment variables passed at `docker run`, the same mechanism task 0.5
put in place. The image runs and answers a real HTTP request through
Granian and Django together.

**Carried into part 2 of this task:**

- `DATABASE_URL` still points at the local SQLite file inside the
  container — part 2 brings up PostgreSQL 18 alongside it
- The database default in `settings.py`, and its conflict with the
  no-`.env` check task 0.10 depends on — part 2
- Static files in production — Granian can serve them, not configured yet
  — task 0.11
- `psycopg[pool]` and Django's `"pool": True` option, alongside Neon's own
  pooling — task 0.11
- Granian's worker count, plus a new observation from this run: a startup
  warning about the default thread ceiling (512) being high relative to
  available CPU cores — task 0.11
