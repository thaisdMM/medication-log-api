# API behaviour

How the API answers: status codes by situation, and what reads and writes
verify. Why 404 and not 403 is ADR 0006.

## Response by situation

Applies to every endpoint that serves an account's data.

| Situation | Response | Why |
|---|---|---|
| no token | **401** | the requester did not identify itself |
| data owner | allowed | it is theirs |
| account with no relation asking for another's data | **404** | the data is not in its set |
| guest whose sharing is **pending** | **404** | no access yet; the data is not in its set |
| accepted guest, **reading** inside the scope | **200** | what the sharing grants |
| accepted guest attempting to **write** | **403** | the data is visible; the action is refused |
| accepted guest asking for what is **outside the scope** | **404** | that part is not in its set |

404 holds for listing and for fetching by id. Other responses enter as
implementation needs them; this table is open by nature.

## Reads and writes are verified separately

The owner filter (ADR 0005) protects **reading** — listing, and fetching by id.

It does not protect **creating**: nothing in it stops an account from creating a
usage period that points at another account's medication by sending that
medication's id. That the medication belongs to the requester is checked
separately, in input validation.

## Validation errors

A request the API refuses for its content answers 400 with a message saying
what is wrong — never 500. This includes a duplicate the database refuses
(ADR 0008).

## Neutral response to an unknown email on invitation

Inviting an email answers the same thing whether or not an account has that
address. Neither the account's name nor its existence is revealed. Accepted
consequence: whoever mistypes the address does not find out.

**Not to be confused:** registration reports a duplicate email as such. A
neutral answer there would need real email delivery, which is a non-goal.
