---
status: accepted
date: 2026-11-18
decision-makers: Thaís
---

# The bot replies inside the webhook response

## Context and Problem Statement

The bot answers the commands that arrive through the webhook (ADR 0012). A
reply can travel inside the webhook response itself, or in a separate call to
the Telegram Bot API.

## Considered Options

* Reply inside the webhook response
* A separate `sendMessage` call through `httpx`
* The `python-telegram-bot` library

## Decision Outcome

Chosen option: "reply inside the webhook response", because it is the simplest
for an MVP with few commands.

### Consequences

* Good, because it adds no new dependency and no outgoing HTTP call from the
  server, as the other two options would.
* Bad, because Telegram does not report whether the message was delivered;
  seeing the delivery needs the separate call.

## More Information

Telegram Bot API, "Making requests when getting updates":
https://core.telegram.org/bots/api#making-requests-when-getting-updates
