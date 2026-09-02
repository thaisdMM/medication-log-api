# DOCUMENTATION MIGRATION PLAN — Portuguese planning files to English project documentation

**Written:** 30/08/2026
**Approved by Thaís:** 30/08/2026
**Status:** active. This plan governs every session that restructures documentation.

---

## WHAT THIS DOCUMENT IS

The plan for turning the Portuguese planning files at the repository root into
English project documentation, one session at a time.

It exists so that a session opened next week reaches the **same** structure a
session opened today would reach. Every decision below was closed in the
conversation of 30/08/2026 and is **not reopened** by a later session. Where
something is still open, it says so and says who decides.

## WHAT THIS DOCUMENT IS NOT

It does not translate anything, it does not decide the content of any project
decision, and it does not change the product. Restructuring documentation
**never** changes what a decision says. A session that believes a decision is
wrong records the discrepancy and stops — it does not fix it while translating.

---

## 1. DECISIONS ALREADY CLOSED

| # | Decision | Who | When |
|---|---|---|---|
| **D1** | The repository becomes the authoritative source of project documentation, in English. The claude.ai project stops being where the truth lives | Thaís | 30/08/2026 |
| **D2** | **Everything written into the project is English.** Conversation between Thaís and the AI stays Portuguese | Thaís | 30/08/2026 |
| **D3** | ADR format is used **only** for decisions that had a real fork in the road. Everything else goes to spec, glossary, non-goals, or open questions | Claude, approved by Thaís | 30/08/2026 |
| **D4** | The ADR set stays small — roughly ten to twelve. The small size is part of the signal | Claude, approved by Thaís | 30/08/2026 |
| **D5** | **Allocation comes before writing.** Session 2 assigns every section a final address; later sessions cite those addresses even before the files exist | Claude, approved by Thaís | 30/08/2026 |
| **D6** | The session order in section 4 below | Thaís proposed, Claude reordered, Thaís approved | 30/08/2026 |
| **D7** | Teaching and conversation-conduct content leaves the commit. It moves to a gitignored `CLAUDE.local.md`; engineering rules stay in a committed `CLAUDE.md`. **Amended 30/08/2026 — see §8, amendment A3** | Thaís | 30/08/2026 |
| **D8** | **The migrated documentation is terse and technical. No verbatim quotations, no conversation transcripts, no decision narrative.** Rationale is restated as a technical argument. ADRs follow the MADR template | Thaís | 30/08/2026 |

### D2 revokes a written rule — do not follow the old one

`METODO_DE_TRABALHO_E_FORMATO_DAS_TAREFAS.md` §1 states that internal planning
files are written in Portuguese, with Thaís' words: *"se não tem diferença, eu
prefiro que seja em português porque aí eu consigo acompanhar linha a linha."*

**That line is revoked as of 30/08/2026.** Her words closing it: *"a partir de
agora, tudo escrito no projeto é ingles, só nas nossas conversas que vamos falar
portugues."*

A session that reads the old method file will find the revoked rule still
written there, because that file has not been migrated yet. **This plan wins
until session 7 rewrites it.**

### The reason for D1 and D2, recorded because Claude got it wrong once

The reason is **consistency with the codebase and with the European job market
Thaís is targeting**.

It is **not** "so the AI makes fewer errors." Claude proposed that reasoning on
30/08/2026 and Thaís corrected it. Do not repeat it as justification anywhere in
the migrated documentation.

---

## 2. THE CRITERION THAT SEPARATES ADR FROM EVERYTHING ELSE

Apply this criterion. Do not re-derive it, and do not negotiate it per item.

> **An ADR answers "why did we choose this and not that". A spec answers "what
> is true about the system".**

Two tests that settle it:

1. **Could a competent engineer, holding the same information, reasonably have
   chosen differently?** Yes → ADR. No → spec.
2. **When it changes, what happens to the old text?** A new record supersedes it
   and the old one survives marked `Superseded` → ADR. You edit it in place
   because the old text is worthless → spec.

### The evidence that this project needs ADR for the first group

`docs/migration-sources/ESTADO_CORRENTE_23_08_2026.md` currently carries **three** hand-written banners
reading "VERSÃO SUPERADA, NÃO LEIA COMO DECISÃO" — at §3, §5 and §6 — because
two different texts share each number. A banner had to be written by hand for
"§3" to identify a single text again.

ADR solves that by construction: `Status: Superseded by 0011` lives in the file.
Nobody has to remember to write a warning.

### Allocation — proposed, confirmed item by item in session 2

**ADR candidates** — each had a documented alternative:

| Source | Decision |
|---|---|
| §3.1–3.6 | `nulls_distinct=False` for the duplicate constraint. §3.5 records the two fallback positions |
| §12.1 | Custom user model before the first migration |
| §17.1 | Ownership discovered through the medication; no owner column. Thaís proposed the column and discarded it |
| §17.2 | Owner filter in a single point of the code |
| §17.5 | 404 instead of 403. **Supersedes** the earlier 403 decision |
| §7.4 | Telegram by webhook, not long polling |
| §8 + §6.7 | Email to console everywhere, including production |
| §5.2 | Disease list in the database, not in code |
| §6.2 | One sharing row per pair of accounts |
| §6.10 | An account cannot invite itself |
| §14.1 | Interactive API documentation published |
| `DECISAO_HOSPEDAGEM.md` | Render plus Neon. Already ADR-shaped |

