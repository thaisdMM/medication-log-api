# DOCUMENTATION MIGRATION — HANDOFF

**Updated:** 01/09/2026, at the end of session 9. Session 3 also delivered
sessions 4 and 5, and part of session 8 — see plan §8, A13.

## What this file is

The current state of the migration, so a new session can open and continue
without re-reading the whole conversation.

**It holds no decisions.** Every decision lives in `docs/migration-sources/DOCS_MIGRATION_PLAN.md` —
sections 1 and 8 — and every **address** lives in `docs/migration-sources/DOCS_MIGRATION_MAP.md`. If
this file and either of those ever disagree, **they win**, and the discrepancy
is recorded rather than resolved by guessing.

This is not one of the `HANDOFF_...` files named in §3 rule 8 of the plan. Those
are Portuguese historical records that leave the repository. This one is English,
current, and stays until the migration finishes.

## First thing a new session does

1. Read `docs/migration-sources/DOCS_MIGRATION_PLAN.md` **completely**, sections 1 and 8 included.
   It governs the session. D1–D8 do not reopen; §8 amends some of them,
   A12 and A13 included.
2. Read this file.
3. Read `docs/migration-sources/DOCS_MIGRATION_MAP.md`. Every citation points at an address it
   assigns — §3 rule 6. The map is not reopened by a session on its own
   judgement; it is amended in plan §8, and each amended row says so. Two
   amendments are already in it: the `docs/roadmap.md` address for ETAPA2 C1,
   C2 and the roadmap file is superseded by A13 — the real address is
   `docs/task-slices/0001-roadmap.md` — and **eight rows are cut, split,
   narrowed or merged by A15 and A16**.
4. Read the mandatory reading for the session being executed — below.
5. Write the draft **in conversation**. Nothing becomes a file before the user
   approves it — §3 rule 10.

## MANDATORY READING FOR SESSION 10 — the second ADR batch

**Session 8 is still not next.** Five of its six records were delivered in
session 3; the sixth is the task 0.5 part 2 completion record, and that task is
still open — §3 rule 12. Session 8 closes when slice 0 does. The next session
is **10**.

**Type `/adr` before anything is written.** The ADR-writing rules live in
`.claude/skills/adr/SKILL.md`, which carries `disable-model-invocation: true`:
its description never enters context and the model cannot load it on its own.
Only the user can, and `CLAUDE.md` requires it loaded before any ADR is written
or amended — plan §8 A21.

Read each file **completely** before writing anything. Not an excerpt, not a
summary, not another document that cites it — §3 rule 1.

| # | File | Lines | Why |
|---|---|---|---|
| 1 | `docs/migration-sources/DOCS_MIGRATION_PLAN.md` | 832 | Governs the session. §2 carries the ADR-vs-spec criterion and the six points specific to migrating an archive; §3 the twelve rules; §8 the amendments, **A18 to A22 included** |
| 2 | `docs/migration-sources/DOCS_MIGRATION_HANDOFF.md` | this file | Current state |
| 3 | `docs/migration-sources/DOCS_MIGRATION_MAP.md` | 257 | **The addresses**, the ADR set of thirteen with its sources, and MAP 3 |
| 4 | `docs/migration-sources/ESTADO_CORRENTE_23_08_2026.md` | 1244 | **Source.** Rule 1 applies to it whole |
| 5 | `docs/migration-sources/ETAPA2_LEVANTAMENTO_DECISOES_FORA_DO_ESTADO_CORRENTE.md` | 686 | **Source** |
| 6 | `docs/adr/0001` to `docs/adr/0006` | 258 | Six records in the house style, written against this map. Read for form, not for content |
| 7 | `docs/non-goals.md` | 215 | The house style A14 produced. Read it for tone and length, not for content |

`CLAUDE.md` and `CLAUDE.local.md` load automatically. Do not re-read them.

**What the session needs from the user before writing:** which records the batch
takes. Seven ADRs remain — **0007 to 0013** — and the map fixes their numbers,
titles and sources; it does not fix the batching, and §3 rule 9 read per A13
means one *decision-bearing* document per approval round.

