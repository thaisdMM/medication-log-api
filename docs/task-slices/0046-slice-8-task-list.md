# Slice 8 — the task list

The tasks of slice 8, in order, with what each delivers and what breaks if
it goes wrong. Not a step-by-step — each task's step-by-step lives in its
own completion record.

## What the slice delivers

From `0001`: a web page where an account signs up, logs in, manages its own
medications, links Telegram and manages the account, against the API already
live. The slice ends only when this runs in production.

## Numbering rule

Same as `0002`: tasks are never inserted mid-list or renumbered. A new task
enters inside an existing one, or appended at the end (8.9 onward).

## The list

| # | Task | Delivers | Breaks if wrong |
|---|---|---|---|
| 8.1 | Decisions recorded | ADR for the web interface in React with TypeScript; ADR for hosting it on Cloudflare Workers; ADR for keeping the token in `sessionStorage`; non-goals item 1 revoked; ADR 0014 amended; the README no longer says there is no user interface; the map issue | the code of 8.2 to 8.8 rests on decisions written nowhere, and the repository still says it has no screens |
| 8.2 | Test page on Cloudflare | `frontend/` with Vite, React, TypeScript and Tailwind CSS; one page with styled text and an image; ESLint, type checking and Vitest; a frontend job in CI; the Workers configuration in single-page-application mode; the production address and a pull request's preview address both serving the page. Branch and pull request | styles that fail to load are found only after every screen is built. If Tailwind fails here, Mantine replaces it; if Workers fails, Cloudflare Pages does |
| 8.3 | CORS on the API | `django-cors-headers`; the allowed origins come from an environment variable: the interface's address and a pattern that matches only this account's preview addresses; tests that an allowed origin gets the CORS headers and another does not. Branch and pull request | a loose pattern lets any site call the API from a browser; a tight one stops the preview addresses from working |
| 8.4 | Signing in | the API client, with the API address from `VITE_API_URL`; a waiting screen that calls `/healthz/` while the API wakes up; sign-up, login and logout; the token in `sessionStorage`; every text in a translation file, English only; API errors shown as they arrive. Branch and pull request | a token kept in the wrong place outlives the visit; without the waiting screen, the first login looks frozen |
| 8.5 | Medications | list, create, edit and delete, showing the API's messages (duplicate, required fields); a confirmation before deleting. Branch and pull request | a swallowed duplicate error makes the person believe the record was saved |
| 8.6 | My account | the Telegram link (a button and a QR code), the link's status and date, unlinking; logout from every device; account deletion with a confirmation. Branch and pull request | an account deleted by one click; a QR code shown for a link that has expired |
| 8.7 | End-to-end tests | Playwright tests in Python with pytest (`pytest-playwright`): sign up, log in, add a medication, see it in the list; CI starts the API with PostgreSQL and serves the built interface. Time-boxed: the first task cut if time runs short; nothing else depends on it. Branch and pull request | a flaky test in CI blocks every pull request after it |
| 8.8 | Slice proven in production | the whole flow against the public addresses; the README gets the interface's address and a screenshot; the slice closes in its record | without it, "the interface is live" is opinion |

## Decisions

* The interface runs against the public environment, which holds fictitious
  data only (non-goals item 19).
* Screens: sign-up, login, the medication list, the medication form and
  "my account". Every endpoint an account uses on itself has a place on them.
* While the API wakes up from free-tier hibernation (ADR 0001), a waiting
  screen calls `/healthz/` until it answers.
* Each visitor creates their own account; there is no shared demo account.
* The interface is in English, with every text in a translation file.
* Styling: Tailwind CSS, proven on the test page of 8.2; Mantine if it fails.
* Component tests with Vitest and Testing Library, written test-first;
  end-to-end tests with Playwright in Python and pytest.
* Telegram linking on screen: a button that opens the deep link, and a QR
  code of the same link.
* Pull request preview addresses call the production API too, through a CORS
  pattern that matches only this account's addresses.
* The API address reaches the interface as a build variable (`VITE_API_URL`).
* The frontend CI job runs on every pull request.

## Carried, not part of this slice

* The interface in Portuguese, with the API answering in the language the
  interface asks for (`Accept-Language`).
* An HttpOnly cookie instead of the token in the browser: it would change the
  API's authentication (ADR 0007).
