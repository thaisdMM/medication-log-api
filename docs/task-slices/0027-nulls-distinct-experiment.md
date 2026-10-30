# Slice 2, task 2.1 — done

# `nulls_distinct=False` experiment

- No code changed in the repository: the experiment ran on a throwaway model,
  with no migration and nothing committed. The script is kept outside the
  repository
- Run on 2026-10-26 against the project's PostgreSQL (compose service `db`,
  the test database created by `pytest-django`): Django 6.1.2, Django REST
  framework 3.18.3, PostgreSQL 18.6
- The constraint under test is the one of the duplicate rule:
  `UniqueConstraint(F("owner"), Lower("name"), F("concentration_value"),
  F("concentration_unit"), F("form"), nulls_distinct=False)`, next to a control
  model with the same constraint and the default `nulls_distinct`
- Django created a unique index:
  `CREATE UNIQUE INDEX ... (owner_id, lower((name)::text), concentration_value,
  concentration_unit, form) NULLS NOT DISTINCT`
- Fact 1: `nulls_distinct=False` acts. Two rows equal except that both have no
  concentration value: the database refuses the second with an
  `IntegrityError` (duplicate key). The control model accepts it
- Fact 2: `full_clean` catches the duplicate and raises `ValidationError`
  (`__all__`, constraint violated). A `ModelSerializer` over the model does
  not: it does not call `full_clean`, and Django REST framework builds no
  validator for a constraint declared over expressions, so `is_valid()`
  returns `True` and `save()` raises the `IntegrityError` from the database,
  so the API would answer 500 until the serializer validates the constraint
- Fact 3: closed-list fields left unchosen store `''` through the ORM and
  through the serializer. The concentration value stores `NULL`
- Case-insensitive name: `dipirona` after `Dipirona`, rest equal, is refused
  the same way in `full_clean` and in the database, with and without a
  concentration value. The first row keeps its spelling
- `docs/domain-model.md` and `docs/open-questions.md` already carry the
  outcome, from the slice 2 task list

**Deviations from the task text:** none.

**What this locks in for the rest of the project:** the duplicate constraint of
the duplicate-constraint ADR is declared with `nulls_distinct=False` and its
fallbacks are not needed. The database enforces the rule, so the model
migration needs no workaround. Validation has to catch the duplicate before
the database does, or the API answers 500 — the serializer task.