**Do not read:** `ROADMAP_MAPA_DAS_FATIAS.md`,
`FATIA0_NIVEL2_LISTA_DAS_TAREFAS.md` and the `FATIA0_TAREFA_0*_CONCLUIDA.md`
files — all migrated in session 3 — `O_QUE_O_PROJETO_NAO_FAZ.md`, migrated in
session 6, and `METODO_DE_TRABALHO_E_FORMATO_DAS_TAREFAS.md`, migrated in
session 7.

**Read only when the session writes `docs/domain-model.md`:**
`docs/migration-sources/FLUXO_CADASTRO_E_ISOLAMENTO_POR_CONTA.md`. MAP 3 is its allocation, and most
of it is cut — plan §8 A20.

This list is not the one deferred by §8 A7. That one is the persona's reading
list for **code tasks**, deferred because its addresses change during the
migration. This one is for **this session**, and every file in it exists today
under the name written here.

## Sessions

| # | Session | Status |
|---|---|---|
| 1 | Rules — `CLAUDE.md`, `CLAUDE.local.md`, skill, `.gitignore` | **DONE** 30/08/2026 |
| 2 | Allocation map — every section to its final address | **DONE** 30/08/2026 |
| 3 | Format pilot — `DECISAO_HOSPEDAGEM.md` becomes ADR 0001 | **DONE** 30/08/2026 |
| 4 | Roadmap — `ROADMAP_MAPA_DAS_FATIAS.md` | **DONE** 30/08/2026, folded into session 3 (§8 A13) |
| 5 | Slice 0 task list — `FATIA0_NIVEL2_LISTA_DAS_TAREFAS.md` | **DONE** 30/08/2026, folded into session 3 (§8 A13) |
| 6 | Non-goals — `O_QUE_O_PROJETO_NAO_FAZ.md` | **DONE** 30/08/2026 |
| 7 | Task format — part of `METODO_DE_TRABALHO_E_FORMATO_DAS_TAREFAS.md` | **DONE** 31/08/2026 |
| 8 | Slice 0 completion records — the `FATIA0_TAREFA_0*_CONCLUIDA.md` files | **partial, and blocked** — 5 of 6 done (01, 02, 03, 04, 05-part-1), folded into session 3. Task 0.5 part 2 is still in progress; its record becomes `docs/task-slices/0008` once that task closes — not ADR 0008 |
| 9 | First ADR batch — ADR 0002 to ADR 0006 | **DONE** 01/09/2026 |
| 10+ | The remaining ADRs — 0007 to 0013 — and the spec files, in batches, from the session 2 map | **NEXT** |

## What sessions 1 to 9 produced

| Path | Committed | Lines |
|---|---|---|
| `CLAUDE.md` | yes | 121 |
| `CLAUDE.local.md` | **no** — gitignored, line 19 of `.gitignore` | 26 |
| `.claude/skills/django-mentor/SKILL.md` | **not yet decided** — O6 | 139 |
| `.claude/skills/adr/SKILL.md` | **not yet decided** — O6. §8 A21, seventh rule per §8 A22 | 90 |
| `.claude/skills/django-mentor/task-format.md` | **no** — gitignored, line 20 of `.gitignore`. §8 A17 | 92 |
| `.gitignore` | yes | amended twice |
| `docs/migration-sources/DOCS_MIGRATION_MAP.md` | no — temporary, leaves with the migration | amended — a fifth standing cut, eight rows marked per §8 A15 and A16, **MAP 3 and findings F6 and F7 added** per §8 A18 to A20 |
| `docs/migration-sources/DOCS_MIGRATION_PLAN.md` | no | amended — §5 O2, O3, O4 and O5 struck, §8 A8 to A22 added |
| `docs/adr/0001-hosting-render-neon.md` | no | 52 |
| `docs/adr/0002-level-2-authentication.md` | no | 48 |
| `docs/adr/0003-custom-user-model.md` | no | 34 |
| `docs/adr/0004-ownership-through-medication.md` | no | 46 |
| `docs/adr/0005-owner-filter-single-point.md` | no | 39 |
| `docs/adr/0006-404-not-403.md` | no | 39 |
| `docs/non-goals.md` | no | 215 |
| `docs/open-questions.md` | no | 10 |
| `docs/task-slices/0001-roadmap.md` | no | 96 |
| `docs/task-slices/0002-slice-0-task-list.md` | no | 70 |
| `docs/task-slices/0003-repository-and-uv.md` | no | 14 |
| `docs/task-slices/0004-ruff-linter-and-formatter.md` | no | 19 |
| `docs/task-slices/0005-mypy.md` | no | 24 |
| `docs/task-slices/0006-pre-commit-and-commit-convention.md` | no | 37 |
| `docs/task-slices/0007-django-project-and-secret-key.md` | no | 54 |

