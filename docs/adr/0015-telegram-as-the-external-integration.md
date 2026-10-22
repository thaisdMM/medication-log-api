---
status: accepted
date: 2026-08-23
decision-makers: Thaís
---

# Telegram as the single external integration

## Context and Problem Statement

The project integrates with exactly one external API, no more, because its time
is limited; a delivery channel counts as an integration (non-goals item 4). It
is a personal project with fake data, so it has no reason to pay for a service
or to take on a heavier integration.

## Considered Options

* **Email.** Some sending providers are paid.
* **WhatsApp.** An integration with more requirements than Telegram's; its cost
  was not verified.
* **Telegram.** A bot is created by talking to BotFather (`/newbot`), which
  returns a token — no business account, no third-party approval, no wait, no
  cost.

## Decision Outcome

Chosen option: **Telegram**, the simplest integration, at no cost. It is used
in query mode: an account sends a command to the bot and receives its own list.
How the bot receives messages is ADR 0012.

### Consequences

* Email stays out of the integration slot: it goes to the console in every
  environment (ADR 0013).

## More Information

Archive address: ESTADO_CORRENTE §7.1, §7.3; ETAPA2 A5. The reasons for
rejecting email and WhatsApp were given by Thaís on 2026-10-22; they are not in
the archive.
