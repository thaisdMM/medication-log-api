# Non-goals

What this project deliberately does not do, and why. Every item is a choice.
None is technical debt: technical debt is doing something wrong on purpose to
ship faster, and it charges interest. A boundary drawn on purpose charges
nothing.

## 1. A user interface

No screens. The project is a REST API and nothing else.

A UI is the project's largest scope multiplier, estimated at 40–50% of total
time. A REST API without a UI is not an incomplete API.

What solves visibility instead: published interactive API documentation plus
the README walkthrough (ADR 0013).

## 2. Anything that makes it a clinical tool

No drug-interaction alerts, no dose calculation, no reminders to take
medication.

A system that advises on medication is a different product category with a
different liability. This one stores what was typed and gives it back.

## 3. An elaborate permission model

No roles, no external carer, no account-type flag, no tokenised invitation
link.

**Not excluded, and the distinction matters:** invitation with acceptance
exists — the inviter supplies an existing account's email, and the invitee
accepts or declines inside the application (`docs/domain-model.md`). Revocation
exists — the owner ends a sharing at any moment, with nobody's consent.

There is one account type only: owning your own records and being someone's
guest are simultaneous, reversible situations of the same account. The admin is
a row of the same table with `is_staff` on, which is permission to operate the
system, not an account type.

## 4. A second external integration

Exactly one exists: Telegram, query mode, by webhook (ADR 0011).

Sign-in with Google or GitHub is out, because it would be the second. If email
ever sends for real in production the project has two, and the one-integration
constraint must be revoked explicitly before that happens.

## 5. Real email delivery

Nobody receives email. The destination is the console, production included
(ADR 0012).

The invitation notice goes through the sending abstraction, and with no
provider configured the invitation works identically.

## 6. Inviting someone who has no account

Only an existing account can be invited.

It would require a tokenised invitation link, excluded in item 3, and real
email delivery, which will not exist. Email identifies an account; it is not a
delivery channel.

## 7. Changing the scope of an accepted sharing

Scope is frozen while the sharing exists. To change it, the owner ends it and
invites again.

Excluded on time cost, not on product objection: the mechanism is known and
solvable, and would need a fresh acceptance, with proposed and current scope
coexisting on one row.

## 8. Limiting how often a declined invitation can be remade

A declined invitation can be remade, and the system does not count attempts.

There is at most one sharing row per pair of accounts (ADR 0009). Remaking a
declined invitation is that row returning to pending.

## 9. Editing by anyone who is not the data owner

Whoever receives access to another account's data reads only — no writes, no
edits, no deletes.

Health data is sensitive, and only the data owner manipulates their own
records. Sharing grants reading; editing never leaves the owner.

## 10. Registering another person's health data

Each account registers only what is its own. Accounts are not created to hold
someone else's records.

Consistent with a single account type, which has no category for registering on
another's behalf.

## 11. An external medication catalogue, and spell-checking

The medication name is free text. There is no official medication database, no
list to choose from, and no spelling correction.

**Not to be confused:** each account has its own medication table. What is out
is an external base.

## 12. Defending against a mistyped name

A name typed wrong is accepted as typed. Not the system's responsibility.

## 13. Normalising the medication name on write or on display

The name is stored exactly as typed and returned unchanged — no upper-, lower-
or title-casing.

**Not to be confused:** the duplicate comparison ignores case (ADR 0007).
`Dipirona` and then `dipirona` is a duplicate, and the second is refused, while
the first keeps the spelling it was given.

## 14. A disease outside the closed list, or added by the user

Disease is chosen from a closed list whose escape option carries no free text.
A regular account never adds a disease; only the admin does, through the Django
panel.

The universe of diseases is open-ended, and a closed list of the widely known
ones with an escape option is the scoped answer. An account whose disease falls
outside it is an accepted consequence of a short project.

## 15. Personal data with no function in the system

The system stores name, email and password. No date of birth, no phone number,
no identity document, no address.

**One necessary exception:** an account that uses Telegram stores the bot
conversation id — without it the bot has nowhere to reply. That is personal
data, because it links this account to a Telegram account, and it is declared
here rather than left implicit.

**It is not a phone number.** The system never asks for, sees or stores one. An
account that never talks to the bot never has the field at all.

Everything else stays out by data minimisation. Email exists because the
invitation uses it to locate the other account.

## 16. Identity verification

No checking of personal documents, no civil identity confirmation.

Data minimisation again: an identity document is an even more sensitive
category of personal data, widening the exposure surface and the GDPR/LGPD
compliance burden with no real need. The data recorded is the account's own,
about itself, and does not depend on third-party confirmation to have value
here.

## 17. A permanent background worker

No process running around the clock waiting on a queue. This is why Telegram
works by webhook rather than long polling (ADR 0011), and it follows from the
free hosting decision (ADR 0001).

**Not excluded — a scheduled task is allowed.** A permanent worker is a second
process alive 24/7 against a queue; a scheduled task is a command that runs at
a fixed time, executes and dies — a Django management command plus the
platform's scheduler. Free tiers support the second.

No decision in this project uses one today. What this item settles is the
boundary, so that needing one later does not reopen the hosting decision.

## 18. Limiting how many sharings an account makes

An account shares with as many people as it chooses. The system does not count
and does not limit.

## 19. Real data in the public environment

The published environment carries fictitious data only.

Health data is a special category, and the system is designed never to hold
real data in a public environment.

## 20. Versioned history

The system does not answer *"what was I taking on 15 March"*. It stores no
previous version of a record, and no date on which a field changed.

Costed at 145–180 hours, which overruns the project. Recorded as a possible
evolution, not as debt.

**Not excluded, and this is the item's boundary:**

- Medication state — in use / suspended — exists as an overwritten value, not a
  timeline. An account suspends instead of deleting, and marks it in use again
  on resuming.
- Usage periods with a start and an end exist, several per medication. That is
  a timeline typed by the person, not automatic versioning.

The question that crosses the boundary, and the answer is no: *on what day did
this medication change state?*

## 21. A calendar and appointment scheduling

The system books no appointments, holds no calendar and schedules nothing.

It is a personal medication log. Appointment scheduling is a medical product —
the same boundary as item 2.

## 22. Data science and machine learning

No model training, no fine-tuning, no model evaluation, no data pipeline, and
no data analysis anywhere.

This is a Python web backend project, and the portfolio exists to prove that.

**Not excluded, and this is the boundary:** consuming an external service from
the backend and serving the result through the API — exactly what Telegram does
(ADR 0011).