Deleted on 30/08/2026: `REGRAS_COMPORTAMENTO_PROJETO.md`. A copy is held outside
the repository. Reasoning in §8 A2 of the plan.

**Nothing has been committed.** The user commits once the whole plan is
executed. Do not commit without being asked.

## Still open

| # | Question | Answered in |
|---|---|---|
| ~~**O3**~~ | **ANSWERED 30/08/2026.** Translate, not archive. See §8 A13 | session 3 |
| ~~**O4**~~ | **ANSWERED 31/08/2026.** Two sections survive, and outside the commit. See §8 A17 | session 7 |
| **O6** | Does `.claude/skills/` go into the commit? Raised in session 1, not decided. **Narrowed 31/08/2026:** `task-format.md` is out for certain — §8 A17 — so the question now covers `SKILL.md` only. **Weightier since 01/09/2026:** the `adr` skill lives there too, and it is the only permanent home of the ADR-writing rules — §8 A21 | any session |
| **O7** | Where the mandatory reading list is written. Deferred by §8 A7. Unblocked since session 2 | any session from 3 on |
| ~~**O8**~~ | **ANSWERED 01/09/2026.** The flow file splits: its facts go to `docs/domain-model.md`, the worked example is cut, and the file leaves with the other Portuguese sources. See §8 A20 and MAP 3 | session 9 |

O2 and O5 were answered on 30/08/2026, in session 2. Plan §8, A9 and A10.

## Findings still to fix

The map is the register of record — `docs/migration-sources/DOCS_MIGRATION_MAP.md`, "FINDINGS" — and
is not reopened. This table is a status view on top of it.

| # | Finding | Fix in |
|---|---|---|
| ~~**F1**~~ | **FIXED 30/08/2026, session 3.** The €5–10 valve is now written directly into ADR 0001's Context | session 3 |
| ~~**F2**~~ | **FIXED 30/08/2026, session 6.** `docs/non-goals.md` carries 22 items. The "19 itens" claim lived in the 24/08 table of `ESTADO_CORRENTE`, which the map cuts whole — nothing had to be rewritten | session 6 |
| **F3** | Two stale passages in `ETAPA2_...`: D5 still describes the form default `"não informada"`, revoked by §3.2; G1 still says the current state uses "titular" where it says "usuário" and "dono" today | session 10+ |
| **F4** | The permission-test table of `ETAPA2_...` B3 answers **403** where §17.5 decided **404**, and has no row for a guest asking outside the invitation scope | session 10+, with `docs/api-behaviour.md` |
| **F5** | §13.7 cites the table of §1.4, which the map cuts. The conclusion stands without it; the citation does not | session 10+ |
| **F6** | The stale 403 of F4 appears twice more, outside the B3 table: `ETAPA2_...` line 214 and `docs/migration-sources/FLUXO_CADASTRO_E_ISOLAMENTO_POR_CONTA.md` line 144. Recorded, not fixed — neither file is edited, both leave the repository. Plan §8 A18 | recorded in session 9 |
| **F7** | The owner column of the medication and of the disease has no address: `ESTADO_CORRENTE` presupposes it and never defines it, and only `docs/migration-sources/FLUXO_CADASTRO_E_ISOLAMENTO_POR_CONTA.md` line 122 names it. Plan §8 A19. **Unblocked the same day by A20** — the line now has an address, MAP 3 | the session that writes `docs/domain-model.md` |

## What session 6 delivered

