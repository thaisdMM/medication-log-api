# Medication Log API — Engineering Rules

## Project context

Single repository. Application code lives in `src/`.

The stack and tools are deliberately not listed here — anything written into
this file goes stale and becomes the exact error rule 10 exists to prevent.

## Project documentation

**Read at the start of every task:**

- `pyproject.toml` — the stack, the tools, and their declared versions.
- `docs/task-slices/0001-roadmap.md` — what the whole project plans to build.
- The most recent slice task list in `docs/task-slices/`
  (`NNNN-slice-N-task-list.md`) — what the current slice proposes.

**Read only when the task touches the subject:**

- `GLOSSARY.md` — naming anything in the domain.
- `docs/domain-model.md` — models, fields, required values.
- `docs/api-behaviour.md` and `docs/definition-of-done.md` — any endpoint.
- `docs/open-questions.md` — before deciding anything in the current slice.
- `docs/non-goals.md` — when scope is in doubt.
- `docs/adr/` — list the filenames first; each name states its decision. Open
  only the ADRs whose name matches the subject of the task.
- Earlier task records in `docs/task-slices/` — only when needed.

## Absolute rules — apply to every persona, every session

1. **Never infer. Never assume. Never fill gaps.**
   If information is missing, incomplete, or ambiguous, stop and ask one
   focused question. Do not complete, extrapolate, or "fill in" what seems
   logical from context. This rule covers **missing or unclear information**:
   you do not have what you need to proceed.
   An incorrect assumption costs more tokens to fix than a question costs to ask.

2. **Always read the relevant files. Never pattern-match from training data.**
   When answering any question about the codebase or making any change to it,
   read every file that is relevant to the answer — not just the snippet
   pasted in chat. This project makes deliberate choices that differ from
   Django defaults; those choices are recorded in the project documentation,
   not in training data. Defaulting to the "usual" pattern is a violation of
   this rule.
   - **Read the full file, not just the visible snippet.** If a fragment, a
     class, or a method is shared, open the complete file before responding.
     Inheritance and imports usually carry information that is not visible
     in the snippet.
   - **Read across the inheritance chain.** When a concrete model is the
     subject of the question, also read its abstract base and any validators
     or managers it uses.

   Reading a file costs less than rewriting a wrong answer. If a tool call
   to read a file would resolve uncertainty, make the tool call — do not infer.

3. **Explain before you write.**
   Present the proposed approach in bullet points. Wait for explicit approval
   before generating any code.

4. **Never modify anything beyond the exact scope of the task.**
   If a change outside scope is needed, explain why and ask for permission
   before touching anything.

5. **Ask before choosing between valid options.**
   When a task requires choosing between patterns, libraries, or approaches
   that are not explicitly defined in the conventions, stop and ask. This
   rule covers **decisions between valid alternatives**: you have the
   information, but more than one path is reasonable and the user must decide.
   One focused question at a time.

6. **English only.**
   All code, variable names, comments, docstrings, commit messages, and
   repository documents must be in English.

7. **No inline comments unless strictly necessary.**
   What needs to be said belongs in the docstring. Only add an inline comment
   when the code cannot be understood without one — and even then, question
   whether the code should be rewritten to be self-explanatory first.

8. **Follow existing patterns.**
   Before writing anything new, read the relevant existing file to understand
   the established pattern. Do not introduce conventions that differ from
   what already exists.

9. **Never write code you suspect may be deprecated.**
   A version being current does not make every API inside it current. If a
   method is superseded within the version in use, do not propose it.

10. **Verify the version in use before proposing any code.**
    Training data lags this stack. Before suggesting or applying any API,
    method, setting, pattern, or command, read the version actually in use:
    `pyproject.toml` for the declared floor, `uv.lock` for the resolved
    version.

    `uv.lock` is long. Read **only** the `name` and `version` lines of the
    packages involved — never load the whole file.

    If the resolved version is outside what training covers, read the
    official documentation for that exact version before answering.

    This rule fires on every proposal, not only on uncertain ones. The
    failure it exists to catch is a confident answer built on an older
    version — which, being confident, never triggers rule 1.

11. **Never generate or run migrations without explicit approval.**
    Migrations are irreversible in production. Propose the migration, explain
    the impact, and wait for confirmation before generating or executing
    anything.

12. **Never run commands that modify state without permission.**
    This includes installs, file deletions, and edits to configuration files.

## Rule 1 vs Rule 5 — clarification

These rules look similar but cover different situations:

- **Rule 1** applies when information is **missing**: a field is undefined,
  a path is unclear, a requirement is ambiguous. You cannot proceed because
  you do not know what is true.

- **Rule 5** applies when the information is **there but a choice remains**:
  two valid patterns exist, two libraries could solve the problem, two
  layers could own a rule. You can proceed, but the user must choose the
  direction.

When in doubt, treat the situation as rule 1 and ask.

## Writing an Architecture Decision Record

The rules for turning a decision into an ADR are not in this file. They live in
the `adr` skill, at `.claude/skills/adr/SKILL.md`.

That skill carries `disable-model-invocation: true`, so its description never
enters context and it cannot be loaded automatically. Only the user loads it, by
typing `/adr`. This note exists because without it nothing in context would
reveal that the skill exists at all.

**Before writing or amending any ADR, that skill must be loaded.** If it has
not been, stop and ask for it — do not write the record from memory of what an
ADR usually looks like.
