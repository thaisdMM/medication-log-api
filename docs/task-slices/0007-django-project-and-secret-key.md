# Slice 0, task 0.5 (part 1 of 2) — done

# Django project created inside `src`, secret key out of code

- Django installed as a project dependency (`uv add django`), version 6.1
- `environs[django]` installed as a project dependency, version 15.1.0 —
  chosen among three options for converting values to typed data compatible
  with strict mode
- `django-stubs[compatible-mypy]` installed as a dev dependency, version
  6.1.0 — `mypy` stayed at 2.3.1, no version change
- Django project created inside `src`
  (`django-admin startproject config src`): `config` package with
  `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`, plus `manage.py`
- `SECRET_KEY` no longer written in code: read from the `DJANGO_SECRET_KEY`
  variable via `env.str(...)`, with a visibly fake development default
- `.env` created at the root with the key moved into it; `.env` added to
  `.gitignore` **before** the file was created
- `pyproject.toml`: `[tool.mypy]` gained `plugins = ["mypy_django_plugin.main"]`;
  new `[tool.django-stubs]` section with
  `django_settings_module = "config.settings"`
- Both expected strict-mode errors fixed: `ALLOWED_HOSTS: list[str] = []` and
  `def main() -> None:` in `manage.py`
- `uv run mypy` — passed, 7 files checked
- `uv run ruff check .` and `uv run ruff format --check .` — pass
- `uv run python src/manage.py runserver` starts, Django's default page loads
  in the browser
- 18 pending migrations reported on server start — no migration applied
- `src/db.sqlite3` was created as a side effect of `runserver`'s
  pending-migration check (SQLite creates the file on connection, even with
  no tables inside) — added to `.gitignore` already in this part, ahead of
  what part 2 planned
- Commit split in two with `git add -p`, separating what `uv add` wrote from
  the two hand-written `pyproject.toml` lines (the `mypy` plugin and the
  `django-stubs` section)
- `git push` done and verified on GitHub: `.env` is not in the repository,
  and the `SECRET_KEY` line does not show the generated key

**What this locks in for the rest of the project:** the Django project
exists, runs locally, passes `mypy` strict mode with the Django plugin
enabled, and the project's first secret is already out of version control.
Part 2 continues the configuration from here.

**Carried into part 2 of this task:**

- Reading the rest of the environment-variable configuration
  (`DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DATABASE_URL`), creating
  `.env.example`, and re-checking `pre-commit`'s hooks
- Generating a new, strong production secret key and running Django's
  deploy check (`check --deploy`) — task 0.11
- Conflict between that check and console-based email delivery — slice 5
- Django 6.1's `MAILERS` format — slice 5
