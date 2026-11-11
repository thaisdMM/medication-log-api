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

**Interactive documentation:** https://medication-log-api.onrender.com/api/docs/
(how to use it: [below](#-using-the-interactive-documentation))

## Status

Work in progress, built in vertical slices: each one ships to production,
through CI, before the next one starts.

| | |
|---|---|
| **Done** | Tooling and CI, production deploy, custom user model, registration, token login, current user endpoint, logout, interactive API documentation, medication records owned per account, account deletion, a verification walkthrough that ends in another account's `404` |
| **Next** | A Telegram bot that answers with the sender's own medication list |

The full plan and the reasons for its order are in the
[roadmap](docs/task-slices/0001-roadmap.md).

## Tech stack

| Area | Tools |
|---|---|
| Language and framework | Python 3.14, Django 6.1, Django REST Framework |
| API documentation | drf-spectacular (OpenAPI 3), Swagger UI |
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
| `GET` | `/api/docs/` | public | Swagger UI page to read and try the endpoints |
| `GET` | `/api/schema/` | public | The OpenAPI schema behind that page |
| `POST` | `/api/users/` | public | Creates an account from email, name and password |
| `POST` | `/api/auth/login/` | public | Exchanges email and password for a token |
| `GET` | `/api/users/me/` | token | Returns the account behind the token |
| `POST` | `/api/auth/logout/` | token | Deletes the token in use |
| `POST` | `/api/auth/logoutall/` | token | Deletes every token of the account |
| `POST` | `/api/users/me/delete/` | token | Deletes the account and its medications, after the password is confirmed |
| `GET` | `/api/medications/` | token | Lists the account's medications, alphabetically; `?state=in_use` or `?state=suspended` filters |
| `POST` | `/api/medications/` | token | Records a medication: name, concentration value and unit, form, state |
| `GET` | `/api/medications/<id>/` | token | Returns one of the account's medications |
| `PUT`, `PATCH` | `/api/medications/<id>/` | token | Edits it; suspending or resuming is `PATCH {"state": ...}` |
| `DELETE` | `/api/medications/<id>/` | token | Deletes it |

## 💻 Trying it from the terminal

The sequence below runs against the public environment with `curl`, from a
new account to another account's `404`, and deletes everything it created at
the end. Copy the token and the id by hand where a step says so.

```bash
BASE=https://medication-log-api.onrender.com
```

1. **Create an account** — `201`, with the new account's id.

   ```bash
   curl -X POST $BASE/api/users/ -H "Content-Type: application/json" \
     -d '{"email": "ana@example.com", "name": "Ana", "password": "a-long-passphrase"}'
   ```

2. **Log in** — `200`, with an expiry and a token.

   ```bash
   curl -X POST $BASE/api/auth/login/ -H "Content-Type: application/json" \
     -d '{"email": "ana@example.com", "password": "a-long-passphrase"}'
   TOKEN=<token from the response>
   ```

3. **See your account** — `200`, with the id and the name.

   ```bash
   curl $BASE/api/users/me/ -H "Authorization: Token $TOKEN"
   ```

4. **Record a medication** — `201`, with the medication and its id.

   ```bash
   curl -X POST $BASE/api/medications/ -H "Authorization: Token $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name": "Losartan", "concentration_value": "50", "concentration_unit": "mg", "form": "tablet"}'
   MED_ID=<id from the response>
   ```

5. **List your medications** — `200`, in alphabetical order.

   ```bash
   curl $BASE/api/medications/ -H "Authorization: Token $TOKEN"
   ```

6. **Get one medication** — `200`, with that medication.

   ```bash
   curl $BASE/api/medications/$MED_ID/ -H "Authorization: Token $TOKEN"
   ```

7. **Edit it** — `200`, with the new concentration. `PUT` sends every field;
   `PATCH` sends only the fields that change, as in the next step.

   ```bash
   curl -X PUT $BASE/api/medications/$MED_ID/ -H "Authorization: Token $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name": "Losartan", "concentration_value": "100", "concentration_unit": "mg", "form": "tablet"}'
   ```

8. **Suspend it** — `200`, with `"state": "suspended"`.

   ```bash
   curl -X PATCH $BASE/api/medications/$MED_ID/ -H "Authorization: Token $TOKEN" \
     -H "Content-Type: application/json" -d '{"state": "suspended"}'
   ```

9. **Filter by state** — `200`, with only the suspended medications.

   ```bash
   curl "$BASE/api/medications/?state=suspended" -H "Authorization: Token $TOKEN"
   ```

10. **Record the same medication again** — `400`, "You already have this
    medication with the same concentration and form.": an account holds each
    medication once.

    ```bash
    curl -X POST $BASE/api/medications/ -H "Authorization: Token $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"name": "Losartan", "concentration_value": "100", "concentration_unit": "mg", "form": "tablet"}'
    ```

11. **Create a second account and log in** — `201`, then `200` with its token.

    ```bash
    curl -X POST $BASE/api/users/ -H "Content-Type: application/json" \
      -d '{"email": "bruno@example.com", "name": "Bruno", "password": "a-long-passphrase"}'
    curl -X POST $BASE/api/auth/login/ -H "Content-Type: application/json" \
      -d '{"email": "bruno@example.com", "password": "a-long-passphrase"}'
    TOKEN_B=<token from the response>
    ```

12. **Ask for the first account's medication** — `404`, the same answer as an
    id that does not exist, so the second account cannot tell that the
    medication exists.

    ```bash
    curl $BASE/api/medications/$MED_ID/ -H "Authorization: Token $TOKEN_B"
    ```

13. **Delete the medication** — `204`, which prints nothing: `204` has no
    body. The first account deletes its own medication.

    ```bash
    curl -X DELETE $BASE/api/medications/$MED_ID/ -H "Authorization: Token $TOKEN"
    ```

14. **Log out** — `204`, which prints nothing: `204` has no body. The second
    account's token stops working.

    ```bash
    curl -X POST $BASE/api/auth/logout/ -H "Authorization: Token $TOKEN_B"
    ```

15. **Delete both accounts** — `204` each, which prints nothing: `204` has no
    body. The second account logs in again first, because its token was
    deleted in step 14. Each account's medications go with it.

    ```bash
    curl -X POST $BASE/api/users/me/delete/ -H "Authorization: Token $TOKEN" \
      -H "Content-Type: application/json" -d '{"password": "a-long-passphrase"}'
    curl -X POST $BASE/api/auth/login/ -H "Content-Type: application/json" \
      -d '{"email": "bruno@example.com", "password": "a-long-passphrase"}'
    TOKEN_B=<token from the response>
    curl -X POST $BASE/api/users/me/delete/ -H "Authorization: Token $TOKEN_B" \
      -H "Content-Type: application/json" -d '{"password": "a-long-passphrase"}'
    ```

## 📖 Using the interactive documentation

The [Swagger UI page](https://medication-log-api.onrender.com/api/docs/)
lists every endpoint with its fields, the values each closed list accepts and
the responses it can give. It also sends real requests: open an endpoint,
choose **Try it out**, fill in the fields and choose **Execute**.

After logging in, choose **Authorize** at the top of the page and type
`Token`, a space, and the token. The page does not add the word `Token` by
itself. The endpoints marked with a lock then send that token. To act as the
other account, choose **Authorize** again, log out of the page's
authorization and type the other token.

The same sequence as the terminal:

1. **Create an account** — **POST /api/users/**
2. **Log in** — **POST /api/auth/login/**, then **Authorize** with the token
3. **See your account** — **GET /api/users/me/**
4. **Record a medication** — **POST /api/medications/**
5. **List your medications** — **GET /api/medications/**
6. **Get one medication** — **GET /api/medications/{id}/**
7. **Edit it** — **PUT /api/medications/{id}/**
8. **Suspend it** — **PATCH /api/medications/{id}/**
9. **Filter by state** — **GET /api/medications/**, with `state` set to `suspended`
10. **Record the same medication again** — **POST /api/medications/**
11. **Create a second account and log in** — **POST /api/users/** and
    **POST /api/auth/login/**, then **Authorize** with the new token
12. **Ask for the first account's medication** — **GET /api/medications/{id}/**
13. **Delete the medication** — **DELETE /api/medications/{id}/**, with the
    first account's token
14. **Log out** — **POST /api/auth/logout/**
15. **Delete both accounts** — **POST /api/users/me/delete/**, once with each
    account's token

The public environment only holds fictional data, so use a made-up email.

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
| [Conventions](docs/conventions.md) | How code, tests, commits and pull requests are written |
| [Decision records (ADRs)](docs/adr/) | Why each structural choice was made |
| [Domain model](docs/domain-model.md) | Entities, ownership and rules |
| [Glossary](GLOSSARY.md) | The domain terms and what each one means |
| [Non-goals](docs/non-goals.md) | What is out of scope on purpose, and why |
| [Task records](docs/task-slices/) | What each task delivered and how it was verified |

## License

[MIT](LICENSE)
