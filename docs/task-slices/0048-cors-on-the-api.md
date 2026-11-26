# Slice 8, task 8.3 — done

# CORS on the API

- `django-cors-headers` 4.9.0: the latest release declares Django up to
  6.0; its upstream change adding Django 6.1 support touches no code
- `settings.py`: `CorsMiddleware` first in `MIDDLEWARE`; the interface's
  address from `CORS_ALLOWED_ORIGINS`; a fixed pattern that matches only
  this account's preview addresses on Cloudflare Workers; CORS on `/api/`
  and `/healthz/` only
- The pattern is fixed in the settings, not read from the environment, so
  the tests check the pattern production uses. The task list says so
- `.env.example`: `CORS_ALLOWED_ORIGINS`, with its format
- `src/tests/test_cors.py`, new: both preview address formats are allowed;
  another site, plain HTTP, a longer domain, another account and a dotted
  prefix are refused; the preflight before an API call allows the
  interface; the admin site gets no CORS header. Each seen failing against
  a deliberate break:
  - Preview pattern removed — both preview addresses and the preflight
    stopped being allowed
  - Loose pattern (`http` or `https`, any prefix) — plain HTTP, the longer
    domain, another account and the dotted prefix were allowed
  - Every origin allowed — another site was allowed, and the preview
    addresses got `*` instead of their own origin
  - CORS on every path — the admin site got the CORS header
- Pull request merged with every CI check passing; Render deployed it with
  `CORS_ALLOWED_ORIGINS` set to the interface's production address
- Production, `/healthz/` with an `Origin` header:
  - the interface's address — `200`, its origin allowed back
  - a preview address — `200`, its origin allowed back
  - `https://example.com` — `200`, no CORS header
- Production, a preflight to `/api/users/me/` from the interface's address
  asking for `authorization` — `200`, the origin allowed and
  `authorization` among the allowed headers

**What this locks in for the rest of the slice:** the interface, on its
production address and on every preview address, can call the API. When
the interface runs on a development machine against a local API, that
local address goes in `CORS_ALLOWED_ORIGINS` of `.env`; `.env.example`
gets it together with `VITE_API_URL` in 8.4.
