---
status: accepted
date: 2026-08-26
decision-makers: Thaís
---

# Hosting on Render with Neon

## Context and Problem Statement

The API needs a production home. Render hosts the web service; its own free
PostgreSQL database expires after 30 days (14-day grace period, no backups,
one free database per account). A €5–10/month budget is authorized, but only
as an escape valve if hibernation becomes a real problem at publish time.

## Decision Drivers

* Zero cost during development
* Two-month project timeline; the resume link must outlive it
* The duplicate constraint requires PostgreSQL 15+ (`NULLS NOT DISTINCT`)
* Keep the web service on Render (existing account)

## Considered Options

* Render (web) + Render (database)
* Render (web) + Neon (database)

## Decision Outcome

Chosen option: "Render (web) + Neon (database)", because Neon's free tier is
permanent, needs no card, and runs PostgreSQL 17 — meeting the version
requirement outright. Render's own documentation is treated as authoritative
over a conflicting third-party source on the free database's grace period.

The €5–10 valve buys exactly one improvement: the free web service hibernates
after 15 minutes idle (~1 minute cold start). Spending it on the database only
fixes expiration, which Neon already solves for free. Spending it on the web
service removes the cold start. The valve is reserved for the web service.

### Consequences

* Good: the database address comes from an environment variable (12-factor);
  switching providers later is a config change, not a code change.
* Bad: the free web service still hibernates — affects only the public link,
  not local development against a containerized database.

## More Information

Reopen when the resume link starts reaching recruiters and the cold start
becomes a real problem: upgrade the web service tier, leave the database as is.

Archive address: ETAPA2 A2.
