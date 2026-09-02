# DOCUMENTATION MIGRATION — ALLOCATION MAP

**Written:** 30/08/2026, session 2.
**Approved by Thaís:** 30/08/2026.

Every section of `docs/migration-sources/ESTADO_CORRENTE_23_08_2026.md` and every item of
`docs/migration-sources/ETAPA2_LEVANTAMENTO_DECISOES_FORA_DO_ESTADO_CORRENTE.md`, with its final
address. Sessions 3 to 9+ cite these addresses even before the files exist —
§3 rule 6 of `docs/migration-sources/DOCS_MIGRATION_PLAN.md`.

This file is temporary. It leaves the repository when the migration finishes.

## Target addresses

```
docs/adr/NNNN-<slug>.md      thirteen records, MADR template
docs/domain-model.md         entities, fields, relations, mandatory fields
docs/api-behaviour.md        status codes, owner filter, permission tests
docs/definition-of-done.md   what must be verified before a slice is done
docs/non-goals.md            the 22 excluded items
docs/glossary.md             usuário, dono do dado, convidado
docs/open-questions.md       what is not decided, and what it blocks
docs/roadmap.md              slices, vertical-slice method, slice 0 tooling
README.md                    purpose, base constraints, stack, walkthrough
```

`docs/api-behaviour.md`, `docs/definition-of-done.md` and `docs/roadmap.md` are
not in the list proposed by §5 O2 of the plan. Added in session 2 — plan §8,
amendments A9 and A11.

## Types used in the map

| Type | Meaning |
|---|---|
| **ADR** | a decision that had a documented alternative |
| **spec** | what is true about the system |
| **cut** | does not become project documentation |
| **delivered** | already written, session 1 |

## The ADR set — thirteen

| # | Title | Source | Session |
|---|---|---|---|
| 0001 | Hosting on Render with Neon | `DECISAO_HOSPEDAGEM.md` | 3, pilot |
| 0002 | Level-2 authentication: multiple users with isolated data | ETAPA2 B1 | 9+ |
| 0003 | Custom user model before the first migration | §12.1 | 9+ |
| 0004 | Ownership discovered through the medication, no owner column | §17.1 | 9+ |
| 0005 | Owner filter in a single point of the code | §17.2 | 9+ |
| 0006 | 404, not 403, for data outside the requester's set | §17.5 | 9+ |
| 0007 | Duplicate constraint with `nulls_distinct=False` | §3.1–3.6 | 9+ |
| 0008 | Disease list in the database, not in code | §5.2 | 9+ |
| 0009 | One sharing row per pair of accounts | §6.2 | 9+ |
| 0010 | An account cannot invite itself | §6.10 | 9+ |
| 0011 | Telegram by webhook, not long polling | §7.4 | 9+ |
| 0012 | Email to console in every environment, production included | §8 + §6.7 | 9+ |
| 0013 | Interactive API documentation published | §14.1 | 9+ |

---

## MAP 1 — `docs/migration-sources/ESTADO_CORRENTE_23_08_2026.md`

