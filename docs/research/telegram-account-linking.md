# Linking a Telegram conversation to an account

Research for issue #14 (map #10). Facts and trade-offs only; no decision.
Sources were read on 2026-10-23. Anything a source does not state is marked
**unverified**.

## Sources

- [BF] Bot features, Deep Linking — https://core.telegram.org/bots/features#deep-linking
- [API] Bot API — https://core.telegram.org/bots/api
- [LINKS] Deep links — https://core.telegram.org/api/links#bot-links
- [LOGIN] Log In With Telegram (OIDC) — https://core.telegram.org/bots/telegram-login
- [LEGACY] Legacy login widget — https://core.telegram.org/widgets/login-legacy
- [WEBAPPS] Mini Apps — https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
- [HOOKS] Webhook guide — https://core.telegram.org/bots/webhooks
- [FAQ] Bots FAQ — https://core.telegram.org/bots/faq

## What Telegram gives the backend in every message

- Each update carries `message.chat` and `message.from`. `Chat.type` is
  `private`, `group`, `supergroup` or `channel` [API, Chat].
- `Chat.id` and `User.id` have at most 52 significant bits, so a signed 64-bit
  integer is safe for storing them [API, Chat / User]. In Django terms: a
  `BigIntegerField`.
- That the private chat id equals the user id is **unverified** — no page
  read states it.
- No mechanism below needs a phone number. Two mechanisms can ask for one
  (`request_contact` on a keyboard button [API, KeyboardButton]; the `phone`
  scope of Telegram Login [LOGIN]). Both are excluded by non-goals item 15.

## Mechanism A — deep link with a one-time code issued by the API

**Flow.** An authenticated endpoint (knox token) creates a random code and
returns `https://t.me/<bot>?start=<code>`. The account opens the link on its
phone; Telegram sends the bot `/start <code>` [BF]. The webhook looks the code
up and stores `chat.id` on the account that requested it.

**Limits stated by Telegram.**
- Allowed characters: `A-Z`, `a-z`, `0-9`, `_` and `-`; base64url is
  recommended for binary content; up to 64 characters [BF]. [LINKS] repeats
  "up to 64 base64url characters".
- The Start button is shown even if the user has already started the bot
  [LINKS], so an account that already talks to the bot can still link.
- Telegram describes this use itself: "an authentication token to connect the
  user's Telegram account to their account on another platform" [BF].

**What it stores.** The conversation id column on the account (or a link
table), plus a code record: the code (or its hash), the account, the creation
time or expiry, and a used flag or deletion on use. Whether to hash the code
like knox hashes tokens is a design choice, not a source fact.

**Abuse.**
- *Leaked link* — whoever opens it first links **their** chat to **the
  issuing account**, and then reads that account's health data through the
  bot. This is the worst case of all mechanisms here, because the account
  cannot see who used the link. Mitigations (single use, short expiry,
  showing the linked Telegram username back through the API) are design
  choices; no source prescribes an expiry.
- *Reuse* — prevented only if the code is deleted or marked used on first
  `/start`.
- *Guessing* — depends on entropy. 64 base64url characters can hold up to 384
  bits; Python's `secrets.token_urlsafe(32)` gives 43 characters (the
  `secrets` module is not a Telegram source — its fit is **unverified** here
  beyond the charset matching).
- *Group chat* — `startgroup=` sends `/start@bot <code>` from a group [BF];
  checking `chat.type == "private"` rejects it.
- Whether the `/start <code>` text stays visible in the user's chat history
  is **unverified**.

**Fits a UI-less API?** Yes. The API only returns a URL in JSON; the rest
happens in the Telegram app.

## Mechanism B — the account pastes an API-issued code into the chat

**Flow.** Same endpoint issues a short code; the account types, e.g.,
`/link 4F7K2Q` into the bot chat.

**Limits.** No length limit specific to this; an incoming message text is
ordinary text. (The 1-4096 limit in [API] is for messages the bot sends.)

**Stores.** Same as A.

**Abuse.** Same leak and reuse risks as A. A code short enough to type is
easier to guess, so it needs a short expiry and attempt limiting — these are
design choices, not source facts. Typing errors are possible; A has none.

**Fits a UI-less API?** Yes. It also works if the account cannot open links on
the phone. One more step for the account than A.

## Mechanism C — reverse direction: the bot issues a code, the account submits it to the API

**Flow.** The account sends `/start` with no parameter; the bot replies with a
code bound to that `chat.id`; the account POSTs the code to an authenticated
endpoint, which stores the chat id on the requesting account.

**Stores.** A pending record keyed by chat id: code, chat id, expiry. Before
confirmation the system holds a chat id that belongs to no account — personal
data with no owner yet (non-goals item 15 only declares it per account).

