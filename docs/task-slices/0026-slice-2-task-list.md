# Slice 2 — the task list

**Written:** 2026-10-27

The tasks of slice 2, in order, with what each delivers and what breaks if
it goes wrong. Not a step-by-step — each task's step-by-step lives in its
own completion record.

## What the slice delivers

From `0001`: an account registers its own medications, never sees anyone
else's, cannot register the same one twice, and gets 404 on what isn't
theirs. The slice ends only when this runs in production.

## Numbering rule

Same as `0002`: tasks are never inserted mid-list or renumbered. A new task
enters inside an existing one, or appended at the end (2.9 onward).

## The list

| # | Task | Delivers | Breaks if wrong |
|---|---|---|---|
| 2.1 | Experiment record | the `nulls_distinct=False` experiment recorded: the three facts, the versions used | ADR 0008 keeps resting on documentation only, with no record of the run |
| 2.2 | Medication model and duplicate constraint | app `medications`; the model with owner (`PROTECT`), name, concentration value and unit, form and state; the case-insensitive duplicate constraint with `nulls_distinct=False`; its migration. Branch and pull request | with a default unique constraint, two registrations of the same medication with only the name filled in pass, because the concentration value stays `NULL` and one `NULL` is not equal to another; `null=True` on unit or form opens the same hole |
| 2.3 | Owner filter mixin | a view mixin that filters every query by a declared `owner_path`; a view without it raises `ImproperlyConfigured` on its first call. Branch and pull request | a filter written by hand in each view is forgotten in one, and that view leaks another account's data in silence |
| 2.4 | Medication serializer | trimmed name, a name of only spaces refused; concentration greater than zero with at most three decimal places, returned without trailing zeros; a duplicate answers 400, never 500; the owner set by the system and never returned. Branch and pull request | a `ModelSerializer` alone lets the duplicate reach the database, and the API answers 500 |
| 2.5 | List and create | `GET` and `POST /api/medications/`: every medication of the account, alphabetical ignoring case, optional `?state`; 401 without a token; another account's medications never listed. Branch and pull request | a list without the owner filter returns every account's medications |
| 2.6 | Retrieve, update and delete | `GET`, `PUT`, `PATCH` and `DELETE /api/medications/<id>/`; 404 on another account's medication; 401 without a token. Branch and pull request | 403 instead of 404 tells another account the medication exists |
| 2.7 | Interactive documentation and README | the medication endpoints on the Swagger UI page, with the possible values of each closed list; the README describes what is live | the page lists endpoints whose fields it does not describe |
| 2.8 | Slice proven in production | create, list, retrieve, update, delete, the duplicate 400 and another account's 404 run against the public address; the slice closes in its record | without it, "slice 2 is live" is opinion |

## Decisions

* Operations: list, create, retrieve, update (`PUT` and `PATCH`) and
  delete. Resuming is `PATCH {"state": "in_use"}`, no endpoint of its own.
* Owner foreign key: `on_delete=PROTECT`.
* Name: leading and trailing spaces trimmed; casing never changed
  (non-goals item 13).
* Concentration value: a decimal greater than zero, stored with three
  decimal places, returned without trailing zeros (`"50"`, `"0.025"`).
  Three places hold strengths written in micrograms, such as 25 mcg as
  `0.025` mg.
* Concentration unit: mg · g · ml · other (roadmap revision 2).
* Form: tablet · capsule · drop · ml · sachet · patch · suppository ·
  ointment · other, no default. An unchosen unit or form stores `''`.
* State: optional on create, `in_use` when not sent.
* List: unpaginated, alphabetical by name ignoring case, optional
  `?state=in_use` or `?state=suspended`.
* Closed-list fields answer with their stored code only.
* Duplicate: 400 from the serializer, `{"non_field_errors": [<fixed
  message>]}`, without the existing medication's `id`.
* Owner filter: a view mixin with a required `owner_path` (ADR 0005).
* Medication is not registered in the admin panel.

## Carried, not part of this slice

* Usage periods: the model is not created in this slice (`0001`, the named
  trap).
* Converting `/healthz/` to DRF (`0014`).
* Logging configuration. ETAPA2 B4 holds meanwhile: no project code
  writes logs.