| Source | Destination | Type | Note |
|---|---|---|---|
| Header, procedência, correção 26/08 | — | cut | Provenance of a file that leaves the repository |
| §0 Project confirmed | `README.md` | spec | Purpose only; the audit reasoning does not travel |
| §1.1 What is mandatory | `docs/domain-model.md` | spec | Merges with ETAPA2 D9 |
| §1.2 Retratação | — | cut | Wrong position abandoned before any implementation |
| §1.3 Meaning is never inferred from an empty field | `docs/domain-model.md` | spec | One line, no attribution |
| §1.4 Three levels of rule | — | cut | Internal criterion. Breaks the citation in §13.7 — F5 |
| §2 Medication state | `docs/domain-model.md` | spec | State is overwritten, never a timeline |
| §3 (23/08, superseded) | ADR 0007 | ADR | **Only** the two options survive, as Considered Options |
| §4 Single account type | `docs/domain-model.md` | spec | Transferable rule kept, worked example dropped |
| §4.1 usuário / dono do dado / convidado | `docs/glossary.md` | glossary | With ETAPA2 G1 |
| §5 (23/08, superseded) | ADR 0008 | ADR | Only the options survive |
| §6 (23/08, superseded) | ADR 0009, ADR 0010 | ADR | Scope vs all-or-nothing becomes Considered Options |
| §7.1 Telegram is the integration | ADR 0011 | ADR | |
| §7.2 Prior status corrected | — | cut | Records an unconfirmed Claude proposal |
| §7.3 What was verified about bots | ADR 0011 | ADR — Context | Verified research, still operative |
| §7.4 Webhook, not long polling | ADR 0011 | ADR — Decision Outcome | |
| §7.5 Hibernation vs Telegram timeout | `docs/open-questions.md` | open | Research not authorized; status unchanged |
| §7.6 Chat id is personal data | `docs/domain-model.md` | spec | The field, and that it is never a phone number |
| §7.6 chat↔account binding | `docs/open-questions.md` | open | One entry with ETAPA2 E1, not two |
| §8 Email | ADR 0012 | ADR | Abstraction, backend by environment variable |
| ~~§8 Cost research deferred~~ | — | **cut** | **CUT 30/08/2026, session 6.** ADR 0012 sends email to the console in every environment, production included. No provider is ever configured, so there is no cost to research |
| §9 Evaluation criteria | — | cut | Portfolio criterion, not system truth |
| §9 item 3 | `docs/definition-of-done.md` | DoD | Already 404 |
| §10 Rule E6 | — | cut | Conversation conduct, delivered in session 1 |
| 24/08 table of 16 subjects, and its correction notes | — | cut | Bookkeeping. Line 436 is F2 |
| §3.1 Uniqueness combination | ADR 0007 | ADR | account + name + value + unit + form |
| §3.2 Form has no default value | ADR 0007, `docs/domain-model.md` | ADR + spec | Contradicts ETAPA2 D5 — F3 |
| §3.3 `nulls_distinct=False` | ADR 0007 | ADR — Decision Outcome | Keep "verified in documentation, never executed" |
| §3.4 No mandatory field closes the constraint | ADR 0007 | ADR — Consequences | |
| §3.5 Fallback positions, in order | ADR 0007 | ADR — Consequences | Forward-looking, both kept in order |
| §3.6 Derived mandatory test | `docs/definition-of-done.md` | DoD | 400 with a validation message, never 500 |
| §3.7 Discarded proposal, conditional mandatory fields | — | cut | What it proved is already §3.4 |
| §3.8 Claude error | — | cut | |
| §3.9 Form list, nine values | `docs/domain-model.md` | spec | "outros"; the escape option carries no free text, project-wide |
| §3.10 Experiment | `docs/open-questions.md` | open | Blocks §3.2, §3.5, §3.6, §3.9, §13.5. **Absorbs ETAPA2 H2 — one entry, not two** (session 6) |
| §5.1 Disease is optional and independent | `docs/domain-model.md` | spec | |
| §5.2 List lives in the database | ADR 0008 | ADR | |
| §5.3 Only the admin adds diseases | `docs/domain-model.md` | spec | |
| §5.4 Django admin panel | `docs/domain-model.md` | spec | Built-in panel, not a feature to build |
| §5.4 Health-data exposure through the admin panel | `docs/definition-of-done.md` | DoD | **Split 30/08/2026, session 6.** Registering medication, usage, disease or sharing in the panel gives every `is_staff` account the health data of all accounts. Verified when the panel is built |
| ~~§5.4 Which models are registered in the panel~~ | — | **cut** | **CUT 30/08/2026, session 6.** A trivial implementation choice, and the source already says it is not decided here. The alert it carried is the row above |
| §6.1 Internal invitation between accounts | `docs/domain-model.md` | spec | Email identifies the account, it is not a delivery channel |
| §6.2 One row per pair | ADR 0009 | ADR | |
| §6.3 Sharing scope | `docs/domain-model.md` | spec | Permission asks two questions |
| §6.4 Owner ends the sharing | `docs/domain-model.md` | spec | Revokes "revogação" in the non-goals list — session 6 |
| §6.5 Scope frozen after acceptance | `docs/non-goals.md` | non-goal | Excluded by time cost, not by product objection |
| §6.6 Neutral response to an unknown email | `docs/api-behaviour.md` | spec | Same reasoning as ADR 0006 |
| §6.7 Email notice decoupled | ADR 0012 | ADR | |
| §6.8 What is not possible | `docs/non-goals.md` | non-goal | |
| §6.9 Registration correction | `docs/non-goals.md` | non-goal | Boundary only: the excluded thing is the tokenised link |
| §6.10 No self-invitation | ADR 0010 | ADR | Declared in the database, not only in Python |
| §6.11 No limit on sharings | `docs/non-goals.md` | non-goal | Item 18. The "one or two relatives" archaeology is cut |
| §12.1 Custom user model | ADR 0003 | ADR | |
| §12.2 Login by email | `docs/domain-model.md` | spec | Email, password, name, and nothing else |
| §12.2 OAuth out of scope | `docs/non-goals.md` | non-goal | Would be a second external integration |
| §12.3 One account table | `docs/domain-model.md` | spec | SkillBridge comparison cut |
| §13.1 Name is free text | `docs/domain-model.md` | spec | Disambiguation of the word "catálogo" is cut |
| §13.2 Spell-checking out of scope | `docs/non-goals.md` | non-goal | |
| §13.3 Typos out of scope | `docs/non-goals.md` | non-goal | |
| §13.4 Name stored exactly as typed | `docs/domain-model.md` | spec | |
| §13.5 Duplicate comparison ignores case | ADR 0007, `docs/domain-model.md` | ADR + spec | The unverified `NULL`-expression caveat travels with it |
| §13.6 Discarded proposal, shadow column | — | cut | |
| §13.7 Name is mandatory, no minimum length | `docs/domain-model.md` | spec | |
| §14.1 Interactive documentation | ADR 0013 | ADR | Served by Django itself, no new service |
| §14.2 README walkthrough | `README.md` | README | Ends in 404 |
| §14.3 Telegram is not the shop window | ADR 0013 | ADR — Consequences | |
| §14.4 "Órfã" revoked | — | cut | |
| ~~§14.5 Which OpenAPI library~~ | — | **cut** | **CUT 30/08/2026, session 6.** A library choice made at install time. The source itself says it is not decided here; recording it as an open question records a non-question |
| §15, §15.1, §15.2, §15.3 Deadline and estimate | — | cut | Internal. No current estimate is a fact, not a pending item |
| §16.1 REST API only, no UI | `README.md`, `docs/non-goals.md` | README + non-goal | "Excluded scope, not technical debt" survives |
| §17.1 No owner column on the usage period | ADR 0004 | ADR | The owner column is the Considered Option, without attribution |
| §17.2 Owner filter in a single point | ADR 0005 | ADR | A new endpoint that omits the path fails on the first call |
| §17.3 Writes verified separately from reads | `docs/api-behaviour.md` | spec | |
| §17.4 Three items for the definition of done | `docs/definition-of-done.md` | DoD | |
| §17.4-A No usage period without a medication | `docs/domain-model.md` | spec | Mandatory by the foreign key |
| §17.5 404, and the three-code table | ADR 0006, `docs/api-behaviour.md` | ADR + spec | The choice is the ADR; the six-row table is the spec |
| §17.5 Other responses may appear | `docs/api-behaviour.md` | spec | Open by nature, not a pending item |

