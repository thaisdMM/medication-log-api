---
status: accepted
date: 2026-11-24
decision-makers: Thaís
---

# The frontend's Python version follows the Cloudflare build image

## Context and Problem Statement

The web interface is built by Workers Builds (ADR 0023), from the `frontend/`
folder. The build image detects a `.python-version` file and installs that
Python version. With no such file in `frontend/`, it read the repository's
root one, which belongs to the API, and installed that version on every
build. The frontend runs no Python.

## Considered Options

* The root file only, the API's version
* The `PYTHON_VERSION` build variable
* A `.python-version` in `frontend/` naming the version the build image ships
* Deploying from GitHub Actions with wrangler

## Decision Outcome

Chosen option: "a `.python-version` in `frontend/` naming the version the
build image ships", because the build then finds that version already
installed and skips the download. The frontend's file differs from the root
one on purpose; matching them brings the download back. With the root file
only, every build spent minutes installing Python. The `PYTHON_VERSION`
variable did not reach the build: its log listed no build variables.
Deploying from GitHub Actions needs a Cloudflare API token and the account ID
as repository secrets, and the preview address would no longer come from
Workers Builds (ADR 0023).

### Consequences

* Good, because builds no longer install Python, so each deploy finishes
  sooner and spends less of the free plan's build minutes (ADR 0023).
* Bad, because when Cloudflare changes the image's default Python version, the
  download returns until the frontend's file names the new version.
