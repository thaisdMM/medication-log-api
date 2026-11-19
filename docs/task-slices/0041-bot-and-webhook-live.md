# Slice 7, task 7.2 — done

# Bot and webhook live

- `src/telegram/`: a new app for the bot's code
- `src/telegram/permissions.py`: `HasTelegramWebhookSecret` lets a request in
  only when the `X-Telegram-Bot-Api-Secret-Token` header carries the secret
  in `TELEGRAM_WEBHOOK_SECRET`, compared with `secrets.compare_digest` on
  bytes; with no secret configured, every request is refused
- `src/telegram/views.py`: `POST /api/telegram/webhook/` answers `200` with an
  empty body; no authentication classes; left out of the API schema
- `src/config/settings.py`: the app installed; `TELEGRAM_WEBHOOK_SECRET` read
  from the environment, empty by default
- `src/telegram/tests/`: the secret accepted; a wrong, missing or non-ASCII
  secret refused with `403` and the permission message; every request
  refused with no secret configured; the webhook absent from the schema
- Each new test seen failing against a deliberate break:
  - Permission letting every request in — the wrong, missing and non-ASCII
    secrets and the unconfigured secret were accepted
  - Permission refusing every request — the update carrying the secret was
    refused
  - Check for a configured secret removed — an empty secret was accepted when
    none is configured
  - Secrets compared as text instead of bytes — the non-ASCII secret raised a
    server error instead of a refusal
  - Webhook put back in the schema — the schema listed the webhook
- `uv run pytest` — 180 passed. Total coverage 98%. `ruff`, `mypy`,
  `manage.py check` and `pre-commit` pass
- Pull request merged with every CI check passing; Render deployed it
  automatically
- The bot created with BotFather. `TELEGRAM_WEBHOOK_SECRET` set on Render.
  The webhook registered with `setWebhook`, with the secret and
  `allowed_updates` set to `message`; `getWebhookInfo` shows the URL, no
  pending update and no error
- Production, from outside, with `curl`:
  - `POST /api/telegram/webhook/` with the secret — `200`
  - without the secret, or with a wrong one — `403`,
    `{"detail": "You do not have permission to perform this action."}`
  - `GET /api/schema/` — the webhook is not listed
- A message sent to the bot reached the webhook and was answered `200`
- Hibernation test, with Granian's access log turned on through environment
  variables only for the test, in a format without the client address:
  - Render's health checks on `/healthz/` did not keep the service awake: it
    shut down 15 minutes after the last real request
  - A message sent to the sleeping bot woke the service. `getWebhookInfo`
    showed one pending update right after, then none, with no error. The log
    shows `POST /api/telegram/webhook/` answered `200` after the cold start
  - No update was lost, so no keep-awake ping was added
  - The two log variables removed from Render afterwards; the secret stays

**Deviations from the task text:** none.

**What this locks in for the rest of the slice:** Telegram reaches the API
only with the secret, through a webhook that survives the free tier's
hibernation. 7.3 adds the link model and endpoints to the `telegram` app;
7.4 turns the webhook's empty `200` into the bot's reply.