**Spec / domain model:** §1.1, §2, §5.1, §6.1, §6.3, §6.4, §3.9, §13.1–13.7,
§17.4-A.

**Glossary:** §4.1 — user, data owner, guest.

**Non-goals:** the 22 items of `O_QUE_O_PROJETO_NAO_FAZ.md`.

**Open questions — never an ADR, because they are not decided:** §3.10 the
experiment, §7.6 the conversation-to-account binding, blocks H1–H6 and item B2
of `docs/migration-sources/ETAPA2_LEVANTAMENTO_DECISOES_FORA_DO_ESTADO_CORRENTE.md`.

**Neither ADR nor spec:** §9 evaluation criteria and §15 deadline and estimate.
They belong in the README or stay internal.

### The ADR template — MADR

Verified at `adr.github.io/madr` on 30/08/2026.

Front matter: `status`, `date`, `decision-makers`, `consulted`, `informed`.
Required sections: **Context and Problem Statement**, **Considered Options**,
**Decision Outcome**. Optional: Decision Drivers, Consequences, Confirmation,
Pros and Cons of the Options, More Information.

**MADR has no provision for verbatim quotations or conversation transcripts.**
Attribution is the `decision-makers` field — a name, not a quotation. This is
what D8 above rests on: terseness is the format, not a concession to it.

**One line of `More Information` per ADR** names the address in Thaís' archive —
for example `ESTADO_CORRENTE §17.1` — as plain text, not a link, since the
archive lives outside the repository. It costs one line and keeps the origin
recoverable.

**Target length: one screen.** An ADR that does not fit is carrying narrative
that D8 removes, or is two decisions wearing one title.

### The rules for writing one live outside this plan — added 01/09/2026

See §8, amendment **A21**. The criterion above, the template above and six
rules born from errors made while writing this batch are in the `adr` skill, at
`.claude/skills/adr/SKILL.md`, which survives the migration. This plan does not
restate them; it adds only what is specific to migrating an archive:

1. **The source is read whole before anything is written** — §3 rule 1.
2. **Every citation points at a map address**, even when the file does not exist
   yet — §3 rule 6.
3. **The five standing cuts of `docs/migration-sources/DOCS_MIGRATION_MAP.md` apply while writing**,
   the fifth included: a question asked and answered, and any comparison with
   another project, never travel — §8 A14.
4. **A defect in the source is recorded, never repaired in passing** — §3
   rule 2. It becomes a finding in the map, and the map is the register.
5. **What the source marks open stays open** — §3 rule 4.
6. **Content supplied by Thaís in conversation travels; content deduced from
   what the source writes does not** — §8 **A22**, added 02/09/2026. The session
   says which is which when it presents the draft.

---

## 3. RULES THAT APPLY TO EVERY SESSION

1. **Read the source file completely before writing anything.** Not the excerpt,
   not a summary, not another document that cites it.
2. **Translation is not rewriting.** If a decision looks wrong, incomplete or
   contradictory, record it in the session's discrepancy list and keep the
   meaning as written. Fixing it is a separate conversation with Thaís.
3. **Never invent content to fill a gap.** A gap in the source is a gap in the
   output, declared as such.
4. **Never promote status.** What the source marks OPEN stays open. What the
   source marks "proposta de Claude não confirmada" stays unconfirmed. A
   proposal never becomes a premise.
5. **Superseded content is preserved, never deleted.** It moves into an ADR
   marked `Superseded`, keeping the date and the reason.
6. **Citations point at the final addresses** from the session 2 map, even when
   the target file does not exist yet.
7. **No verbatim quotations and no decision narrative — D8.** The migrated
   documentation states the technical argument, not who said what in which
   conversation. `decision-makers` and `date` in the front matter carry the
   attribution; the body carries the reasoning. Where a section of the source
   spends a paragraph on how a decision was reached, the output keeps the
   conclusion and drops the account.
8. **Historical files are not migrated, and they leave the repository.**
   `docs/migration-sources/ESTADO_CORRENTE_23_08_2026.md`, `ETAPA2_...`, `FASE1_...`, `FASE2_3_...`,
   `HANDOFF_...`, `MODELAGEM_...`, `CORRECAO_...` stay in Portuguese and move to
   Thaís' archive outside the project. They exist to trace the origin of a
   decision, never as a statement of what is true today. Nothing in the migrated
   documentation may depend on a reader having access to them.
9. **One session, one document.** Do not start the next one because there is
   room left.
10. **Nothing is written to the repository before Thaís approves it in
    conversation** — `METODO...` §5. The AI writes it in the conversation, she
    approves, then it becomes a file.
11. **No code, no migrations, no application changes.** This whole plan is
    documentation work. The barrier of `FATIA0_NIVEL2_LISTA_DAS_TAREFAS.md`
    stands: nothing creates a table before task 0.7.
12. **Slice 0 continues in parallel and is not blocked by this plan.** Task 0.5
    part 2 is still open.

---

## 4. THE SESSIONS

