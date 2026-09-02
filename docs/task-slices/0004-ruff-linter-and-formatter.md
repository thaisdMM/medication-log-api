# Slice 0, task 0.2 — done

# `ruff` as linter and formatter

- `ruff` installed as a dev dependency (`uv add --dev ruff`), version 0.16.5
- Configuration in `pyproject.toml`:
  - `[tool.ruff]` with `line-length = 88`
  - `[tool.ruff.lint]` with `extend-select = ["I", "UP", "C4"]`
  - `[tool.ruff.format]` empty
- No `ruff.toml` or `.ruff.toml` file created
- `uv run ruff check .` — passed with no findings
- `uv run ruff format --check .` — files already formatted
- `pyproject.toml` metadata adjusted in this task: email removed from
  `authors`, `description` filled in

**What this locks in for the rest of the project:** style and dead-code
tooling wired in while the project is still empty — avoids the large, late
formatting commit described in the task. Configuration living only in
`pyproject.toml` avoids the silent trap of a competing `ruff.toml`.
