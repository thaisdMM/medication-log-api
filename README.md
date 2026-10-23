# Medication Log API

[![CI](https://github.com/thaisdMM/medication-log-api/actions/workflows/ci.yml/badge.svg)](https://github.com/thaisdMM/medication-log-api/actions/workflows/ci.yml)
![Python 3.14](https://img.shields.io/badge/python-3.14-blue)
![Django 6.1](https://img.shields.io/badge/django-6.1-darkgreen)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

A REST API for keeping a personal log of medications. Each account manages
only its own records, and any record that belongs to someone else answers
`404`, as if it did not exist.

There is no user interface by design. This is a backend project, built to be
explored through HTTP requests. Health data is a sensitive category, so the
public environment only ever holds fictional data.

**Stack:** Python 3.14 · Django 6.1 · Django REST Framework · PostgreSQL ·
Docker · GitHub Actions · deployed on Render and Neon.

**Live:** https://medication-log-api.onrender.com/healthz/ (free tier, so the
first request after a while can take up to a minute to wake the service)

## Status

Work in progress, built in vertical slices: each one ships to production,
through CI, before the next one starts.

| | |
|---|---|
| **Done** | Tooling and CI, production deploy, custom user model, registration, token login, current user endpoint |
| **Next** | Logout, interactive API documentation, medication records owned per account |
| **Then** | A Telegram bot that answers with the sender's own medication list |

The full plan and the reasons for its order are in the
[roadmap](docs/task-slices/0001-roadmap.md).

## Tech stack

| Area | Tools |
|---|---|
| Language and framework | Python 3.14, Django 6.1, Django REST Framework |
| Authentication | django-rest-knox (tokens stored hashed, fixed expiry), Argon2 password hashing |
| Database | PostgreSQL 18 |
| Server and container | Granian (WSGI), multi-stage non-root Docker image, Docker Compose |
| Quality | pytest, pytest-django, pytest-cov, mypy in strict mode, Ruff, pre-commit, Conventional Commits |
| CI/CD | GitHub Actions (lint, types, tests against PostgreSQL, migration check, image build), branch protection |
| Hosting | Render (application), Neon (PostgreSQL) |
| Packaging | uv |

## Endpoints available today

| Method | Path | Access | What it does |
|---|---|---|---|
| `GET` | `/healthz/` | public | Reports whether the application reaches its database |
| `POST` | `/api/users/` | public | Creates an account from email, name and password |
| `POST` | `/api/auth/login/` | public | Exchanges email and password for a token |
| `GET` | `/api/users/me/` | token | Returns the account behind the token |

```bash
BASE=https://medication-log-api.onrender.com

curl -X POST $BASE/api/users/ -H "Content-Type: application/json" \
  -d '{"email": "ana@example.com", "name": "Ana", "password": "a-long-passphrase"}'

curl -X POST $BASE/api/auth/login/ -H "Content-Type: application/json" \
  -d '{"email": "ana@example.com", "password": "a-long-passphrase"}'

curl $BASE/api/users/me/ -H "Authorization: Token <token from the login>"
```

## Running locally

Requirements: [uv](https://docs.astral.sh/uv/) and Docker.

```bash
git clone https://github.com/thaisdMM/medication-log-api.git
cd medication-log-api
cp .env.example .env          # set DJANGO_DEBUG=True and fill the values
uv sync
docker compose up -d db       # PostgreSQL on port 5434
uv run python src/manage.py migrate
uv run python src/manage.py runserver
```

## Quality checks

The same checks run in CI on every pull request, and a pull request cannot
merge while any of them fails.

```bash
uv run pytest             # tests with coverage report (needs the database)
uv run mypy               # strict type checking
uv run ruff check .       # lint
uv run ruff format --check .
```

## Design and documentation

Every structural choice is written down before it is built, with its
reasons, so the code can be read against the decision behind it.

| Document | Content |
|---|---|
| [API behaviour](docs/api-behaviour.md) | Status codes and response conventions |
| [Decision records (ADRs)](docs/adr/) | Why each structural choice was made |
| [Domain model](docs/domain-model.md) | Entities, ownership and rules |
| [Glossary](GLOSSARY.md) | The domain terms and what each one means |
| [Non-goals](docs/non-goals.md) | What is out of scope on purpose, and why |
| [Task records](docs/task-slices/) | What each task delivered and how it was verified |

## License

[MIT](LICENSE)