| # | Session | Output | Decision it needs from Thaís |
|---|---|---|---|
| ~~**1**~~ **DONE 30/08/2026** | Rules | `CLAUDE.md` (committed), `CLAUDE.local.md` (gitignored), `.claude/skills/django-mentor/SKILL.md`, `.gitignore` line. **All three in English.** See §8 | **O1** — answered, §8 A1 |
| **2** | **Allocation map** | One table: every section of the current state and of the Etapa 2 survey mapped to its final address. No prose. Fixes F1 and F2 below | confirm the allocation and the target paths (**O2**) |
| **3** | Format pilot | `DECISAO_HOSPEDAGEM.md` becomes the first ADR | approve the ADR template |
| **4** | Roadmap | `ROADMAP_MAPA_DAS_FATIAS.md` translated | — |
| **5** | Slice 0 task list | `FATIA0_NIVEL2_LISTA_DAS_TAREFAS.md` translated | — |
| **6** | Non-goals | `O_QUE_O_PROJETO_NAO_FAZ.md` translated. The most citation-dense file — roughly 25 pointers into the current state | — |
| **7** | Task format | The task-format part of `METODO_DE_TRABALHO_E_FORMATO_DAS_TAREFAS.md`. The working-method part goes to `CLAUDE.local.md` | **O4** below |
| **8** | Slice 0 completion records | The `FATIA0_TAREFA_0*_CONCLUIDA.md` files | **O3** below |
| **9+** | ADRs and spec | The bulk, in batches, from the session 2 map | — |

### Why session 2 exists, and why it comes second

Every document in sessions 4 to 8 cites the current state by section number —
`§12.1`, `§3.3`, `§17.2`, `§6.7`, `§13.1`. If those files were translated before
the current state was split, each would point at section numbers that are about
to stop existing, and all of them would need a second pass.

The map is cheap because it assigns addresses without writing prose. **Addresses
are what a citation needs; the file itself can arrive later.**

### Why the hosting decision is the pilot

`DECISAO_HOSPEDAGEM.md` already has every part of an ADR: context (the free
tier), decision (Render plus Neon), alternative examined and rejected (the
database on Render), assumed consequence (hibernation), and a trigger to reopen.
Converting it is reformatting, not rewriting — which makes it the cheapest place
to see the template on real content before committing to it for twelve more.

### ~~What session 1 merges, and what it must not drop~~ — SUPERSEDED 30/08/2026

> **This section is superseded by §8, amendment A2. It is kept because the plan
> preserves superseded content rather than deleting it (§3 rule 5). Do not
> execute the instruction below.**

~~`CLAUDE.md` carried over from the other project covers **code discipline**.
`REGRAS_COMPORTAMENTO_PROJETO.md` covers **evidence and status discipline**, and
four of its rules — A2, A4, D1 and D2 — have no equivalent in the carried-over
file. These four were born from errors made in **this** project. They survive
the merge.~~

What actually held: rule 12 of the carried-over file — Docker, monorepo,
`django_version/` — was dropped whole, as planned. `REGRAS_COMPORTAMENTO_PROJETO.md`
was dropped **entirely**, and the file was deleted from the repository on
30/08/2026. See §8 A2 for the reasoning.

The official documentation recommends staying under 200 lines. The delivered
`CLAUDE.md` is 121. **The merge was curation, not concatenation.**

---

## 5. OPEN DECISIONS

| # | Question | Where it is answered |
|---|---|---|
| ~~**O1**~~ | **ANSWERED 30/08/2026.** R3 is split: the execution clause is rule 13 of the committed `CLAUDE.md`; the "does not hand over finished code" clause is in the `django-mentor` skill. See §8 A1 | session 1 |
| ~~**O2**~~ | **ANSWERED 30/08/2026.** The target paths, with the spec split into three files. See §8 A9 | session 2 |
| **O3** | The slice 0 completion records: translate them, or archive them? They are execution logs, not system documentation | session 8 |
| ~~**O4**~~ | **ANSWERED 31/08/2026.** The three planning levels and the task template survive; everything else is cut or was already delivered. They do **not** become project documentation — the file is gitignored. See §8 A17 | session 7 |
| ~~**O5**~~ | **ANSWERED 30/08/2026.** A file, `docs/open-questions.md`. See §8 A10 | session 2 |

---

## 6. FINDINGS TO FIX DURING THE MIGRATION

Both found on 30/08/2026 by comparing citations against the sections that
actually exist.

| # | Finding |
|---|---|
| **F1** | `DECISAO_HOSPEDAGEM.md` line 78 cites `§16.2` of the current state for the authorized budget of five to ten euros per month. **§16.2 does not exist** — §16 is "Interface — API only" and stops at §16.1. The fact lives in item A2 of the Etapa 2 survey, sourced from Fase 1, decision D1 |
| **F2** | `docs/migration-sources/ESTADO_CORRENTE_23_08_2026.md` line 436 says the non-goals list has *"19 itens"*. **It has 22.** |

Neither blocks anything. Both are fixed in the session that touches the file.

---

## 7. WHAT THIS PLAN DOES NOT AUTHORIZE

- Changing any decision while translating it.
- Merging two decisions because they look similar.
- Writing an ADR for something the source marks as open.
- Deleting a superseded section instead of recording it as superseded.
- Migrating the historical files.
- Starting the next session's document because there was room left.
- Getting ahead of slice 0. If a session suggests *"while we are here, let's also
  create…"*, that is the trap named in `ROADMAP_MAPA_DAS_FATIAS.md`, and Thaís
  interrupts.

---

## 8. AMENDMENTS

Decisions taken **after** the plan was approved, which change what an earlier
section says. Every one was decided by Thaís in conversation. The superseded
text is kept in place and marked, never deleted — §3 rule 5.

