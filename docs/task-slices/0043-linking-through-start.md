# Slice 7, task 7.4 — done

# Linking through `/start`

Two pull requests: the shared Telegram test fixtures first, then the start
command.

## The shared fixtures

- `src/telegram/tests/conftest.py`: `secret_header`, `link_code` and
  `account_link`, used by the webhook and link endpoint tests that built the
  same header, code or link by hand
- The tests prove the same behaviour as before; the deliberate breaks of the
  secret check, the link status and the unlinking still make them fail
- Pull request merged with every CI check passing

## The start command

- `src/telegram/models.py`: `TelegramLinkCode.objects.link_chat(code,
  chat_id)`. In one transaction it looks the code up by its hash, only while
  it is valid, locking the row with `select_for_update()`; then it deletes
  the code, deletes the account's and the chat's earlier links, and creates
  the new one. It returns `True` or `False`, so an expired, used or unknown
  code cannot be told apart
- `src/telegram/views.py`:
  - `start_link_code()` reads the update and returns the chat id and the
    code only for `/start <code>` sent in a private chat. Every level is
    checked with `isinstance` first, so an update in a shape Telegram does
    not send is answered `200` with an empty body
  - The webhook answers `200` with `{"method": "sendMessage", "chat_id":
    ..., "text": ...}`: "Your account is linked. Send /list to see your
    medications in use." or "This link is not valid. Ask for a new link and
    open it within 10 minutes.", the minutes taken from
    `LINK_CODE_LIFETIME`. Any other update keeps the empty `200`
- `src/telegram/tests/test_start_command.py`: the reply to a valid code, the
  chat linked to the code's account, the code deleted, one same reply for an
  expired, unknown and used code, nothing linked by an expired code, the
  account's and the chat's earlier links replaced, the link time renewed, a
  group start ignored with its code kept, other messages and malformed
  updates ignored; `expired_link_code` in `conftest.py`
- The malformed-update test failed against the first version of the code
  with no deliberate break, each of its four cases a server error; the
  `isinstance` checks fixed it
- Each new test seen failing against a deliberate break:
  - Linked reply text changed — the reply to a valid code was not the linked
    reply
  - No link created — the chat was not linked to the code's account
  - Code kept after use — the code stayed, and using it again linked the
    chat again
  - Expiry not checked — an expired code got the linked reply and linked the
    chat
  - Expired code with its own reply — the reply differed from the not-valid
    reply
  - Unknown code with its own reply — the reply to an unknown or used code
    differed from the not-valid reply
  - Account's earlier link not deleted — linking the account to a new chat
    raised a server error
  - Chat's earlier link not deleted — linking a chat taken by another
    account raised a server error
  - Same chat and account keeping the earlier link — the link time did not
    move forward
  - Group chats accepted — a group start got a reply and used the code up
  - Any command beginning with start accepted — a longer command got the
    not-valid reply
  - Start without a code looked up — a bare start got the not-valid reply
  - Body not checked to be an object — a JSON list raised a server error
  - Message not checked to be an object — a null message raised a server
    error
  - Chat not checked to be an object — a chat sent as text raised a server
    error
  - Text not checked to be text — a photo message and a null text raised a
    server error
  - Chat id not checked — a private chat without an id raised a server error
  - Every message answered — non-start messages got the not-valid reply and
    valid codes stopped linking
- `uv run pytest` — 239 passed. Total coverage 98%, the `telegram` app 100%.
  `ruff`, `mypy`, `makemigrations --check`, `spectacular --validate` and
  `pre-commit` pass
- Pull request merged with every CI check passing; Render deployed it
  automatically
- Production, through the API documentation page and Telegram, with an
  account created for the check:
  - `POST /api/telegram/link/` — `201`, a link to `medication_log_api_bot`
    expiring 10 minutes later
  - opening the link and pressing Start — the bot replied "Your account is
    linked. Send /list to see your medications in use."
  - `GET /api/telegram/link/` — `200`, `linked_at` at the moment Start was
    pressed, no chat id
  - opening the same link again — the bot replied "This link is not valid.
    Ask for a new link and open it within 10 minutes."
  - `/start` alone and plain text — no reply
  - `DELETE /api/telegram/link/` — `204`

**Not tested:** two starts with the same code at the same moment, which needs
two database connections at once. Two starts with different codes from the
same chat at the same moment can end one in a server error, on the one-chat
rule; Telegram delivers that update again.

**What this locks in for the rest of the slice:** a chat is linked to one
account and the webhook can reply inside its response. 7.5 reads the other
messages: `/list` for the account linked to the chat, `/help`, plain text,
and a chat with no link; the reply to a bare `/start` from a linked chat is
still to be decided.
