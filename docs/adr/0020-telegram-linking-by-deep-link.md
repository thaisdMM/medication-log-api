---
status: accepted
date: 2026-11-18
decision-makers: Thaís
---

# Telegram account linking by deep link with a one-time code

## Context and Problem Statement

A bot cannot start a conversation, so the person talks to it first and the
backend stores that conversation's id (ADR 0012). Before the bot replies with
an account's medications, the backend must know which account the
conversation belongs to.

## Considered Options

* Deep link with a code issued by the API
* Pasting an API-issued code into the chat
* The bot issues the code and the account submits it to the API
* Telegram Login, the login widget or a Mini App

## Decision Outcome

Chosen option: "deep link with a code issued by the API", because it is the
most practical for an MVP without giving up security: one click, nothing to
type. Pasting the code takes one more step, and a code short enough to type is
easier to guess. In the reverse flow, a leaked code would link the victim's
chat to the attacker's account, and the database would hold chat ids with no
account. Telegram Login and the login widget need a browser, and a Mini App is
a web interface (non-goals item 1).

The code is valid for 10 minutes and usable once; a new code cancels the
account's unused ones.

## More Information

Research: issue #14, branch `research/telegram-account-linking`.