### A1 — O1 is answered: restriction R3 is split, not placed

**Decided 30/08/2026, session 1.** Supersedes: §5, O1.

R3 of Phase 1 is two clauses with different owners, and the D7 line falls
between them:

| Clause | Where it now lives |
|---|---|
| "the code is written and the project commands are run by the developer" | rule 13 of the committed `CLAUDE.md` |
| "the AI explains reasoning; it does not hand over finished code" | the `django-mentor` skill |

The argument that R3 "is what makes the portfolio defensible" appears in
`ETAPA2_...` line 88, sourced from `FASE1_...` line 120. **That source file is
not in this repository and could not be opened.** The claim is recorded as
unverified and must not be reused as a premise.

### A2 — `REGRAS_COMPORTAMENTO_PROJETO.md` is dropped entirely

**Decided 30/08/2026, session 1.** Supersedes: §4, "What session 1 merges".

Nothing from that file entered `CLAUDE.md` — not A2, A4, D1 or D2. The file was
deleted from the repository on 30/08/2026; a copy is held outside the project.

The reasoning: the errors those rules guarded against came from documentation
that was not reorganized when a later decision broke an earlier one. That defect
is what ADR `Status: Superseded` fixes by construction — §2 of this plan. Rules
1 and 2 of the carried-over `CLAUDE.md` already cover most of what remained.

### A3 — Conduct content splits three ways, not two

**Decided 30/08/2026, session 1.** Amends: §1, D7.

D7 assumed two destinations. Delivery required three, because a skill only loads
when it is invoked, and some conduct must hold **before** the first message of a
session:

| Destination | Holds | Committed |
|---|---|---|
| `CLAUDE.md` | engineering rules | yes |
| `CLAUDE.local.md` | only what must be in context from message one: conversation language, transcribed-audio handling, a pointer to the skill | no — gitignored |
| `.claude/skills/django-mentor/SKILL.md` | the mentoring method: teaching, evidence labels, research boundary, conversation conduct | not yet decided |

The skill carries `disable-model-invocation: true`. `[doc]` Verified at
`code.claude.com/docs/en/skills` on 30/08/2026: with that field the skill's
description never enters context and the model cannot load it — only the user
can, by typing `/django-mentor`. This is why `CLAUDE.local.md` must name the
skill: nothing else in context reveals that it exists.

`[doc]` Also verified at `code.claude.com/docs/en/memory` on 30/08/2026:
`CLAUDE.local.md` is current, loads alongside `CLAUDE.md`, and is documented as
the place for per-project preferences that stay out of version control.

### A4 — Everything written into the project is English, without exception

**Decided 30/08/2026, session 1.** Corrects: §4, the session 1 row, which said
`CLAUDE.local.md` would be in Portuguese. That contradicted D2. **D2 wins, at
face value.** All three delivered files are in English.

### A5 — A new rule that D8 does not cover: verify the version in use

**Decided 30/08/2026, session 1.** Adds to: the rule set, not to any decision.

`CLAUDE.md` rule 10 requires reading `pyproject.toml` (declared floor) and the
`name`/`version` lines of `uv.lock` (resolved version) before proposing any API,
pattern or command, and reading the official documentation when the resolved
version falls outside training. Rule 9 was narrowed to its prohibition, because
its old remedy — "ask the user to verify" — contradicted rule 10.

`[executed]` 30/08/2026: `pyproject.toml` declares floors, not pins; `uv.lock`
is 540 lines, which is why rule 10 forbids reading it whole.

### A6 — DRF is confirmed for this project

**Decided 30/08/2026, session 1.** Adds to: §2, the allocation.

`ETAPA2_...` §C2 lists the decided tooling and does **not** name Django REST
Framework; it appears only indirectly through §14.1 of the current state.
Confirmed directly by Thaís on 30/08/2026: the project will use DRF. Session 9+
records it where the allocation map places it.

### A7 — The mandatory reading list is deferred

**Decided 30/08/2026, session 1.** Affects: §4, sessions 2 and 7.

The reading list of `PERSONA_DEV_SENIOR_ACOMPANHANTE.md` §1 was **not** carried
into any of the three delivered files. Five of its six entries stop existing
under their current names during sessions 2 to 9, and §3 rule 6 requires
citations to point at final addresses that the session 2 map has not yet
assigned. It is written into `.claude/` once the documents are organized.

### A8 — Superseded content is preserved only if something was built on it

**Decided 30/08/2026, session 2.** Restricts: §3, rule 5.

Rule 5 says superseded content is preserved and moves into an ADR marked
`Superseded`. That rule now applies **only** to a decision that was superseded
**after** something had been implemented against it.

The argument: an ADR marked `Superseded` earns its place by explaining why code
changed. Nothing in this project has been built. A position abandoned before any
implementation existed is not the history of a system — it is a draft of a
conversation, and it becomes documentation nobody can act on.

What this does **not** cut: the rejected alternative itself. It travels into the
ADR as a **Considered Option**, with the technical reason it lost. An ADR
without alternatives fails the first test of §2. What is cut is the account —
who proposed it, who withdrew it, and on which day two texts came to share a
section number.

Consequence already applied by the session 2 map: the three `VERSÃO SUPERADA`
texts of `ESTADO_CORRENTE` (§3, §5, §6) do not become superseded records; only
their option tables survive. The earlier 403 decision does not become a
`Superseded` ADR either — it is a Considered Option of ADR 0006.

