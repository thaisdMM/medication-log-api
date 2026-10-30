---
status: accepted
date: 2026-08-24
decision-makers: Thaís
---

# Duplicate constraint with `nulls_distinct=False`

## Context and Problem Statement

The same account must not save the same medication twice. Uniqueness is
declared over owner + name + concentration value + concentration unit + form;
form is part of it, so two presentations of the same medication are two rows.

Only the name is mandatory. In PostgreSQL two `NULL`s are not equal by default,
so two incomplete registrations of the same medication pass the constraint.
Unit and form are closed-list text fields that store empty text, never `NULL`;
the concentration value is numeric, and it is the only column of the
combination that can be `NULL`.

## Considered Options

* **Declare in the database that empty equals empty** — `nulls_distinct=False`.
* **Accept the duplicate** and declare it in the README as a decision. Costs
  nothing; the list can show repeated rows.
* **Make the fields mandatory.** Ruled out: recording is optional beyond the
  medication name (`docs/domain-model.md`).

## Decision Outcome

Chosen option: **`nulls_distinct=False`**, because it solves the duplicate
without asking anything of the account.

The name is compared in a uniform case, not as the raw column: `Dipirona` and
then `dipirona`, the rest equal, is a duplicate, and the first keeps its
spelling. Declaring the constraint over an expression makes Django create a
unique index instead of a table constraint, and `deferrable` cannot be used
with it.

**Executed: the option acts.** PostgreSQL's `NULLS NOT DISTINCT` changes the
default; Django exposes it as `UniqueConstraint.nulls_distinct`, ignored on
databases other than PostgreSQL. The experiment and its result are in
`docs/task-slices/0027-nulls-distinct-experiment.md`.

### Consequences

* No field is made mandatory to close the constraint, under any hypothesis.
* `null=True` on unit or form opens the hole again.
* The option is ignored silently where unsupported, so a test is the only proof
  it acts (`docs/definition-of-done.md`).
* A closed Django tracker ticket reports that an expression yielding `NULL`
  combined with `nulls_distinct=False` is treated as distinct in Python
  validation while the database refuses it. Its resolution was not verified.
  The name is mandatory, so the expression never yields `NULL`.
* **Fallbacks if the experiment shows `nulls_distinct` does not act**, in order:
  1. A default value on form — "not informed" — which the database compares
     normally. It does not cover the concentration value: inventing a number to
     mean *not filled* gives hidden meaning to a value.
  2. Accept the duplicate and record it in the README.

## More Information

Archive address: ESTADO_CORRENTE §3 (23/08 option table), §3.1–§3.6, §13.5.
