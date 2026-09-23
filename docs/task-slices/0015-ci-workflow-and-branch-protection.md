# Slice 0, task 0.10 — done

# CI workflow and branch protection rule on main, proven to block merges

- `.github/workflows/ci.yml` created: workflow `CI`, triggered on `push`
  and `pull_request` targeting `main`, both with `paths-ignore` for
  `**.md` and `docs/**`
- Three jobs, each on a fresh `ubuntu-latest` machine (`permissions: {}`
  at the workflow level, `contents: read` per job): `quality` (`ruff
  check`, `ruff format --check`, `mypy`), `tests` (PostgreSQL 18
  service, `pytest`, `makemigrations --check`), `build` (`docker
  build .`)
- In `quality` and `tests`, every step after the first carries
  `if: ${{ !cancelled() }}`, so a failure early in the job does not
  skip the checks that come after it — each one still runs and reports
  its own result
- Actions pinned by full commit SHA (`actions/checkout`,
  `astral-sh/setup-uv`); `uv` fixed at `0.12.6`; Python installed from
  `.python-version`
- `DATABASE_URL` set in both `quality` and `tests`, as literal
  non-secret values — the database exists only for the job's lifetime;
  `quality` needs it because `mypy`/`django-stubs` import `settings.py`,
  no connection opened
- Pushed directly to `main` — the last direct push to `main` planned
  for this project
- Classic branch protection rule added on `main` (Settings → Branches):
  only "Require status checks to pass before merging" enabled,
  requiring `quality`, `tests` and `build`. No pull-request requirement,
  no strict/up-to-date requirement, no bypass restriction
- A disposable branch opened a pull request against `main` to prove the
  rule blocks each required check on its own, one push at a time:
  `quality` failing first (all three of its steps, to prove none are
  skipped), then `tests` failing alone, then `build` failing alone —
  each push showed the pull request's merge box blocked, with the
  owner-only bypass checkbox visible and left unchecked
- No application code, test or `Dockerfile` change reached `main` from
  that pull request: it was closed without merging, and both the
  GitHub and local copies of the branch were deleted. `main` ended at
  the same commit it started at

**What this locks in for the rest of the project:** every push and
pull request against `main` is checked for lint, formatting, types,
tests, missing migrations and a buildable image — and nobody without
owner bypass can merge while any of the three is red, proven per check,
not just configured.

**Carried into later tasks:**

* This record's own pull request — documentation only — is the
  project's first real pull request and the first exercise of
  `paths-ignore` skipping the CI
* Branch naming convention — not created
* Whether Render republishes on a doc-only push to `main` — task 0.11
* `migrate --check` against the production database — task 0.11
* `check --deploy` reproving the console email backend — task 0.11 and
  slice 5
* README: the protection blocks collaborators, not the owner; where
  `paths-ignore` comes from — slice 6
* Required tests limited to what's costliest to get wrong;
  `docs/definition-of-done.md` doesn't exist yet — slice 1
