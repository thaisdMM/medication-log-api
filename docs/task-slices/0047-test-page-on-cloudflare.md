# Slice 8, task 8.2 — done

# Test page on Cloudflare

- `frontend/`, new: Vite, React, TypeScript, Tailwind CSS and Biome; Node
  from `.nvmrc`, read by CI and by Workers Builds
- `src/App.tsx`: one page with a heading, a paragraph and an image, styled
  with Tailwind classes; `src/main.tsx` renders it into the `root` element
- `src/App.test.tsx`, new: the page shows its title as a heading and the
  medication image with its description. Each seen failing against a
  deliberate break:
  - Title written as a paragraph — the heading test failed
  - Image with an empty description — the image test failed
- `wrangler.jsonc`: an assets-only Worker serving `dist/` in
  single-page-application mode, preview addresses on, and the `previews`
  block that `wrangler preview` requires
- `frontend/.python-version`: the Python the Cloudflare build image ships,
  so the build skips installing the root file's version (ADR 0025)
- `.github/workflows/ci.yml`: a `frontend` job with lint, formatting, type
  checking, tests and the build
- `.dockerignore` leaves `frontend/` out of the API image;
  `.gitattributes` collapses `package-lock.json` in pull requests
- Biome in place of ESLint: typescript-eslint supports TypeScript up to
  6.0, and the project uses TypeScript 7. The task list and
  `conventions.md` say so
- Pull request merged with every CI check passing; Workers Builds deployed
  it automatically
- The preview address of the branch `feat/frontend-test-page` was
  `feat-frontend-test-page-medication-log-web.thaisdmm.workers.dev`: the
  slash became a hyphen. Each build also gets its own
  `<id>-medication-log-web.thaisdmm.workers.dev` address
- The preview address in a browser, at `/` and at `/medications`: the same
  page, with its styles
- Production, `https://medication-log-web.thaisdmm.workers.dev`:
  - `/` — `200`, the page
  - `/medications` opened as a browser does — `200`, the same page
  - the stylesheet — `200`, `text/css`

**Found on Cloudflare:** the preview build failed until `wrangler.jsonc`
had a `previews` block, and a preview has no address until **Preview** is
on under the Worker's URL in the dashboard. The `PYTHON_VERSION` build
variable never appeared in the build's settings.

**What this locks in for the rest of the slice:** Tailwind CSS and Workers
both work, so neither Mantine nor Cloudflare Pages is needed. The preview
address format sets the CORS pattern of 8.3.
