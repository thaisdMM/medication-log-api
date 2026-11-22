# Slice 7, task 7.6 — done

# Slice 7 proven in production

- No code changed
- Production, on the Swagger UI page and in Telegram, on two new accounts, A
  and B. Ids, tokens, link codes and the chat id are left out:
  - A records four medications — `201` each
  - A asks for a link — `201`; opening it and choosing Start —
    "Your account is linked. Send /list to see your medications in use."
  - `/list` from A's chat:

    ```
    Your medications in use:
    - Ácido fólico · 5 mg · tablet
    - Vitamina D · 10 other unit · drop
    - Xarope A · 0.5 g · ml
    - Zinco · 1000 mg
    ```

    The accented name sorts before `Z`, the unit `other` reads
    `other unit`, `0.500` loses its trailing zeros and `1000` is never
    written as `1E+3`
  - `/help` — the help text
  - B records Losartana, asks for a link and opens it in the same chat — the
    linked reply; `/list` — only `- Losartana · 50 mg · tablet`, none of A's
    medications
  - `GET /api/telegram/link/` as B — `200` with `linked_at`; as A — `404`:
    one chat holds one account, and A's link was replaced
  - B unlinks — `204`; `GET /api/telegram/link/` — `404`; `/list` —
    "This chat is not linked to an account." with how to link it
  - A's link, already used — "This link is not valid. Ask for a new link and
    open it within 10 minutes."
  - A link opened more than 10 minutes after it was issued — the same
    "not valid" reply, and the chat stayed unlinked
  - A group with the bot: `/list` and `/help` got no reply
  - Clean-up: both accounts deleted with their passwords. Before deleting B,
    a new link linked the chat and `/list` showed only Losartana; after the
    deletion, `/list` got "This chat is not linked to an account." and the
    used link got the "not valid" reply
- The production database, read in the Neon SQL editor with `SELECT`, never
  on the hash columns:
  - A's four medications and B's one, `0.500` stored with its zeros
  - No row in the link table nor in the link code table
  - Two tokens for B, from logins with no logout, none for A
  - Two expired tokens of older accounts still in the token table, as the
    "Expired tokens" follow-up already describes
- README: the Telegram integration at the top, the link and webhook
  endpoints, steps 11 to 13 of the Swagger walkthrough, a "Telegram bot"
  section with a screenshot of the conversation

**Found on the Swagger UI page:** logging in as B while "Authorize" still
held A's token kept every request acting as A. The API answers the token it
receives; logging in does not change the token the page sends, and A's token
stays valid until logout or expiry. The README now says so, and a shorter
token lifetime is a follow-up on the first release map.

**What this locks in for the rest of the project:** an account links its
Telegram chat through the public address, the bot answers `/list` with that
account's medications in use only, and unlinking stops it. Slice 7 is
closed, and with it the first release.
