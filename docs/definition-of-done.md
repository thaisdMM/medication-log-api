# Definition of done

What must be verified before a task or slice is done, on top of the slice rule
in `docs/task-slices/0001-roadmap.md` (no slice ends before its endpoint
responds in production).

## Every merged change to the application

- [ ] The deploy log shows the service live, and every new migration applied.
- [ ] `curl` from outside: `/healthz/` answers `200`, and each new endpoint
      answers as documented.

## Every endpoint that serves an account's data

- [ ] A test for each row of the response table in `docs/api-behaviour.md` that
      applies to the endpoint — at least the data owner and an account with no
      relation, which gets **404** on listing and on fetching by id.
- [ ] Creating a record that points at another account's data is refused in
      input validation — for example a usage period pointing at another
      account's medication.
- [ ] The endpoint declares its path to the owner. An endpoint that does not
      must fail on its first call (ADR 0005).
- [ ] A refused request answers 400 with a validation message, never 500.

## Medication

- [ ] A test saves the same medication twice, blank except for the name, and
      expects a duplicate error — 400 with a validation message, not 500. The
      database ignores `nulls_distinct` silently where unsupported, so only a
      test proves it acts (ADR 0008).

## Logs

- [ ] No name and no email in any log line. The hard case is the error log,
      which can carry a whole object with name and email inside without anyone
      writing it.

## Admin panel

- [ ] Registering medication, usage period, disease marks or sharing in the
      admin panel gives every `is_staff` account the health data of all
      accounts. Checked when the panel is built.
