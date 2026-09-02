# Roadmap — the map of slices

**Date:** 2026-08-26

This is the execution order of the project, slice by slice, with the reason
for each position. It carries no tasks, no step-by-step, no hour estimates —
each slice is detailed once the previous one is live.

## The map

| # | Slice | What exists at the end that did not exist before |
|---|---|---|
| 0 | Tooling, user model, address live | reproducible environment, CI that blocks merge, a production URL responding — with the custom user model created and migrated, no feature yet |
| 1 | Registration and token login | an account signs up with email and password, requests a token, and uses it to authenticate. Includes the interactive API documentation, which grows on its own from here |
| 2 | Medication — the project's core | an account registers its own medications, never sees anyone else's, cannot register the same one twice, gets 404 on what isn't theirs |
| 3 | Usage period | an account logs when it took each medication; ownership is discovered through the medication |
| 4 | Disease | a disease table only the admin feeds; an account marks its own |
| 5 | Sharing | one account invites another, with scope; the invitee accepts, reads what was granted; the owner ends it at will |
| 6 | README and verification walkthrough | whoever gets the link can run, alone, the sequence that ends in 404, and read the project's decisions, non-goals included |
| 7 | Telegram | a command to the bot returns the sender's own list |

## Why this order

The criterion: what is most expensive to get wrong here — not what is hardest,
what costs the most to undo.

**Slice 0 first**, because two of its parts are practically irreversible: the
user model (replacing it after data exists is one of Django's most destructive
migrations) and the deploy platform (discovering in week six that the chosen
platform doesn't work means redoing configuration, database and CI with the
whole project on top).

**Authentication next**, because nothing below it has an owner — every table
carries, directly or indirectly, the account it belongs to.

**Medication before everything else**, because it is where the project proves
what it exists to prove. Three structural pieces are born together here: the
owner column, the single-point owner filter, and the database-level duplicate
constraint. The still-unrun experiment on form defaults is this slice's first
task, not the previous one's, since it needs Django and PostgreSQL already up.

**Usage period before disease**, counterintuitively: disease is simpler (one
table, one many-to-many, the admin panel). Usage period is the hard case,
because it's the only resource whose owner is indirect — no owner column,
reached through the medication. If the single-point filter has a defect, it
surfaces here. Cheaper to find it with two resources than with four.

**Sharing after the three core resources** carries the project's largest
rework risk: before it, permission answers one question ("is this yours?");
after it, two ("do you have access, and to what?"). Every endpoint written
before it is touched. The defense is designing the single-point filter in
slice 2 already anticipating the second question.

**README near the end**, because it documents what exists. The interactive
API documentation went to slice 1 instead: it builds itself from existing
endpoints, so installing it early means every slice is born already
documented.

**Telegram last**, for two independent reasons: it is the only item with an
open blocker (how the backend confirms which account a conversation belongs
to), and it is not the project's shop window.

## The rule that makes a slice vertical

Slices 1 through 5 each cross the whole stack, in this order:

> model → migration → serializer → endpoint → permission rule → tests →
> CI green → **production deploy responding**

No slice ends before its endpoint responds in production. Slice N+1 does not
start before slice N is live.

**Three declared exceptions:**
1. Slice 0 is not vertical — tooling, not a feature.
2. Slice 6 is not vertical — a document, not a feature.
3. The user model is created outside the slice that uses it, in slice 0 — the
   only model born before its feature, because of the destructive-migration
   constraint above.

**The named trap:** building the medication model in slice 2 makes it tempting
to also create the usage-period model, since it points back by foreign key.
The usage-period model is born in slice 3, with the foreign key added in a
later, trivial migration. The same holds for disease in slice 4 and sharing in
slice 5. Creating a future slice's model early is the trap to block.

## Full tooling from slice zero

Complete tooling before the first feature: `uv` for packages and environment,
`ruff` as linter and formatter, `mypy` for types, `pre-commit` as a pre-commit
gate, `pytest` with coverage reporting, Docker and Docker Compose with
PostgreSQL, CI that blocks merge, and an empty health-check endpoint live in
production in the first week — before any feature exists.

**Cost vs. building tools as needed:** roughly 10% more raw time upfront, for
one benefit: in any given week, something whole is live. An interruption in
week six leaves a small working system, not a skeleton of unfinished layers.