---

## MAP 2 — `docs/migration-sources/ETAPA2_LEVANTAMENTO_DECISOES_FORA_DO_ESTADO_CORRENTE.md`

| Source | Destination | Type | Note |
|---|---|---|---|
| Header, procedência, origin marks, block summary | — | cut | |
| A1 Thaís writes the code | `CLAUDE.md` rule 13, `django-mentor` skill | delivered | Plan §8 A1 |
| A2 Free hosting with a €5–10 valve | ADR 0001 | ADR — Context | **Fixes F1** — this is the address, not §16.2 |
| A3 Cron allowed, permanent worker forbidden | `README.md`, `docs/non-goals.md` | constraint | Contradiction with non-goals item 17 recorded, not fixed |
| ~~A4 Firebase, Supabase and BaaS discarded~~ | — | **cut** | **CUT 30/08/2026, session 6 — plan §8 A15.** Nothing was weighed and rejected; the question was settled by what the project already is. Recording it would tell a reader the category was once a candidate here |
| A5 Exactly one external integration | `README.md`, ADR 0011 | constraint | The counting trap sustains the §8 watch |
| ~~A6 Real-utility domain, scope frozen on day 1~~ | — | **cut** | **CUT 30/08/2026, session 6.** Working method, not system truth — the same ground on which §9 was cut. The scope that was frozen is stated by `docs/non-goals.md`, which is the artefact; the act of freezing it is not documentation |
| A7 Data and ML outside the domain | `README.md`, `docs/non-goals.md` | constraint | In neither list today |
| A8 Reuse SkillBridge knowledge | — | cut | Working criterion, internal |
| ~~A9 Hosting platform never chosen~~ | — | **cut** | **CUT 30/08/2026, session 6.** Fully closed by ADR 0001: the platform is Render + Neon, and all three "a reverificar" data points are settled in its Context |
| B preamble, levels 1 and 2 | ADR 0002 | ADR — Considered Options | The **technical cost** of level 2 travels: token authentication on the API, owner filtering in every query, tests doubled. The learning-value argument does not — A14 |
| B1 Level 2 chosen | ADR 0002 | ADR | The decision the project exists to prove |
| B2 `simplejwt` vs Django 6.x | `docs/open-questions.md` | open | Caveat written about 6.0; environment is 6.1 |
| B3 Mandatory permission test table | `docs/api-behaviour.md`, `docs/definition-of-done.md` | spec + DoD | Two defects recorded, not fixed — F4 |
| B4 Name and email never in logs | `docs/definition-of-done.md` | DoD | Error logs are the hard case |
| C1 Vertical slice | `docs/roadmap.md` | roadmap | Session 4 |
| C2 Full tooling from slice zero | `docs/roadmap.md`, `README.md` | roadmap + stack | DRF confirmed — plan §8 A6 |
| ~~C3 First slice after authentication~~ | — | **cut** | **CUT 30/08/2026, session 6.** Answered by `docs/task-slices/0001-roadmap.md`: slice 2 is medication, and the whole order is fixed |
| D1 "No two active uses" rule dropped | `docs/domain-model.md` | spec | |
| D1 Whether a rule replaces it | `docs/open-questions.md` | open | |
| D2 Structured frequency | `docs/domain-model.md` | spec | Count and time unit, dates structured too |
| D3 Structure what the system must understand | `docs/domain-model.md` | spec | Paired with §1.3 |
| D4 Dose is just a number | `docs/domain-model.md` | spec | Insulin trade-off kept |
| D5 Form, closed list with escape option | `docs/domain-model.md` | spec | Merges into §3.9. Its default value is revoked — F3 |
| D6 Concentration: free number, closed unit list | `docs/domain-model.md` | spec | Open units go to H1 |
| D7 Medication is name and concentration in one table | `docs/domain-model.md` | spec | Not an ADR — plan §8 A11 |
| D8 Medication↔usage period is one-to-many | `docs/domain-model.md` | spec | Records which relations are not many-to-many |
| D9 Mandatory-field table | `docs/domain-model.md` | spec | Four items, chat id only for bot users |
| E1 How the bot proves account ownership | `docs/open-questions.md` | open | Same entry as §7.6 |
| E2 No phone number is needed | `docs/domain-model.md` | spec | The fact travels; the corrected assumption does not |
| F1 Versioned history | `docs/non-goals.md` | non-goal | Item 20 — session 6 |
| F2 LLM service | — | cut | Decided not to become an item |
| F3 Calendar and scheduling | `docs/non-goals.md` | non-goal | Item 21 — session 6 |
| G1 "Titular" retired | `docs/glossary.md` | glossary | Its "situação hoje" is stale — F3 |
| H1 Concentration units beyond mg, g, ml | `docs/open-questions.md` | open | |
| H2 Which forms, and whether "não informada" is one | `docs/open-questions.md` | open | **Merged into the §3.10 entry, session 6.** It is not a separate question: it is what the experiment decides |
| H3 Which frequency values | `docs/open-questions.md` | open | |
| H4 Does frequency have "outro" | `docs/open-questions.md` | open | |
| ~~H5 Does "outro" in the unit carry free text~~ | — | **cut** | **CUT 30/08/2026, session 6.** §3.9 answered it project-wide: no escape option anywhere carries free text |
| ~~H6 Confirm "outras" in disease carries no free text~~ | — | **cut** | **CUT 30/08/2026, session 6.** Same answer, and `docs/non-goals.md` item 14 already states it |
| "O que não entrou neste levantamento" | — | cut | |

