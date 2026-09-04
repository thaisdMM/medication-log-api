# Slice 0, task 0.5 (part 2 of 2) — done

# Environment variable configuration and the example file

- `DEBUG` no longer hardcoded: read via `env.bool("DJANGO_DEBUG", default=False)`
- `ALLOWED_HOSTS` no longer hardcoded: read via
  `env.list("DJANGO_ALLOWED_HOSTS", default=[])`, type annotation kept
- `DATABASES["default"]` no longer a hand-written dict: read via
  `env.dj_db_url("DATABASE_URL", default="sqlite:///db.sqlite3")` —
  `environs[django]`'s single-line database URL parser
- `.env.example` created at the root: lists all four variables
  (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`,
  `DATABASE_URL`) with no real values, English comments, written from the
  variable list rather than copied from `.env`
- `.env` now has three variables: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=True`,
  `DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost` — `DATABASE_URL` intentionally
  absent locally, since the code default already points at the local
  SQLite file
- `src/db.sqlite3` already covered by `.gitignore` from part 1; no new
  entry needed in this part
- `uv run mypy` — passed, 7 files, including with `.env` temporarily
  removed (`manage.py check` also passed with `.env` removed)
- `uv run ruff check .`, `uv run ruff format --check .`,
  `uv run pre-commit run --all-files` — all pass; the `mypy` hook has
  `pass_filenames: false` in `.pre-commit-config.yaml`, confirmed not to
  diverge from the manual `uv run mypy` (ignores changed-files list, keeps
  respecting `files = ["src"]` in `pyproject.toml`)
- `conventional-pre-commit` hook (`stages: [commit-msg]`) confirmed to not
  run under `--all-files`, by design — only the commit-msg stage triggers it
- Verified in execution, Django 6.1: `runserver` refuses to start only when
  **both** `DEBUG=False` and `ALLOWED_HOSTS` is empty — an explicit check at
  the start of the `runserver` command itself (`CommandError`, raised before
  system checks run). This is separate from the per-request `Host` header
  check (`get_host()`), which returns `400` per request instead and doesn't
  block startup. `DEBUG=False` alone, or an empty `ALLOWED_HOSTS` alone, is
  not enough to reproduce the refusal.

**What this locks in for the rest of the project:** task 0.5 is done in
full. All per-environment configuration (secret key, debug mode, allowed
hosts, database address) now comes from environment variables with safe
defaults, and `.env.example` documents the full list for anyone cloning the
repository. The project runs identically with `.env` present or absent,
which is the condition slice-0's automation and hosting tasks depend on.

**Carried forward:**

- Replace the local SQLite default with the containerized PostgreSQL address
  — task 0.6
- First test of the project — task 0.9
- CI relies on `mypy`/`manage.py check` passing with no `.env` file, already
  verified here — task 0.10
- Fill `DJANGO_ALLOWED_HOSTS` with the platform's real address, generate a
  strong production `DJANGO_SECRET_KEY`, and run `check --deploy` in the
  platform's environment — task 0.11
- `check --deploy` rejects console-based email delivery, which the current
  state document keeps for production — conflict to resolve in slice 5
- Django 6.1's `MAILERS` setting uses a different shape than the current
  state document's §8 — slice 5
- Document how to fill `.env` from `.env.example` in the README — slice 6
