---
status: accepted
date: 2026-11-23
decision-makers: Thaís
---

# The web interface is hosted on Cloudflare Workers

## Context and Problem Statement

Once built, the web interface (ADR 0022) is a set of static files and needs a
free host. The API stays on Render and the database on Neon (ADR 0001).

## Considered Options

* Render static site
* Cloudflare Pages
* Cloudflare Workers (static assets)

## Decision Outcome

Chosen option: "Cloudflare Workers (static assets)", because a static site on
Render draws on the same monthly outbound bandwidth and build minutes as the
API, and when the bandwidth runs out on an account with no payment method,
Render suspends every free service for the rest of the month, the API
included. Cloudflare builds a preview address for each branch and posts it on
the pull request. Of its two products, Cloudflare points new projects to
Workers, whose configuration lives in the repository. Cloudflare Pages is the
fallback if Workers fails in practice.

### Consequences

* Good, because requests to the static files are free and unlimited, and the
  free plan includes 3,000 build minutes a month.
* Bad, because it adds a second platform, with its own account and dashboard.