---

## MAP 3 — `docs/migration-sources/FLUXO_CADASTRO_E_ISOLAMENTO_POR_CONTA.md`

**Added 01/09/2026, session 9 — plan §8 A20.** The file had no address until
then; O8 recorded the gap and this map section closes it.

| Source | Destination | Type | Note |
|---|---|---|---|
| Header, "what this document is", provenance, "the misunderstanding this undoes" | — | cut | Provenance of a file that leaves, plus the doubt that produced it — A14 |
| Step-by-step, Maria and João, lines 38–95 | — | cut | The worked example answering that doubt — A14. The README walkthrough stages the same scene |
| The mistyped name in this design, lines 98–111 | — | cut | Restates non-goals items 11 and 12, already written |
| The owner column — *dono → conta* on `Medicamento` and `Doenca`, line 122 | `docs/domain-model.md` | spec | **Fixes F7.** The only place in the archive that names the column. Sourced at `CORRECAO_MODELAGEM...` 219 and 221 |
| The three pieces that produce isolation, lines 120–127 | `docs/domain-model.md` | spec | Owner column, owner filter on every query, database constraint. The third exists because the first two are code, and code is forgotten |
| Why one table and not one per account, lines 131–159 | `docs/domain-model.md` | spec | Four reasons. Reason 3 argues from *"o teste do 403"* — **F6**: the reason travels, the code does not |
| Performance of one indexed table over many, lines 151–153 | `docs/domain-model.md` | spec | |
| Repeating a medication name across accounts is intentional, lines 155–159 | `docs/domain-model.md` | spec | The table holds the box in someone's drawer, not the substance |
| The usage period, lines 163–184 | — | cut | Restates §17.1 and §17.2, which are ADR 0004 and ADR 0005 |

