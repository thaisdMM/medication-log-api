# Slice 0, task 0.6 (part 2 of 2) — done

# PostgreSQL 18 alongside the application, and a required `DATABASE_URL`

- PostgreSQL published on host port `5434`, not the planned `5433`: `lsof`
  showed `5433` taken by the SkillBridge project, whose `db` service
  publishes `5433:5432`; `5432` and `5434` were free. Only the host side of
  the mapping changed
- `compose.yaml` created at the root, two services: `db` (`postgres:18`) and
  `web` (`build: .`)
- `postgres:18` pins the major version only — Neon applies minor upgrades on
  its own, and pinning the minor locally would diverge from production
- `db` volume: named volume `postgres-data` mounted at
  `/var/lib/postgresql`, the version-18 path, not `/var/lib/postgresql/data`.
  `PGDATA` confirmed as `/var/lib/postgresql/18/docker` in the initdb log
- `db` healthcheck: `pg_isready` with `$$` escaping, `interval: 5s`,
  `timeout: 5s`, `retries: 10`, `start_period: 10s`
- `web`: `depends_on: db: condition: service_healthy`, and `DATABASE_URL`
  assembled inside `compose.yaml` from the `.env` pieces, pointing at
  `db:5432` — service name and internal port, so the password is not written
  twice
- `settings.py`: `env.dj_db_url("DATABASE_URL")`, with
  `default="sqlite:///db.sqlite3"` removed. No fallback database
- `.env`: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` and
  `DATABASE_URL` added, the URL pointing at `localhost:5434` — the published
  port, which is what host-side `uv run mypy` and `manage.py check` use
- `.env.example`: same four variables with placeholder values, declared once
- `manage.py check` with `.env` moved aside — fails at settings import:
  `environs.exceptions.EnvNotSetError: Environment variable "DATABASE_URL"
  not set`. With `.env` in place — `System check identified no issues (0
  silenced)`
- `docker compose up --build` — startup order confirmed: db initialized,
  then `Container medication-log-api-db-1 Healthy`, then Granian
  `Listening at: http://0.0.0.0:8000`
- `docker compose ps` — `db` `Up (healthy)`, `0.0.0.0:5434->5432/tcp`; `web`
  `0.0.0.0:8001->8000/tcp`. Only `db` declares a healthcheck, so only `db`
  reports a health state
- `SELECT version()` through Django's own connection →
  `postgresql -> PostgreSQL 18.6 (Debian 18.6-1.pgdg13+2) on
  aarch64-unknown-linux-gnu`
- `curl -i http://localhost:8001/` → `200 OK` with Django's welcome page and
  `server: granian`, not the `404` of part 1: Compose passes
  `DJANGO_DEBUG=True` from `.env`, while part 1's `docker run` passed no
  environment variables and fell back to `DEBUG=False`
- `psql -c "\dt"` → `Did not find any tables.`; `ls src/` in the `web`
  container → `config manage.py medication_log_api`, no `db.sqlite3`
- Granian's startup warning about the 512-thread ceiling appeared again,
  unchanged from part 1

**What this locks in for the rest of the project:** one command brings up the
application and PostgreSQL 18 together, in the right order, with Django
reaching the real database. `DATABASE_URL` is mandatory everywhere — a
missing value stops the project at import time instead of silently
redirecting it to a local file. Task 0.7 inherits an empty database.

**Carried into later tasks:**

* First migration and the custom user model — task 0.7, which finally creates
  tables
* `DATABASE_URL` must exist in the CI environment, now that no default covers
  its absence — task 0.10
* `DATABASE_URL` must exist in the Render dashboard, for the same reason —
  task 0.11
* A test asserting `404` on `/` would fail under Compose, where
  `DJANGO_DEBUG=True` makes that route answer `200` — tasks 0.9 and 0.10
* Static files in production — task 0.11
* Granian's worker count and the thread-ceiling warning — task 0.11
* `psycopg[pool]` and Django's `"pool": True`, alongside Neon's own pooling —
  task 0.11
