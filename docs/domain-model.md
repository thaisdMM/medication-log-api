# Domain model

What is true about the system's data: entities, fields, relations, and what is
mandatory. Terms are defined in `GLOSSARY.md`; the choices with a real
alternative are ADRs.

## Principles

- **An empty field means one thing: nobody filled it.** When the system needs to
  know a state, that state is a field of its own, never an inference about
  emptiness.
- **Structure what the system must understand; leave free what it only stores
  and returns.**
- **What an account has becomes a relation; what an account is becomes a type**
  — and only if it never changes. This is why a single account type exists.
- **Derivable information is not stored.** A stored copy can disagree with its
  source. No account-type flag; no owner column on the usage period (ADR 0004).

## What is mandatory

Recording anything is optional. An account with zero medications and zero
diseases is a legitimate, permanent state: it has no rows, not empty columns.

| Field | Mandatory |
|---|---|
| Account email, password and name | always |
| Medication name | whenever a medication is saved |
| The medication a usage period belongs to | always — enforced by the foreign key |
| Telegram conversation id | only for an account that uses the bot |

Everything else is optional: concentration, unit, form, dose, frequency, dates.
No field is ever made mandatory to close the duplicate constraint (ADR 0008).

## Account

- Fields: **email, password, name — nothing else.**
- Email is the login identifier; there is no username. Unique, and stored whole
  in lowercase, so one address is one account whatever case it is typed in.
- Password is stored hashed.
- One account table. The admin is a row of it with `is_staff` on — permission
  to operate the system, not an account type, and it does not use the product
  side of the system.
- Owning records and being a guest are simultaneous, reversible situations of
  the same account.

## Medication

One table for every account. Each row carries the account it belongs to (the
owner column).

| Field | Rule |
|---|---|
| owner | the account; set by the system |
| name | free text, mandatory, no minimum length, stored as typed, without leading and trailing spaces; casing never changed |
| concentration value | a decimal greater than zero, three decimal places, optional |
| concentration unit | closed list, optional |
| form | closed list, optional |
| state | in use / suspended |

- **Name and concentration live in one table.** `FUROSEMIDE 5 mg` and
  `FUROSEMIDE 20 mg` are two rows. Separating substance from presentation is
  the modelling of a pharmaceutical catalogue, which is a non-goal. Cost
  accepted: the same name repeats, and grouping by it takes a heavier query.
- **The same name across accounts is intentional.** Two people owning the same
  box is not a duplicate.
- **Duplicate rule:** the same account cannot save the same medication twice —
  owner + case-insensitive name + concentration value + unit + form (ADR 0008).
- **State.** A new medication appears as *in use* without the account doing
  anything; the account marks it *suspended* when it stops. The value is
  overwritten — the system does not record when it changed (non-goals item 20).
  Suspending, rather than deleting, keeps its usage periods; resuming is a new
  usage period.
- **Form list:** tablet · capsule · drop · ml · sachet · patch · suppository ·
  ointment · other. Nine values.
- **Form has no default value.** Left unchosen, it stays empty.
- **Concentration unit list:** mg · g · ml · other.
- **A closed-list field stores empty text, never `NULL`.** Empty text equals
  empty text in the database, so form and unit never break the duplicate rule.
  `null=True` on either brings the hole back.
- **"Other" never carries free text**, in any closed list of the project. It is
  a label to mark. Accounts never add values to any list.

## Usage period

A stretch of time during which an account took one medication.

| Field | Rule |
|---|---|
| medication | mandatory foreign key |
| dose | a bare number, optional |
| frequency | structured: a count and a time unit, optional |
| start, end | structured dates, optional |

- **Medication to usage period is one-to-many**, with no intermediate table.
- **No usage period without a medication.** An account that has registered no
  medication cannot register a usage period.
- **No owner column.** Ownership is found by crossing to the medication
  (ADR 0004). The foreign key makes the link mandatory, not correct: that the
  medication is the requester's own is checked in input validation
  (`docs/api-behaviour.md`).
- **Dose is read in the medication's form.** `FUROSEMIDE · 50 mg · tablet`, dose
  `2`, reads as two tablets. There is no form-and-dose coherence check, because
  there are not two lists to match. Cost accepted: insulin is dosed in
  international units from a pen; an insulin user records pen units.
- **An empty end date means nobody filled it.** It does not mean *in use* — the
  medication state says that.
- **Two usage periods of the same medication may overlap.** Three times a day,
  morning and night, different doses at different hours. The rule that forbade
  it is dropped. Whether another rule replaces it is open
  (`docs/open-questions.md`), as are the frequency values.

## Disease

- A closed list in the database, maintained only by the admin through the
  Django admin panel (ADR 0009). The list rows have no owner.
- An account marks the diseases it has: a many-to-many between account and
  disease. **The owner lives on that link**, not on the disease.
- Optional, independent of medication — the system never asks which
  medication treats which disease.
- The escape option is "other", with no free text (non-goals item 14).
- The admin panel is Django's built-in one, not a feature to build.

## Sharing

- Links account to account. Only an existing account can be invited: the
  inviter supplies its email, and the system locates the account. Email
  identifies an account; it is not a delivery channel.
- The invitee sees the invitation inside the application and accepts or
  declines it.
- **At most one row per pair** of inviter and invitee (ADR 0010). A pending
  invitation cannot be resent; a declined one can be remade, returning the same
  row to pending; different pairs are independent.
- **An account cannot invite itself** (ADR 0011).
- **Scope:** medications, diseases, or both (ADR 0016).
- **Scope is frozen** while the sharing exists (non-goals item 7).
- **The owner ends a sharing at any moment**, with nobody's consent. The guest
  goes back to being refused.
- A guest reads only (non-goals item 9).
- Creating an invitation asks for an email notice through the sending
  abstraction (ADR 0013).

## Telegram conversation id

- The bot replies to the conversation id Telegram assigns; it is stored linked
  to the account. It exists only once the account first talks to the bot,
  because a bot cannot start a conversation.
- It is personal data — it links the account to a Telegram account
  (non-goals item 15).
- **It is not a phone number.** The system never asks for, sees or stores one.
- How the backend confirms that a conversation belongs to an account is open
  (`docs/open-questions.md`). The answer may add a column or a table.

## How accounts stay separated

Every account's rows live in the same tables. Separation comes from three
pieces, and all three must exist:

| Piece | What it does |
|---|---|
| Owner column | stamps each row with its account |
| Owner filter on every query | each account sees only its own rows (ADR 0005) |
| Database constraint | holds what code could forget (ADR 0008) |

The third exists because the first two are code, and code is forgotten.

**Why one table, and not one per account:**

1. The duplicate rule includes the account; in a per-account table that column
   would have no function.
2. Sharing needs the owner's rows while the guest is logged in; per-account
   tables would need the table name discovered at runtime.
3. Isolation is only demonstrable when the data coexists and the system
   separates it.
4. Django generates no migration for tables created at runtime, and every field
   change would multiply by the number of accounts.

One table indexed on the owner column is faster than many tables.
