# Slice 0, task 0.4 — done

# `pre-commit` tying linter and types together, plus the commit message convention

**Commit:** `15d9437`

- `pre-commit` installed as a dev dependency (`uv add --dev pre-commit`),
  version 4.6.2
- `.pre-commit-config.yaml` created at the root, with four hooks:
  `ruff-check`, `ruff-format` and `mypy` (local, via `uv run`), and
  `conventional-pre-commit` (`compilerla/conventional-pre-commit`, `v4.4.0`)
- `default_install_hook_types: [pre-commit, commit-msg]` — installs both hook
  points at once
- `uv run pre-commit install --install-hooks` — installed at
  `.git/hooks/pre-commit` and `.git/hooks/commit-msg`
- `uv run pre-commit run --all-files` — all three code hooks pass
- Tested with `git commit --allow-empty -m "testing the hook"` — rejected by
  the message hook, nothing recorded
- Commit message convention settled: Conventional Commits 1.0.0, scope
  optional, type chosen by whether the commit has a single target or not
- The tool's eleven standard types accepted, unrestricted

**What this locks in for the rest of the project:** code outside `ruff`'s or
`mypy`'s standard, or a message outside the convention, does not become a
commit on Thaís' machine — the error stops on screen, not in history.

**Note:** `pre-commit` runs at two separate points per commit (`pre-commit`,
then `commit-msg`), and each point stashes and restores any change outside
`git add` — hence the temporary-file message appearing twice. Expected
behavior, not a fault.

**Carried into later tasks:**
* Repository-hygiene hooks (large file, private key) — Thaís' decision,
  outside this task's scope
* Re-checking the hooks once `django-stubs` is installed — task 0.5
* Writing the commit convention into `README.md`, in English — slice 6
* Running the same checks on the server — task 0.10
