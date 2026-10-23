# Telegram webhook versus free-tier hibernation

Research for issue #13 (open question "Slice 7" in `docs/open-questions.md`).
Primary sources only, read on 2026-10-23. Facts, no decision.

## Question

Does a Telegram webhook still work when the Render free web service has spun
down (15 minutes idle, about a minute to wake — ADR "Hosting on Render with
Neon")?

## Short answer

Probably yes for delivery, but not provably from the docs. Telegram retries a
failed webhook delivery and keeps undelivered updates for up to 24 hours, so
an update that arrives during a cold start should be redelivered once the
service is up. What the docs do not say: Telegram's response timeout, how many
retries it makes and how far apart, and what Render returns to a non-browser
client during spin-up. The reply to the user will be about a minute late
either way.

## Telegram (core.telegram.org)

| Fact | Source |
|---|---|
| Delivery is an HTTPS POST of a JSON `Update` to the webhook URL. | [setWebhook](https://core.telegram.org/bots/api#setwebhook) |
| "In case of an unsuccessful request (a request with response HTTP status code different from 2XY), we will repeat the request and give up after a reasonable amount of attempts." | [setWebhook](https://core.telegram.org/bots/api#setwebhook) |
| "Incoming updates are stored on the server until the bot receives them either way, but they will not be kept longer than 24 hours." | [Getting updates](https://core.telegram.org/bots/api#getting-updates) |
| `getWebhookInfo` reports `pending_update_count` ("Number of updates awaiting delivery"), `last_error_date` and `last_error_message`. Useful to observe what happens on a cold start. | [WebhookInfo](https://core.telegram.org/bots/api#webhookinfo) |
| `setWebhook` / `deleteWebhook` accept `drop_pending_updates` ("Pass True to drop all pending updates"). | [setWebhook](https://core.telegram.org/bots/api#setwebhook) |
| Webhook and `getUpdates` are mutually exclusive: "You will not be able to receive updates using getUpdates for as long as an outgoing webhook is set up." | [setWebhook](https://core.telegram.org/bots/api#setwebhook), [FAQ](https://core.telegram.org/bots/faq) |
| Ports 443, 80, 88, 8443 only; TLS 1.2+; "Redirects are not supported." | [Webhooks guide](https://core.telegram.org/bots/webhooks), [FAQ](https://core.telegram.org/bots/faq) |
| A `secret_token` set on `setWebhook` is sent back in the `X-Telegram-Bot-Api-Secret-Token` header. | [setWebhook](https://core.telegram.org/bots/api#setwebhook) |

**Unverified** (no Telegram page states it — searched the Bot API page, the
webhooks guide and the FAQ):

* How long Telegram waits for the webhook to answer (the timeout).
* Whether a timeout or connection error counts as "unsuccessful" the same way
  a non-2XY status does. The docs only define failure by status code.
* How many attempts "a reasonable amount" is, and the interval between them.
* Whether updates stay ordered across retries.

## Render (render.com/docs)

| Fact | Source |
|---|---|
| "Render spins down a Free web service that goes 15 minutes without receiving any inbound traffic." | [Free instances](https://render.com/docs/free#spinning-down-on-idle) |
| "A Free web service spins back up whenever it next receives an HTTP request or new WebSocket connection. This process takes about one minute." | [Free instances](https://render.com/docs/free#spinning-down-on-idle) |
| "Render displays a loading page to connecting browsers while a service is spinning up." | [Free instances](https://render.com/docs/free#spinning-down-on-idle) |
| 750 free instance hours per workspace per month; "spun-down services don't consume Free instance hours"; when used up, free web services are suspended until next month. | [Free instances](https://render.com/docs/free#free-instance-hours) |
| Only static sites, web services, Postgres and Key Value support free instances ("Other service types don't support Free instances"). | [Free instances](https://render.com/docs/free#create-a-free-instance) |
| Background workers "don't receive any incoming network traffic". | [Background workers](https://render.com/docs/background-workers) |
| Starter web service: $7/month, 512 MB, 0.5 CPU. Upgrading to a paid compute plan removes the free limitations. | [Pricing](https://render.com/pricing), [Free instances](https://render.com/docs/free#upgrading-to-a-paid-instance) |

**Unverified** (Render docs do not say):

* Whether the request that wakes the service is held and forwarded once the
  app is up, or answered straight away.
* What a non-browser client (Telegram's POST) receives during spin-up — the
  loading page's HTTP status is not documented. If it were a 2XY, Telegram
  would treat the update as delivered and never retry it; that would lose the
  update. This is the main risk and needs a test.
* The exact cold-start time for this app (Docker image, Django start-up);
  "about one minute" is Render's general figure.

## Does a cold start fit?

* Against the timeout: unknown, because Telegram documents no timeout.
  A one-minute wake is unlikely to fit inside a single HTTP request (inference,
  unverified).
* Against the retry window: updates are kept up to 24 hours and failures are
  retried, so a later attempt after the service is up should succeed — as long
  as Render's spin-up response is not a 2XY (unverified, see above).
* How to check it directly: let the service spin down, send the bot a
  message, then call `getWebhookInfo` and watch `pending_update_count` and
  `last_error_message` until the update arrives.

## Options if it does not fit (facts, not a decision)

* **Paid plan valve** — ADR "Hosting on Render with Neon" reserves the
  €5–10/month valve for the web service. A Starter web service is $7/month and
  is not subject to the free spin-down.
* **Long polling (`getUpdates`)** — needs a process running all the time. On
  Render that is a background worker, which has no free instance type; a free
  web service would still spin down because outbound polling is not inbound
  traffic (the spin-down rule counts only inbound traffic). Polling and a
  webhook cannot be used at the same time.
* **Keep the free service awake** — any inbound HTTP request every <15 minutes
  resets the idle timer. One service running all month uses at most 744 hours
  (31 × 24), inside the 750 free hours, if it is the only free service in the
  workspace. Render's docs neither endorse nor forbid an external pinger
  (unverified either way); Render cron jobs are not a free service type.
* **Accept the delay** — rely on Telegram's retries and the 24-hour storage;
  the first message after idle is answered about a minute late.
