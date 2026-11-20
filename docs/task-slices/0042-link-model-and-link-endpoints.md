# Slice 7, task 7.3 — done

# Link model and link endpoints

Two pull requests: the models first, then the endpoints.

## The models

- `src/telegram/models.py`:
  - `TelegramLink`: one account, one chat. The account is a one-to-one
    field and the chat id a unique `BigIntegerField`; `linked_at` is set when
    the link is made. Deleting the account deletes its link
  - `TelegramLinkCode`: the account, the SHA-256 of the code and its expiry.
    The code itself is never stored. Deleting the account deletes its codes
  - `TelegramLinkCode.objects.issue(account)`: draws a code with
    `secrets.token_urlsafe(32)`, made only of the characters Telegram accepts
    in the start parameter, valid for 10 minutes. In one transaction it
    deletes the account's earlier codes and stores the new hash
- `src/telegram/migrations/0001_initial.py`: the two tables
- `src/telegram/tests/test_models.py`: the unique chat, one link per account,
  both rows deleted with the account, the code's characters, the hash
  stored instead of the code, the expiry, earlier codes cancelled and other
  accounts' codes kept, string forms without personal data
- Each new test seen failing against a deliberate break:
  - Chat id no longer unique — a second account was linked to the same chat
  - Account no longer unique on the link — an account got a second link
  - Account deletion protected by the link — deleting the account was refused
  - Account deletion protected by the link code — deleting the account was
    refused
  - Code ending with a character Telegram refuses — the code failed the
    start parameter pattern
  - Code stored as it is — the database held the code instead of its hash
  - Code valid for a day — the expiry was past the link code lifetime
  - Earlier codes kept on issue — the account kept more than one code
  - Codes of every account deleted on issue — another account's code was
    removed
  - Link string form showing the chat id — the string form held personal data
  - Code string form showing the hash — the string form held the hash
- Pull request merged with every CI check passing; the production checks
  below show both tables in the database

## The endpoints

- `src/config/settings.py`: `TELEGRAM_BOT_USERNAME` read from the
  environment, empty by default
- `src/telegram/serializers.py`: the deep link with its expiry, and the
  moment the link was made, without the chat id
- `src/telegram/views.py`, `TelegramLinkView` on `/api/telegram/link/`, for
  the account behind the token; `401` without a token:
  - `POST` issues a code and answers `201` with
    `https://t.me/<bot>?start=<code>` and `expires_at`. With no bot user name
    set it answers `503`, `{"detail": "The Telegram bot is not configured."}`,
    and issues no code
  - `GET` answers `200` with `linked_at`, or `404`,
    `{"detail": "No Telegram link for this account."}`
  - `DELETE` deletes the link and the account's codes and answers `204`.
    Without a link it answers the same `404`, and the codes are deleted all
    the same
  - The three operations are in the API schema with a summary, a success
    example and an example for each error. The webhook stays out of it
- `src/telegram/models.py`: `issue()` now returns the code and the stored
  row. Looking the row up again by its hash raised a server error when a
  second request from the same account had already replaced the code; a
  regression test reproduces it
- `src/telegram/tests/`: `test_link_views.py` for the three operations, new
  schema tests, and the `bot_username` and `account_token` fixtures
- Each new test seen failing against a deliberate break:
  - Deep link pointing to another bot — the link did not start with the
    bot's address
  - Deep link carrying the hash — the start parameter was not the issued code
  - Expiry a minute after the stored one — the answer's expiry differed from
    the database
  - Bot user name check removed — the request was accepted without a user
    name
  - Code issued before the user name check — a refused request left a code
    in the database
  - Status showing the first link of any account — another account's link
    was shown
  - Status also showing the chat id — the body held more than when the link
    was made
  - Status using the generic not-found message — the link's own message was
    missing
  - Unlinking answering `200` with an empty object — the answer was not an
    empty body
  - Unlinking keeping the link — the account's link stayed in the database
  - Unlinking keeping the codes — the account's link codes stayed in the
    database
  - Codes deleted only when there was a link — an unused code survived
    unlinking an account without a link
  - Unlinking using the generic not-found message — the link's own message
    was missing
  - Unlinking deleting every account's links — another account's link was
    removed
  - Unlinking deleting every account's codes — another account's link code
    was removed
  - Endpoints open to anonymous requests — requests without a token were not
    refused
  - Bot-not-configured answer left out of the schema — the schema listed no
    such response
  - Not-found answer left out of the status in the schema — the schema
    listed no such response
  - Status not-found example changed — the example differed from the real
    body
  - Unlinking not-found example changed — the example differed from the
    real body
  - Bot-not-configured example changed — the example differed from the real
    body
  - New code looked up again by its hash — a code replaced by a concurrent
    request raised a server error
  - Link request example without the expiry — the example lacked a returned
    field
  - Link status example without the link time — the example lacked a
    returned field
  - Issuing returning an unsaved row — the row returned was not the stored
    one
- `uv run pytest` — 218 passed. Total coverage 98%, the `telegram` app 100%.
  `ruff`, `mypy`, `makemigrations --check`, `spectacular --validate` and
  `pre-commit` pass
- Pull request merged with every CI check passing; Render deployed it
  automatically. `TELEGRAM_BOT_USERNAME` set on Render
- Production, from outside, with `curl`, logged in as a test account:
  - `POST /api/telegram/link/` — `201`, a link to `medication_log_api_bot`
    with its expiry
  - `GET` and `DELETE /api/telegram/link/` — `404`,
    `{"detail": "No Telegram link for this account."}`
  - the three methods without a token — `401`

**Deviations from the task text:** without a link, `DELETE` still deletes the
account's link codes, so a link asked for and not used yet can be cancelled.
The task text named only the unlinking.

**What this locks in for the rest of the slice:** a link code reaches the
account as a deep link, and only its hash is in the database. 7.4 reads
`/start <code>` in the webhook, looks the code up by its hash, and replaces
both the account's link and the chat's link before storing the new one,
since each is unique.
