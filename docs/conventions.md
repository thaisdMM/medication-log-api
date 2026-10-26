
# Conventions

How code, tests, commits and pull requests are written in this project. Read
it before writing code, a test, a commit message or a pull request body. The
absolute rules for working on the project are in `CLAUDE.md`; this file does
not repeat them.

## Names

- A name says what the thing does or what happens, in the domain's words
  (`GLOSSARY.md`).
- No numbers in names: no status codes, no task, slice, ADR or record numbers.
  This holds for code, tests, commit messages, pull requests and repository
  documents. Name things by what they are: "the account and token endpoints",
  not "the slice 1 endpoints".

## Code

- Type hints on every function and method signature (`mypy --strict` runs in
  pre-commit and CI).
- One responsibility per class and per function. A function that does two
  things is split.
- No inline comments (`CLAUDE.md`, rule 7).
- Third-party classes are aliased on import when the project defines a class
  with the same name: `from knox.views import LoginView as KnoxLoginView`.

### Docstrings

Google style on every module, class, method and function of the application
code. Tests follow the rule under Tests.

- A docstring states **what** the code does: its behaviour, its inputs and
  outputs. Sections: `Args`, `Returns`, `Attributes`, `Raises`, only those that
  apply.
- It does not justify a design decision, argue against an alternative, explain
  framework internals or refer to an ADR. That reasoning belongs in
  `docs/adr/` or the task record.

```python
# Rejected: explains the decision
"""Use knox's views because its docs advise against altering them."""

# Accepted: describes the behaviour
"""Delete the token used in the request, so it stops working at once."""
```

## Dependencies and versions

- Direct dependencies are declared in `pyproject.toml` with a floor
  (`>=X.Y.Z`), the form `uv add` writes. The exact installed version lives
  only in `uv.lock`.
- No version number is copied into another file. To find one, search the lock
  for that package: `grep -A1 '^name = "<package>"' uv.lock`.
- A front-end asset loaded from a CDN has no lock file, so its exact version is
  written in its URL (`swagger-ui-dist@5.34.0`), never `@latest`.

## Tests

### Runner and layout

- `pytest` with `pytest-django`. Run one file with `--no-cov`:
  `uv run pytest src/users/tests/test_views.py --no-cov`.
- Tests live in `<app>/tests/`, one file per source module or per endpoint
  group: `test_models.py`, `test_serializers.py`, `test_views.py`,
  `test_auth_views.py`.
- Every test folder has an `__init__.py`.

### What to test

- Only decisions this project makes. Behaviour the framework or a library
  already guarantees is not tested again; the pull request lists it under
  "Not tested, as library behaviour".
- A test must fail when the behaviour it guards is removed. Every new test is
  seen failing once against a deliberate break — a throwaway pytest plugin
  outside the repository that monkeypatches the code — and passing without it.
- Endpoints are tested through the API with the `client` fixture, by what a
  caller sees: status and body.

### One behaviour per test

- When a test fails, its name alone says what broke. A name that needs "and"
  or "also" is two tests.
- Test names say what happens, with no status codes or numbers:
  `test_logout_makes_the_token_used_stop_working`, not
  `test_logout_returns_401`.
- Several assertions in one test are fine when they check facets of the same
  response. A precondition is asserted first (for example, the logout answered
  before its effect is checked).
- `@pytest.mark.parametrize` when the same assertion runs over different inputs;
  each case gets an `id` when the value alone does not say what it is.
- Test modules, tests and fixtures: a one-line docstring, the behaviour
  verified. A helper class inside a test file (such as a stand-in for the
  database connection) follows the application style.

### Fixtures

- Shared fixtures live in `<app>/tests/conftest.py`, in dependency order. A
  fixture used by one test file stays in that file.
- Data fixtures return a `dict` of valid input; tests override one field with
  `{**data, "field": value}`.
- Every fixture and test is annotated, built-in fixtures included
  (`client: Client`): `mypy --strict` checks the tests.

### Database

- `@pytest.mark.django_db` on every test that touches the database, even when
  a fixture it uses already does. Tests that do not touch it carry no marker.
- The transactional mode only when the test depends on real commits.

### Assertions on errors

- A message the project defines is asserted through its constant, never
  retyped: `[INVALID_CREDENTIALS_MESSAGE]`.
- A message that comes from Django or a library, with no constant in the
  project, is asserted as the response writes it:
  `"The password is too similar to the user name." in serializer.errors["password"]`.

## Commits

Conventional Commits, checked by the `commit-msg` hook.

```
<type>(<scope>): <main change, imperative, lower case, no full stop>

- <short line naming a file touched and what changed in it>
```

- **Types:** `feat`, `fix`, `refactor`, `test`, `docs`, `chore`. (`test`, not
  `tests`: the hook only accepts the standard types.)
- **Scope:** whenever the change has one: the app (`users`, `ops`, `config`)
  or, outside the apps, the area: `docs(adr)`, `docs(task-slices)`,
  `docs(readme)`, `docs(claude)`, `docs(conventions)`, `chore(ci)`,
  `chore(docker)`. A change that spans several areas has no scope
  (`docs: ...`). The scope is never a file; the file goes in the subject when it
  helps the reader.
- **Granularity:** one commit per change: production code with the tests that
  cover it, a model with its migration.
- **Body:** short, objective bullets, a few at most. They tell the reader which
  files the commit touches and what changed in each; they do not describe
  everything that was done or repeat the pull request.
- No task, slice, ADR or record numbers; ADRs by subject.
- No `Co-Authored-By`, "Generated with" or session trailers.
- The message is shown and approved before the commit is made.

## Pull requests

- One small pull request per piece of work, about 200 changed lines (lock files
  not counted).
- Body sections: **Summary**, **Tests**, **Choices**.
  - Summary: what the API does differently.
  - Tests: one line per test, the behaviour it proves.
  - Choices: each routine choice with its reason, then "Not documented: ..." and
    "Not tested, as library behaviour: ..." lines when they apply.
- Technical only, and approved before it is posted.
- Documentation-only changes go straight to `main`, without a pull request.
