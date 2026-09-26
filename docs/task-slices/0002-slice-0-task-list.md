# Slice 0 — the task list

**Written:** 2026-08-27

The tasks of slice 0, in order, with what each delivers and what breaks if it
goes wrong. Not a step-by-step — each task's step-by-step lives in its own
completion record (0003 onward in this same directory).

## Numbering rule

Task numbers are already cited inside approved files (the hosting ADR cites
tasks 0.6 and 0.11; the 0.1 completion record cites 0.2–0.5). **Tasks are
never inserted mid-list or renumbered.** A new task enters either inside an
existing one, when the subject belongs there, or appended at the end (0.12
onward).

## The list

| # | Task | Delivers | Breaks if wrong |
|---|---|---|---|
| 0.1 | Repository and environment with `uv` — done, see [0003](0003-repository-and-uv.md) | `medication-log-api` on GitHub, Python 3.14.7 pinned, `uv`-managed virtualenv, README, MIT license | removing `.venv` or a leaked secret from git history means rewriting the whole history |
| 0.2 | `ruff` as linter and formatter — done, see [0004](0004-ruff-linter-and-formatter.md) | one command flags and fixes style and dead code, configured in `pyproject.toml` | without it, 0.4 and 0.10 have nothing to run; formatting the project for the first time later produces one giant commit across every file |
| 0.3 | `mypy` for types — done, see [0005](0005-mypy.md) | one command complains when a function's declared and actual return types disagree | the more code exists before enabling it, the more expensive: every error surfaces at once |
| 0.4 | `pre-commit` tying the two together, plus the commit message convention — done, see [0006](0006-pre-commit-and-commit-convention.md) | a non-compliant commit does not happen on Thaís' machine; the message follows the convention promised in 0.1 | without it, the first place the error surfaces is 0.10 — after push, not before |
| 0.5 | Django project, configured by environment variable — part 1 done, see [0007](0007-django-project-and-secret-key.md); part 2 open | the project runs locally, no secret in code, an example file lists the variables it needs. No migration applied here | a secret in code costs the same as in 0.1; a migration applied here compromises 0.7 |
| 0.6 | Docker and Docker Compose with PostgreSQL | one command brings up the project and the database together, verified without creating a table | this is the artifact 0.11 deploys |
| 0.7 | The custom user model, before the first migration | an account table keyed by email, no username field, recognized by Django as the user model. This is the project's first migration | replacing the user model after data exists is one of Django's most destructive migrations |
| 0.8 | `pytest` with coverage reporting | one command runs the tests and reports how much code they exercise | without tests, 0.10 has nothing to gate on |
| 0.9 | Health endpoint, with a test | a URL reports the system is up, verified by an automated test | this is what 0.11 uses to prove the deploy worked; without it, "it's live" is opinion |
| 0.10 | CI that blocks merge — in two halves | automation runs tests, style and types on every push, **and** a branch protection rule blocks merging without it green. Work moves to branches with pull requests from here | the first half alone blocks nothing: CI goes red and the merge happens anyway |
| 0.11 | Platform configured, production responding, redeploying on every merge to main | the health endpoint responds publicly, backed by the real Neon database, redeploying automatically on merge | discovering late that the platform doesn't work means redoing configuration, database and CI with the whole project on top |
| 0.12 | User model behavior tests — done, see [0013](0013-user-model-behavior-tests.md) | an automated test suite for `UserManager.create_user` and `create_superuser`: persistence, uniqueness, validation errors, password hashing, default and admin flags read from the database, and the authentication contract | a regression in user creation, password hashing or authentication surfaces only in production, with no automated signal before it |

## The rule that spans the whole slice

**No table-creating command runs before task 0.7** — not `migrate`, not
`createsuperuser`. Django prints a warning about pending migrations on first
run; obeying it lets Django's default user tables get created before the
custom model of 0.7 exists. Today the fix is deleting the database and
starting over, affordable only because no data exists yet — which is exactly
why this must happen in slice 0.

## What task 0.11 verifies

Tracked in `docs/open-questions.md`, "Hosting: pending verifications for task
0.11" — a fourth item was added on 2026-08-27: whether Render's free plan
redeploys automatically on every merge to main. If that turns out to be
separate work, it becomes task 0.12, appended per the numbering rule above.

## Decisions recorded in this document's source conversation

* Python 3.14.7 is compatible with Django 6.1 — confirmed against Django
  6.1's official release notes (2026-08-05), which declare support for
  Python 3.12, 3.13 and 3.14.
* Production redeploys automatically on every merge to main.
* The local container in 0.6 runs the same major PostgreSQL version as
  production; the exact number is confirmed by task 0.11's verification 3.

## Still open

* Test coverage: report only, or does CI fail below a threshold? — task 0.10.

## What comes after

Slice 1 planning starts once slice 0 is live — one slice planned at a time.

## What this slice does not deliver

No feature. Slice 0 is the project's only non-vertical slice, by design. DRF,
token authentication, the interactive API documentation, and every model but
the user model belong to slice 1 onward.

## Addendum — 2026-09-26: slice 0 closed

This document is kept as written on 2026-08-27. Nothing above was edited.
What changed after it was written is recorded here.

1. **Every task is done.** Completion records: 0.5 part 2 —
   [0008](0008-environment-variable-configuration.md); 0.6 —
   [0009](0009-production-image-with-granian.md) and
   [0010](0010-postgres-service-and-required-database-url.md); 0.7 —
   [0011](0011-custom-user-model-and-first-migration.md); 0.8 —
   [0012](0012-pytest-and-coverage-report.md); 0.9 —
   [0014](0014-health-endpoint.md); 0.10 —
   [0015](0015-ci-workflow-and-branch-protection.md); 0.11 —
   [0016](0016-production-on-render-and-neon.md). Record numbers follow
   completion order, which is why 0.12's record (0013) comes before 0.9's.
2. **"Production redeploys automatically on every merge to main" no longer
   holds as written.** Render deploys "After CI Checks Pass": every merge
   to main that runs the CI workflow redeploys. A documentation-only merge
   skips CI under `paths-ignore`, Render detects no check, and nothing is
   published. See [0016](0016-production-on-render-and-neon.md).
3. **The fourth hosting verification did not become task 0.12.** It was
   closed inside task 0.11 (see `docs/open-questions.md`). The number 0.12
   went to the user model behavior tests instead.
4. **PostgreSQL version:** production runs PostgreSQL 18 (`18.6`, from
   `SELECT version()` in Neon), the same major version as the local
   container.
5. **Test coverage:** report only, no minimum threshold — decided by Thaís on 2026-09-17, during task 0.10's planning. Not recorded in 0015.
