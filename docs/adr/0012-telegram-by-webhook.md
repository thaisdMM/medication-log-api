---
status: accepted
date: 2026-08-23
decision-makers: Thaís
---

# Telegram by webhook, not long polling

## Context and Problem Statement

The project has exactly one external integration, and a delivery channel counts
as one (non-goals item 4). It is Telegram (ADR 0015).

A bot cannot start a conversation: the person talks to it first, and the
backend stores that conversation's id.

A bot receives messages in one of two modes.

## Considered Options

* **Long polling.** Requires a process running all the time — a permanent
  worker, which the free hosting forbids (ADR 0001, non-goals item 17).
* **Webhook.** Telegram calls a public URL of the system.

## Decision Outcome

Chosen option: **webhook**. It becomes an endpoint of the API itself.

### Consequences

* Two questions stay open (`docs/open-questions.md`): how the backend knows
  which account a conversation belongs to, and whether the webhook survives the
  free tier's hibernation.

## More Information

Archive address: ESTADO_CORRENTE §7.1, §7.3, §7.4; ETAPA2 A5.