### A9 — O2 is answered: the target paths, with the spec split in three

**Decided 30/08/2026, session 2.** Supersedes: §5, O2.

```
docs/adr/NNNN-<slug>.md      docs/non-goals.md
docs/domain-model.md         docs/glossary.md
docs/api-behaviour.md        docs/open-questions.md
docs/definition-of-done.md   docs/roadmap.md
README.md
```

Three of these are not in the proposal O2 carried. `docs/api-behaviour.md`
exists because §17.2, §17.3, §17.5 and the permission-test table of ETAPA2 B3
are response and permission behaviour, and sit badly in a file called
`domain-model.md`. `docs/definition-of-done.md` exists because §3.6, §17.4 and
ETAPA2 B4 state what must be verified, not what is true. `docs/roadmap.md` is
the session 4 address, and receives ETAPA2 C1 and C2.

The nine base constraints of ETAPA2 block A go to `README.md`. A
`docs/constraints.md` was considered and rejected: the README is where a
portfolio project states what it may and may not use.

### A10 — O5 is answered: open questions are a file

**Decided 30/08/2026, session 2.** Supersedes: §5, O5.

`docs/open-questions.md`. Not GitHub issues.

The argument: §3 rule 6 requires citations to point at final addresses, and an
issue number does not exist until the issue is created. A file has an address
today, is versioned beside the documentation that cites it, and turning its rows
into issues later stays cheap.

### A11 — The ADR set is thirteen

**Decided 30/08/2026, session 2.** Adds to: §2, the allocation. Affects: D4.

ETAPA2 B1 — level-2 authentication, multiple users with isolated data — becomes
**ADR 0002**. The proposal in §2 did not list it. It had a documented
alternative (level 1, single user), it was chosen against the recommendation
recorded at the time, and `FASE2_3...` 28 states it is the reason the system
exists. It is the strongest ADR candidate in the survey.

D4 says "roughly ten to twelve". Thirteen holds.

ETAPA2 D7 — medication is name and concentration in one table — was examined as
a fourteenth and stays **spec**. It has a documented alternative, but the
alternative it rejected is a pharmaceutical catalogue, which is already a
non-goal.

### A12 — Session 3 delivers two files: ADR 0001 and the first entry of open-questions.md

**Decided 30/08/2026, session 3.** Amends: §4, session 3 row.

Session 3 was scoped to one output, `DECISAO_HOSPEDAGEM.md` becoming ADR
0001. Thaís decided the task 0.11 pending verifications do not mix into the
ADR body — they open `docs/open-questions.md` instead, as its first entry.
Rule 9 still forbids starting session 4's document; it does not forbid a
second, smaller file within the same session when two document types must
not mix.

Fixes F1 (§6): the €5–10 valve (ETAPA2 A2) is now written directly into ADR
0001's Context, replacing the broken `§16.2` citation.

### A13 — O3 is answered: translate, not archive; sessions 3, 4 and 5 run together; a new address supersedes docs/roadmap.md

**Decided 30/08/2026, session 3.** Supersedes: §5, O3. Amends: §4, the
session 3, 4 and 5 rows; the map's `docs/roadmap.md` address for ETAPA2 C1,
C2 and the roadmap file itself.

**O3 answered:** the slice 0 completion records (`FATIA0_TAREFA_0*_CONCLUIDA.md`)
are translated, not archived. They hold at least one decision with no other
address — the commit message convention (Conventional Commits 1.0.0, scope
optional), settled in task 0.4 — and Thaís uses them operationally, to
reconstruct what exists before planning the next task's tutorial.

**Sessions 3, 4 and 5 ran as one conversation**, at Thaís' request, since
roadmap and task-list content is translation and adaptation, not judgment
calls between competing decisions the way ADRs are. Rule 9 (one session, one
document) is read here as one *decision-bearing* document at a time — ADR
0001 stayed alone in its own approval round; roadmap, task list and the
completion records did not carry that same risk.

**New address, replacing `docs/roadmap.md`:** `docs/task-slices/`, numbered
like the ADR set —

```
docs/task-slices/0001-roadmap.md                          ROADMAP_MAPA_DAS_FATIAS.md + ETAPA2 C1, C2
docs/task-slices/0002-slice-0-task-list.md                 FATIA0_NIVEL2_LISTA_DAS_TAREFAS.md
docs/task-slices/0003-repository-and-uv.md                 task 0.1 completion record
docs/task-slices/0004-ruff-linter-and-formatter.md          task 0.2 completion record
docs/task-slices/0005-mypy.md                               task 0.3 completion record
docs/task-slices/0006-pre-commit-and-commit-convention.md   task 0.4 completion record
docs/task-slices/0007-django-project-and-secret-key.md      task 0.5 part 1 completion record
```

Task 0.5 part 2 is still open (§3 rule 12); its completion record becomes
`0008` once that task closes, in a later session.

### A14 — Answered doubts and cross-project comparisons are not documentation

**Decided 30/08/2026, session 6.** Adds to: §3, the rules. Extends the
"CUTS THAT APPLY TO EVERY SECTION" list of `docs/migration-sources/DOCS_MIGRATION_MAP.md` with a
fifth entry, without reopening the map's addresses.

A fifth standing cut, applied while writing every destination file:

