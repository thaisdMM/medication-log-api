# Open Questions

What is not decided yet, which slice it blocks, and what is already known.
Ordered by the slice that needs the answer. A closed question moves to the
document that holds its answer.

## Slice 2 — Does `nulls_distinct=False` act? (the experiment)

Blocks: the medication model. First task of slice 2.

ADR 0008 rests on documentation read, never on code run. Run against the
project's PostgreSQL and Django, with the duplicate constraint declared:

| # | Prove | What the answer decides |
|---|---|---|
| 1 | Two rows equal except that both have no concentration value — does the database refuse the second? | Whether `nulls_distinct` acts. If not, ADR 0008's first fallback applies: form gets a default value, which becomes a tenth item of the form list |
| 2 | Is the refusal raised in Python validation (`full_clean`, serializer), or only as an `IntegrityError` from the database? | Whether the API answers 400 or 500 |
| 3 | Does a closed-list field left unchosen store `''` or `NULL`? | Confirms the empty-text rule of `docs/domain-model.md` |

It also settles whether a case-insensitive name expression that yields `NULL`
is treated as distinct in Python validation while the database refuses it. The
name is mandatory, so the expression should never yield `NULL`.

Until it runs, the form list and the empty-text rule are a working hypothesis.

## Slice 2 — Which concentration units beyond mg, g, ml?

Blocks: the unit list. Decided so far: mg, g, ml, other. Candidates: mcg,
international unit, mg/ml.

## Slice 3 — Which values does frequency accept?

Blocks: the frequency field. Decided so far: it is structured — a count and a
time unit. Candidates for the time unit: daily, weekly, specific days.

## Slice 3 — Does frequency have an "other" option?

Blocks: the frequency field. If it has one, it carries no free text, as in every
closed list of the project.

## Slice 3 — Does any rule replace "no two active usage periods"?

The rule forbidding two active usage periods of the same medication is dropped
(`docs/domain-model.md`). Whether another rule replaces it, or none does, is
open.

## Slice 7 — How does the backend know which account a conversation belongs to?

Blocks: the Telegram integration — the only open blocker of a decided feature.
No source decides the mechanism. What is known: the account starts the
conversation from its own phone, because a bot cannot start one. The answer may
add a column or a table.

## Slice 7 — Does the webhook survive the free tier's hibernation?

The free web service hibernates after 15 minutes idle and takes about a minute
to wake (ADR 0001). Telegram has a time limit for a webhook to answer and a
retry policy on failure. To research: that limit, that policy, and whether the
wake-up fits inside them. ADR 0001 reserves a €5–10/month valve for the web
service if hibernation becomes a real problem.

## Closed — Hosting: pending verifications for task 0.11

Source: `DECISAO_HOSPEDAGEM.md`, partly closed by ADR 0001. From ETAPA2 A9.

- [x] Whether Render deploys from the project's `Dockerfile`. Closed by
  task 0.11, step 6: Language set to Docker, built from the repository's
  `Dockerfile`. See `docs/task-slices/0016`.
- [x] How the Neon database URL is set as an environment variable in
  Render's dashboard. Closed by task 0.11, step 6: pasted as
  `DATABASE_URL` under Advanced → Environment Variables. See
  `docs/task-slices/0016`.
- [x] Confirm in Neon's dashboard (not documentation) that the created
  project runs PostgreSQL 15+. Closed by task 0.11, step 4:
  `SELECT version();` in the SQL Editor returned `PostgreSQL 18.6`. See
  `docs/task-slices/0016`.
- [x] How production redeploys automatically on every merge to main,
  and whether Render's free plan supports it (added 2026-08-27). Closed
  by task 0.11, step 11 and the order proof in step 14: Auto-Deploy set
  to "After CI Checks Pass", confirmed on the free plan — no separate
  task 0.12 needed. See `docs/task-slices/0016`.
