# Medication Log API

A REST API for keeping a personal log of medications and health conditions.
An account can register its own medications and conditions — nothing is
mandatory beyond having an account — and can grant another registered account
read-only access to that data, by invitation. The invited account only ever
reads what was shared; it never edits or deletes another account's records.

There is no user interface by design: this is an API, meant to be explored
through its interactive documentation. Health data is a sensitive category,
so the publicly deployed environment only ever holds fictional data — never
real medical information.

Built with Django and PostgreSQL.

**Status:** work in progress. Setup instructions and a full walkthrough will
be added as the project grows.