> **5. A question that was asked and answered, and any comparison with another
> project.** The source files record doubts raised and settled in conversation,
> and passages that reason about this project by contrast with SkillBridge or
> with work done elsewhere. Neither states what is true about this system.
> Where the answer changed a decision, the decision travels; the question never
> does.

**The argument, and it is about length, not about tidiness.** A document is
read in full or it is not read. Every line that documents a doubt rather than
the system pushes the line that matters further down the page, and the reader
who gives up before reaching it has been failed by the file's length, not by
its accuracy. Terseness is the format — D8 — and this cut is what enforces it
on content the other four cuts do not reach.

The map already cut most of it row by row: `ESTADO_CORRENTE` §1.2, §3.7, §3.8,
§10, §13.6, §14.4, the SkillBridge paragraph of §12.3, and ETAPA2 A8. What the
rule adds is the general form, so that sessions 9+ do not re-derive the
judgement per item. Passages it reaches that no row cuts today:

| Source | What goes |
|---|---|
| §7.3 | *"A pergunta 'é possível?' está respondida: é."* — the answered question. The verified facts about bots stay |
| §7.4 | The Stripe comparison. The webhook decision stays |
| §12.2 | *"Argon2, já usado no SkillBridge"*. That the password is stored hashed stays |
| ETAPA2 C1 | *"é a correção direta do que aconteceu no SkillBridge"*. Already dropped in session 3 |
| ETAPA2 D3 | The note that the criterion was once misapplied. The criterion stays |

### A15 — ETAPA2 A4 is cut; it is not a non-goal and not a README constraint

**Decided 30/08/2026, session 6.** Amends: the MAP 2 row for A4, which sent it
to `README.md` and `docs/non-goals.md`.

Firebase, Supabase and the backend-as-a-service category are not an excluded
scope of this project. Nothing was weighed and rejected: the question was
settled by what the project already is — a Python web backend, written by a
backend developer — and never reached the status of a decision with a real
alternative. Recording it as a non-goal would tell a reader that the category
was once a candidate here, which is the opposite of true.

This is A14 applied to a row the map wrote before A14 existed. It is the first
of its kind found; sessions 9+ apply the same test to every remaining ETAPA2
block-A row before it reaches `README.md`.

`docs/non-goals.md` therefore carries **22 items, not 23**.

### A16 — A14 applied to the whole map: eight rows amended

**Decided 30/08/2026, session 6.** Amends: `docs/migration-sources/DOCS_MIGRATION_MAP.md`, MAP 1 and
MAP 2. The map's addresses are still not reopened by a session on its own
judgement; they are amended **here**, and the map records the amendment beside
each row.

A15 cut one row. Reading every remaining row through A14 found seven more, in
three kinds.

**Questions the work has already answered.** Not doubts — rows that aged. Each
was routed to `docs/open-questions.md` and has no question left inside:

| Row | Answered by |
|---|---|
| ETAPA2 C3 — first slice after authentication | `docs/task-slices/0001-roadmap.md`: slice 2 is medication |
| ETAPA2 A9 — hosting platform never chosen | ADR 0001. All three "a reverificar" data points are settled in its Context |
| §8 — email cost and free-tier research, deferred | ADR 0012: console in every environment. No provider is ever configured |
| ETAPA2 H5 — does "outro" in the unit carry free text | §3.9, project-wide: no escape option anywhere carries free text |
| ETAPA2 H6 — confirm "outras" in disease carries no free text | The same answer; `docs/non-goals.md` item 14 states it |

**A14 proper.**

- **§14.5**, which OpenAPI library — cut. A library choice made at install time,
  which the source itself declines to decide. An open-questions file listing
  library choices lists non-questions.
- **§5.4** — split. *Which* models are registered in the admin panel is cut, a
  trivial implementation choice. The alert attached to it is real engineering
  and survives, moved to `docs/definition-of-done.md`: registering medication,
  usage, disease or sharing in the panel gives every `is_staff` account the
  health data of all accounts.
- **B preamble** → ADR 0002 — narrowed, not cut. The technical cost of level 2
  travels: token authentication on the API, owner filtering in every query,
  tests doubled. The argument that it is worth it because "REST stateless" is a
  concept not yet known, and the reference to an interview-preparation file, do
  not.

**Working method mistaken for system truth.**

- **ETAPA2 A6**, real-utility domain with scope frozen on day 1 — cut, on the
  same ground §9 was. The scope that was frozen is stated by
  `docs/non-goals.md`, which is the artefact. The act of freezing it is not
  documentation.

**One merge, no cut:** ETAPA2 H2 — which forms, and whether "não informada" is
one — folds into the §3.10 entry. It is not a separate question; it is what the
experiment decides.

**Kept, examined and not cut:** the transferable rule of §4 — *what an account
has becomes a relation; what an account is becomes a type* — is a maxim, but it
is the reason a single account type exists. One line in `docs/domain-model.md`.

**Effect:** `docs/open-questions.md` is projected at **eight entries, not
thirteen** — Telegram timeout vs hibernation, the §3.10 experiment with H2
inside, the conversation-to-account binding, `simplejwt` vs Django 6.1, whether
a rule replaces the dropped active-use rule, and H1, H3, H4.

### A17 — O4 is answered: the task format survives, and it leaves the commit

**Decided 31/08/2026, session 7.** Supersedes: §5, O4. Amends: §4, the session 7
row, which sent the task format to project documentation.