---

## CUTS THAT APPLY TO EVERY SECTION

Not one row of the map, and they must be applied while writing each destination:

1. **Audit-closure lines.** *"Isso encerra o achado AUD-05"*, and the same
   sentence in §5.2, §6.10, §6.11, §15.3 and §16.1. The audit file leaves the
   repository; the pointer would aim at nothing.
2. **Reconciliations between two historical files.** Any passage whose only work
   is to say which of two files that leave the repository was wrong — §13.1, §7.2,
   §14.4, §15.1, and the "one or two relatives" paragraph of §6.11.
3. **Verbatim quotations and attribution in the body** — D8. Attribution is the
   `decision-makers` field of the front matter.
4. **Who proposed what, and who withdrew it.** A rejected alternative travels as
   a Considered Option with its technical reason, never as an account of the
   conversation that rejected it.
5. **A question that was asked and answered, and any comparison with another
   project.** Added 30/08/2026, session 6 — plan §8 **A14**. The source files
   record doubts raised and settled in conversation, and passages that reason
   about this project by contrast with SkillBridge or with work done elsewhere.
   Neither states what is true about this system. Where the answer changed a
   decision, the decision travels; the question never does.

   Read every remaining row through this cut before writing its destination. A
   row can survive the map and still carry nothing: **A4 is the first one cut
   whole on this ground** — plan §8 A15.

## FINDINGS

| # | Finding | Fix in |
|---|---|---|
| **F1** | `DECISAO_HOSPEDAGEM.md` line 78 cites `§16.2`, which does not exist. The fact is item A2 of the Etapa 2 survey | session 3 |
| **F2** | `ESTADO_CORRENTE` line 436 says the non-goals list has 19 items. It has 22 | session 6 |
| **F3** | ETAPA2 D5 still describes the form default `"não informada"`, revoked by §3.2 on 26/08. ETAPA2 G1 still says the current state uses "titular" in §7.1, §6.3 and §6.4; those sections say "usuário" and "dono" today | session 9+ |
| **F4** | The B3 permission-test table answers **403** where §17.5 decided **404** — account with no relation, and pending guest. The row for an accepted guest asking outside the invitation scope is missing | session 9+ |
| **F5** | §13.7 cites the table of §1.4, which the map cuts. The conclusion of §13.7 stands without it; the citation does not | session 9+ |
| **F6** | The stale 403 of F4 appears twice more, outside the B3 table: `ETAPA2` line 214, in the block B preamble, describes the doubled test as *"outro usuário, que tem que receber 403"*, and `docs/migration-sources/FLUXO_CADASTRO_E_ISOLAMENTO_POR_CONTA.md` line 144 calls the isolation proof *"o teste do 403"*. §17.5 answers **404** in both. **Recorded 01/09/2026, session 9 — plan §8 A18** | recorded, not fixed |
| **F7** | The owner column of the medication and of the disease has no address. `ESTADO_CORRENTE` presupposes it and never defines it — §17.1 calls it *"o carimbo da conta"*, §3.1 makes the account the first element of the uniqueness combination, §17.3 speaks of the medication belonging to the requester. The only file that names it as a column, *dono → conta* on `Medicamento` and `Doenca`, is `docs/migration-sources/FLUXO_CADASTRO_E_ISOLAMENTO_POR_CONTA.md` line 122 — the file with no address of O8. **Recorded 01/09/2026, session 9 — plan §8 A19; addressed the same day by A20**, which sends that line to `docs/domain-model.md` — MAP 3 | the session that writes `docs/domain-model.md` |

## WHAT THIS MAP DOES NOT DECIDE

- The content of any destination file. It assigns addresses only.
- The ADR file slugs. Only the numbers and titles above are fixed.
- Whether `FATIA0_TAREFA_0*_CONCLUIDA.md` is translated or archived — O3,
  session 8.
- Which parts of `METODO_DE_TRABALHO_E_FORMATO_DAS_TAREFAS.md` survive — O4,
  session 7.
- Whether `.claude/skills/` enters the commit — O6.