`docs/non-goals.md`, 22 items, 215 lines from a 416-line source. Every one of
the ~25 pointers into `ESTADO_CORRENTE` was resolved against the map and
replaced by a final address — ADR numbers, `docs/domain-model.md` — with no
section number surviving. Fixes **F2**.

It also produced three decisions, all in plan §8: **A14**, the fifth standing
cut; **A15**, which cuts ETAPA2 A4; and **A16**, which applies A14 to the whole
map — eight rows cut, split, narrowed or merged, and `docs/open-questions.md`
projected at eight entries instead of thirteen.

## What session 7 delivered

`.claude/skills/django-mentor/task-format.md`, 92 lines from a 195-line source:
the three planning levels and the task template, and nothing else. Answers
**O4** — plan §8 **A17**, which also records the destination, the two rules the
format carries that the source did not, and one discrepancy left unfixed.

The file is **gitignored**. The repository is a portfolio, and beginner-tutorial
instructions state how the work is conducted, not what is true about the system.
Nothing already in `docs/` cites the method file or the word "tutorial" —
verified before writing. Two supporting edits: line 20 of `.gitignore`, and a
pointer section in `SKILL.md`, without which nothing reveals the file exists.

`METODO_DE_TRABALHO_E_FORMATO_DAS_TAREFAS.md` is now fully processed and leaves
the repository with the other Portuguese sources — §3 rule 8.

## What session 9 delivered

Five ADRs, 206 lines: `0002` level-2 authentication, `0003` custom user model,
`0004` ownership through the medication, `0005` owner filter in a single point,
`0006` 404 instead of 403.

It also produced five decisions, all in plan §8: **A18**, which records F6 and
the rule that a status code is written only in the record that decides it;
**A19**, which records F7; **A20**, which answers **O8**, splits
`docs/migration-sources/FLUXO_CADASTRO_E_ISOLAMENTO_POR_CONTA.md` and adds **MAP 3**; and **A21**,
which moves the ADR-writing rules into `.claude/skills/adr/SKILL.md`; and
**A22**, which settles where a record's content comes from when the archive does
not hold it.

**One record carries content that no archive file holds.** ADR 0003's two
Considered Options and its email-authentication driver were supplied by Thaís in
conversation on 01/09/2026: `ESTADO_CORRENTE` §12.1 states the decision and one
motive — the destructive migration — and names no alternative at all. A session
reading §12.1 alone will not find that driver there, and it was not inferred.
That is what **A22** records, and rule 7 of the `adr` skill is its general form.

## What session 10 does

The rest of the ADR set — **0007 to 0013** — and the spec files, from the map.
Seven records remain, and their sources are `ESTADO_CORRENTE` §3, §5, §6, §7,
§8 and §14, none of which has been migrated section by section yet.

What it needs from the user: **which records the batch takes**, and `/adr` typed
before the first one is written.

Three traps. The ADR set is small on purpose — D4, thirteen by A11 — so a
decision that fails the §2 criterion goes to spec, not to a fourteenth record.
Three findings are still due — **F3**, **F4** and **F5** in the table above —
each recorded, never silently repaired — §3 rule 2. And four of the seven
records — 0007 to 0010 — take their Considered Options from the `VERSÃO
SUPERADA` texts of §3, §5 and §6, where **A8** applies: only the option tables
survive, and the account of who abandoned what does not.

**Do not write a second decision-bearing document.** §3 rule 9, read per A13.

## Maintaining this file

At the end of every session: mark the session DONE in the table above, rewrite
the mandatory-reading block for the session that comes next, and move anything
newly decided into §8 of the plan — not into this file. This file holds state;
the plan holds decisions.

This file is temporary. It leaves the repository when the migration finishes.

## Standing constraints

- No code, no migrations, no application changes. This is documentation work —
  §3 rule 11.
- Slice 0 runs in parallel and is not blocked by this plan. Task 0.5 part 2 is
  still open — §3 rule 12.
- One *decision-bearing* document per approval round — §3 rule 9, read per
  §8 A13. Do not start the next one because there is room left.
- Historical files are not migrated and leave the repository — §3 rule 8.
- Everything written into the project is English. The conversation is Portuguese
  — D2, and §8 A4.