Two of the six sections of `METODO_DE_TRABALHO_E_FORMATO_DAS_TAREFAS.md` survive
— the three planning levels and the task template. The other four are cut, and
none of them loses content:

| Source section | Why it does not travel |
|---|---|
| Header, "what this document is / is not" | Provenance, plus the SkillBridge comparison — A14 |
| §1 Language | Its rule that internal planning files are Portuguese is **revoked by D2**. What remains is rule 6 of `CLAUDE.md`, `CLAUDE.local.md`, and the closing line of the `django-mentor` skill |
| §2 The audio rule | Delivered in session 1, `CLAUDE.local.md` |
| §5 Planning becomes a file | Working method, not system truth. Its second half — the AI drafts in conversation, Thaís approves, only then it becomes a file — is §3 rule 10 of this plan, which leaves the repository with the migration. Recorded here so that it is a decision and not an omission |
| §6 Open items | All six already have an address: the persona is the skill; hosting is ADR 0001; the §3.10 experiment, `simplejwt`, concentration units and frequency values, and the chat-to-account binding are `docs/open-questions.md`; the 403/404 contradiction is F4 |

**Destination:** `.claude/skills/django-mentor/task-format.md`, gitignored, with
one line added to `.gitignore` and a pointer in `SKILL.md` — the same argument as
A3: nothing else reveals the file exists.

**Why it leaves the commit.** Thaís' decision, 31/08/2026: the repository is a
portfolio, and beginner-tutorial instructions describe how the work is conducted,
not what is true about the system. Nothing already written in `docs/` cites the
method file or depends on it — verified before the file was written.

**Two rules the format carries that the source did not.**

1. **A decision is cited by its migrated address**, and one with no address is
   written as *not documented* — never guessed, and never pointing at a
   Portuguese planning file, since those leave the repository. This is §3 rules
   3 and 6 applied to the task template.
2. **No SkillBridge comparison.** A14 applied whole: the source's two tables —
   what was added to the SkillBridge example and what was removed from it —
   disappear as comparison. What was a rule survives as a rule.

**One discrepancy recorded, not fixed** — §3 rule 2. §4 of the source justifies
the field *"por que esta tarefa existe"* by saying every decision is traceable to
a statement of Thaís'. **D8 revoked that**: attribution is the `decision-makers`
field of an ADR, never a quotation in the body. The field survives with the
technical reason — the person writing the code must know which decision they are
implementing — and the address replaces the statement.

### A18 — F6: the stale 403 sits in three places, not one

**Decided 01/09/2026, session 9.** Adds to: §6, the findings, and to
`docs/migration-sources/DOCS_MIGRATION_MAP.md`, "FINDINGS", which gains row **F6**.

F4 records the defect in the ETAPA2 B3 permission-test table. Reading block B
whole for ADR 0002 found the same stale code twice more:

| Where | What it says | What §17.5 decided |
|---|---|---|
| `ETAPA2` line 214, block B preamble | the doubled test is *"outro usuário, que tem que receber 403"* | **404** — an account with no relation is not in the requester's set |
| `docs/migration-sources/FLUXO_CADASTRO_E_ISOLAMENTO_POR_CONTA.md` line 144 | the isolation proof is *"o teste do 403"* | **404**, which line 87 of that same file already states |

Neither file is edited: both leave the repository — §3 rule 8 for the first,
and the second is the open item at the end of this amendment.

**The cause, recorded once so that no session re-derives it.** The 403 predates
§17.2. While the owner filter was written per view, permission was checked
after the object had been fetched, so a refusal could say *"it exists and is not
yours"*. With the query filtered before it runs, another account's row is not in
the set at all, and 404 is what Django REST Framework produces with no code
written for it. §17.5 keeps **both** codes, each where it is true: **404** where
the data is not in the requester's set, **403** where the data is visible and
the action is what is denied — the accepted guest attempting a write.

**The rule this fixes for the rest of the batch.** A status code is written only
in the record that decides it. ADR 0002 states the doubled test without a code;
ADR 0006 settles 401, 403 and 404; `docs/api-behaviour.md` carries the six-row
table. Repeating a code in a record that does not decide it is how a superseded
number survives a migration.

**Open, and not decided here:** `docs/migration-sources/FLUXO_CADASTRO_E_ISOLAMENTO_POR_CONTA.md` has
no row in the map and is not in the §3 rule 8 list of files that leave. §17.5
treats it as live — it records having corrected that file's step 6 from 403 to
404 on 26/08/2026. It needs an address before the migration closes.

### A19 — F7: the owner column of the medication has no address

**Decided 01/09/2026, session 9.** Adds to: §6, the findings, and to
`docs/migration-sources/DOCS_MIGRATION_MAP.md`, "FINDINGS", which gains row **F7**.

The single most basic fact of the domain model — every medication row carries
the account it belongs to — is stated nowhere as a definition.

`ESTADO_CORRENTE` presupposes it in three places and defines it in none: §17.1
calls it *"o carimbo da conta"*, §3.1 makes the account the first element of the
uniqueness combination (a constraint can only be declared over columns that
exist), and §17.3 speaks of verifying that the medication belongs to the
requester. The only file in the archive that names it as a column — *dono →
conta* on `Medicamento` and on `Doenca`, sourced at `CORRECAO_MODELAGEM...` 219
and 221 — is `docs/migration-sources/FLUXO_CADASTRO_E_ISOLAMENTO_POR_CONTA.md`, line 122.

