# Slice 7 — the task list

The tasks of slice 7, in order, with what each delivers and what breaks if
it goes wrong. Not a step-by-step — each task's step-by-step lives in its
own completion record.

## What the slice delivers

From `0001`: a command to the bot returns the sender's own medication list;
the README is updated as the slice's last task. The slice ends only when this
runs in production.

## Numbering rule

Same as `0002`: tasks are never inserted mid-list or renumbered. A new task
enters inside an existing one, or appended at the end (7.7 onward).

## The list

| # | Task | Delivers | Breaks if wrong |
|---|---|---|---|
| 7.1 | Decisions recorded | ADR for account linking by deep link; ADR for replying inside the webhook response; the WhatsApp research in `docs/research/`; the linking question closed in `docs/open-questions.md` and `docs/domain-model.md`; WhatsApp as a later-release item in `0001` | the code of 7.3 to 7.5 rests on decisions written nowhere |
| 7.2 | Bot and webhook live | the bot created; `POST /api/telegram/webhook/` checks the secret token Telegram sends (403 when wrong) and answers 200 doing nothing else; the webhook registered with Telegram; the hibernation test run against production, with a keep-awake ping if updates are lost. Branch and pull request | built last, a lost update after hibernation is found when the whole slice depends on it; without the secret check, anyone can post fake updates to the endpoint |
| 7.3 | Link model and link endpoints | the link (one account, one chat, chat id unique, deleted with the account) and the link code (stored as a hash, valid for 10 minutes, single use; a new code cancels the unused ones); `POST`, `GET` and `DELETE /api/telegram/link/`; 401 without a token. Branch and pull request | a code stored in plain text works for whoever reads the database; a code with no expiry turns any leaked link into a permanent way in |
| 7.4 | Linking through `/start` | the webhook reads `/start <code>`, links the chat to the code's account and replies; an expired, used or unknown code gets one same reply. Branch and pull request | different replies for expired, used and unknown codes help whoever is guessing codes |
| 7.5 | Bot commands | `/list` replies with the account's medications in use (name, concentration and unit); `/help`; an unknown command or plain text gets the `/help` text; an unlinked chat gets a short reply on how to link. Branch and pull request | a list built without the owner filter sends one account's medications to another account's chat |
| 7.6 | Slice proven in production | linking, `/list`, unlinking and an unlinked chat run against the public address; the README gets a "Telegram bot" section with a screenshot of the conversation; the slice closes in its record | without it, "slice 7 is live" is opinion |

## Decisions

* Linking: an authenticated endpoint returns `t.me/<bot>?start=<code>`; the
  account opens it and Telegram sends `/start <code>` to the webhook, which
  stores the chat id. Done once; after that the bot needs no link, login or
  token.
* Link code: random, made only of the characters Telegram accepts in the
  start parameter; only its hash is stored; valid for 10 minutes; single
  use; a new code cancels the account's unused ones.
* One chat for one account; a new link replaces the old one.
* Link storage: a table of its own, not a column on the account, so the
  account model is unchanged; deleting the account deletes the link.
* Link endpoints: `POST` returns the deep link, `GET` says whether a link
  exists and since when, `DELETE` unlinks. `/api/users/me/` is unchanged.
* Unlinking through the bot is left to the later release.
* Commands: `/start <code>`, `/list` and `/help`. Bot replies in English.
* `/list`: medications in use only, with name, concentration, unit and form.
* The bot replies inside the webhook response (`"method": "sendMessage"`):
  no outgoing HTTP call and no Telegram library. Whether the reply was
  delivered is not visible to the backend.
* Webhook: Telegram's secret token is checked on every request. The bot token
  and the secret token live in environment variables on Render.
* Chat id: `BigIntegerField` (Telegram ids go up to 52 bits).
* Tests use the Django test client only; nothing calls Telegram.
* Local development sends simulated updates; the real check happens in
  production.

## Carried, not part of this slice

* WhatsApp Cloud API integration: a later-release item. It needs a second
  phone number, and non-goals item 4 must be revoked by an ADR first.
* Sending replies through an outgoing HTTP call, which would show whether a
  reply was delivered.
* The follow-ups listed on the first release map: the CSRF failure page and
  the expired-token cleanup.
