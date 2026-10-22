# Medication Log API

A personal log of medications and diseases. Each account records its own data
and may grant another account read-only access to it.

## People

**Account**:
Whoever signs up, logs in and records their own medications and diseases. The
only kind of user the system has.
_Avoid_: titular, patient, holder

**Data owner**:
The account a record belongs to. Permission rules are phrased in terms of it.
_Avoid_: creator, author

**Guest**:
An account that has accepted read access to another account's data. A
situation of an account, reversible, never an account type.
_Avoid_: carer, viewer, invitee (once accepted)

**Admin**:
An account with permission to operate the system from inside, through the
Django admin panel. A permission, not an account type.
_Avoid_: staff user, administrator account

## Health records

**Medication**:
A box in someone's drawer: a name typed by the account, with an optional
concentration and form. Not a substance and not a catalogue entry.
_Avoid_: drug, catalogue item, medicine entry

**Medication state**:
Whether the account is currently taking a medication: in use or suspended. An
overwritten value, not a history.
_Avoid_: status history, active flag

**Usage period**:
A stretch of time during which an account took one medication, with optional
dose, frequency, start and end.
_Avoid_: usage, prescription, treatment

**Form**:
How a medication is presented — tablet, capsule, drop and so on. The unit in
which its dose is read.
_Avoid_: dose unit, presentation

**Concentration**:
The amount of active substance per unit of a medication, as printed on the
box: a number and a unit.
_Avoid_: dosage, strength, milligramage

**Dose**:
How many units of the form are taken at once. A bare number.
_Avoid_: dosage, quantity

**Disease**:
An entry of the closed list of diseases that only the admin maintains. An
account marks the ones it has.
_Avoid_: condition, diagnosis, illness

## Sharing

**Sharing**:
The relation through which a data owner grants one other account read access
to part of their data. At most one per pair of accounts.
_Avoid_: share, permission, access grant

**Invitation**:
A sharing that the invited account has not yet accepted or declined.
_Avoid_: invite link, request

**Scope**:
What a sharing grants: medications, diseases, or both. Never nothing.
_Avoid_: permissions, access level