That file is the one with no address, recorded as **O8** in A18. So the fact
travels only in passing — ADR 0004 says the medication carries its account,
ADR 0007 puts the account inside the uniqueness combination — and the
definition travels nowhere.

**Not fixed here, and the reason matters:** fixing it means giving that file an
address, which is O8, and O8 is a decision for Thaís. `docs/domain-model.md` is
the obvious home, but assigning it is amending the map, not writing an ADR.

**What a session must not do meanwhile:** write the word *column* into an ADR on
the strength of `FLUXO`. ADR 0004 says the medication *carries the account it
belongs to*, which is §17.1 at face value, precisely because the column is not
defined in an addressed source — §3 rule 3.

### A20 — O8 is answered: the flow file splits, and F7 gets its address

**Decided 01/09/2026, session 9.** Supersedes: **O8**, raised in A18. Unblocks:
**F7**, raised in A19. Adds **MAP 3** to `docs/migration-sources/DOCS_MIGRATION_MAP.md`, and adds
`docs/migration-sources/FLUXO_CADASTRO_E_ISOLAMENTO_POR_CONTA.md` to the §3 rule 8 list of Portuguese
files that leave the repository.

The file splits: its facts about the system travel to `docs/domain-model.md`,
and the worked example does not. MAP 3 carries the row-by-row allocation.

**Why the worked example is cut.** The file exists because a doubt was raised —
*what happens when a second account types the same medication?* — and A14 is the
rule for exactly that shape: where the answer changed a decision, the decision
travels; the question never does. Migrating the Maria-and-João walkthrough whole
would open an exception in a rule that has already cut eight rows of this map.

**What replaces it for the reader,** so the cut costs nothing: the README
verification walkthrough (§14.2) has the reader create two accounts, ask for the
other's data and receive 404. It stages the same scene instead of describing it.

**One trap inside the part that travels.** Reason 3 of *why one table and not
one per account* argues from *"o teste do 403"*. That is the stale code of
**F6**. The reason travels; the code does not — A18: a status code is written
only in the record that decides it, and that record is ADR 0006.

### A21 — The ADR rules become a skill, and outlive this plan

**Decided 01/09/2026, session 9.** Adds to: §2, which gains a pointer, and to
the rule set. Does not amend any decision.

The rules for writing an ADR were spread across §2 and §3 of this plan, which
**leaves the repository when the migration ends**. A17 already recorded one rule
lost that way. Session 9 broke four of these rules in a single draft — an
invented context paragraph, an invented positive consequence, a motive
constructed where the source had none, and a stale status code carried into a
record that does not decide it — which is what made the loss concrete.

**Destination:** the `adr` skill, `.claude/skills/adr/SKILL.md`, with
`disable-model-invocation: true`. Thaís' decision, and her reasons: she invokes
it herself when the work calls for it, and it spends no context until then.

`[doc]` Verified at `code.claude.com/docs/en/skills` on 01/09/2026: a skill's
body loads only when the skill is used; the directory name becomes the command;
`disable-model-invocation: true` means only the user can invoke it. Also
verified at `code.claude.com/docs/en/memory` the same day: a `@path` in
`CLAUDE.md` is an **import**, expanded into context at launch, so it is the
wrong mechanism for a file that must not cost context — a path in backticks
stays literal.

**One supporting edit, and without it the skill is invisible:** a section in
`CLAUDE.md` naming the skill and requiring that it be loaded before any ADR is
written. Same argument as A3.

**What stays in this plan:** only what is specific to migrating an archive —
the five points added to §2. The skill holds what is true about writing a
record in any context, including after the migration closes and this file is
gone.

**Open, and it decides how permanent this is:** whether `.claude/` enters the
commit is still **O6**. If it does not, the skill is permanent on Thaís'
machine and absent from the repository.

### A22 — Where a record's content comes from when the archive does not hold it

**Decided 02/09/2026, session 9.** Adds a sixth point to §2, "The rules for
writing one live outside this plan". Does not amend any decision.

The archive does not always hold the motive or the alternative of a decision it
records. Where Thaís supplies either in the migration conversation itself, it
enters the record, and the record stops being verifiable against the archive
alone. That is accepted; what is not accepted is a gap closed by deduction.

**Sixth point of §2:** content supplied by Thaís in conversation travels, and
the session says so when it presents the draft. Content deduced from what the
source writes does not travel. A session that cannot tell the two apart asks —
§3 rule 3, and rule 7 of the `adr` skill, which is where the general form lives.

**The case that produced it.** ADR 0003, custom user model. `ESTADO_CORRENTE`
§12.1 states the decision and one motive — replacing the user model after data
exists is one of the most destructive migrations in Django — and names no
alternative at all. The first draft built two Considered Options backwards from
that motive. Thaís refused it and supplied what was missing: authentication is
by email address, and that requires substituting the user model, which is the
case Django's own documentation names for overriding the default. Both the
options and that driver reached the record from the conversation of 01/09/2026.

**What it costs, and it is accepted:** ADR 0003 cannot be checked against the
archive the way the other records of the batch can. Its `More Information` names
§12.1 and §12.2 — §12.2 carries the email as the identification field, and no
archive file carries the link between that and the user model. The Django
documentation does, and it is not a file of this repository.