**Abuse.** The authority flips. A leaked code lets the attacker link the
**victim's** chat to the **attacker's** account: the victim would then
receive the attacker's data, not the reverse, and the victim's chat id sits
under the attacker's account. Bot replies to anyone who writes, so anyone can
make the system create pending rows.

**Fits a UI-less API?** Yes.

## Mechanism D — Telegram Login (OpenID Connect, current)

**Flow.** Authorization Code flow with PKCE against `oauth.telegram.org`; the
`redirect_uri` must be pre-registered in BotFather; the code is exchanged
server-side with a client secret; the `id_token` (JWT, RS256 by default) is
verified against the JWKS, checking `iss`, `aud` and `exp` [LOGIN]. A `nonce`
can be included against replay [LOGIN].

**What it yields.** `openid` gives `sub`, `iss`, `iat`, `exp`; the `profile`
scope adds `id`, name, username, picture; `phone` adds a phone number;
`telegram:bot_access` "allows your bot to send direct messages to the user
after login" [LOGIN]. How `sub` relates to the Telegram user id is not stated
— **unverified**. With `telegram:bot_access` the bot could write first, which
is in tension with the statement "a bot cannot start a conversation" in
`docs/domain-model.md`.

**Stores.** The Telegram user id, plus short-lived `state`, PKCE verifier and
`nonce` for the flow; a client secret in configuration.

**Abuse.** Handled by the protocol (state, PKCE, nonce, signature). The
`phone` scope must never be requested.

**Fits a UI-less API?** Poorly. The authorization URL "must be opened in the
user's browser" [LOGIN], and the browser does not carry the knox token, so
binding the result to the logged-in account needs extra state carried
through `state` (**unverified** as a pattern; not described by Telegram).
It also behaves like "sign in with a provider", which non-goals item 4 rules
out for Google/GitHub.

## Mechanism E — legacy login widget, and `login_url` buttons

**Legacy widget** [LEGACY]: a website embeds a widget; Telegram returns `id`,
names, `username`, `photo_url`, `auth_date`, `hash`. The backend checks
`hash` = HMAC-SHA-256 of the sorted data-check-string with `SHA256(bot_token)`
as key, and may check `auth_date` against outdated data. The domain is linked
with `/setdomain`. Needs a web page: does not fit a UI-less API.

**`login_url` inline button** [API, LoginUrl]: the bot sends a button; tapping
it opens an HTTPS URL on the bot's linked domain "with user authorization
data added to the query string", same data and same hash check as the widget.
It proves the Telegram identity, but the URL opens in a browser that has no
knox token, so it does not by itself say which account — linking would still
need a code (as in A) or a login page. Not supported for ephemeral messages.

## Mechanism F — Mini App `initData`

A web page opened inside Telegram receives `initData`; the backend validates
`hash` with `HMAC_SHA256(bot_token, "WebAppData")` as key and may check
`auth_date` [WEBAPPS]. A third-party Ed25519 `signature` check also exists.
A Mini App is a web UI, which non-goals item 1 excludes.

## Comparison

| | Stores beyond the chat id | Worst abuse | Fits UI-less API |
|---|---|---|---|
| A deep link | code, account, expiry, used | leaked link → stranger reads the account | yes |
| B pasted code | same as A | same as A; shorter code is easier to guess | yes |
| C reverse code | pending row per chat | victim's chat linked to attacker's account | yes |
| D OIDC login | Telegram id, flow state, client secret | protocol-protected | poorly — needs a browser |
| E widget / `login_url` | Telegram id | replay if `auth_date` unchecked | no / only with a code |
| F Mini App | Telegram id | replay if `auth_date` unchecked | no — it is a UI |

## Webhook: confirming a request comes from Telegram

- `setWebhook` takes `secret_token`, 1-256 characters of `A-Z`, `a-z`, `0-9`,
  `_`, `-`; every webhook request then carries the header
  `X-Telegram-Bot-Api-Secret-Token` with it, "useful to ensure that the
  request comes from a webhook set by you" [API, setWebhook].
- The older FAQ recommends a secret path in the URL, e.g.
  `www.example.com/your_token` [FAQ]. Logging of URLs makes a path secret
  easier to leak than a header — **unverified** for this host.
- Webhook requests come from `149.154.160.0/20` and `91.108.4.0/22`, and the
  range "might change in the future" [HOOKS]. Filtering by IP behind the
  hosting's proxy is **unverified** for Render.
- Ports 443, 80, 88, 8443 only [API, setWebhook].
- A non-2XX response is retried, and Telegram will "give up after a
  reasonable amount of attempts"; the count is not stated. `update_id` lets the bot ignore repeated updates; unread
  updates are kept up to 24 hours [API, Getting updates].
- Comparing the header in constant time is general practice, not a Telegram
  statement.
