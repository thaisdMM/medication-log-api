# Open Questions

## Hosting: pending verifications for task 0.11

Source: `DECISAO_HOSPEDAGEM.md`, partly closed by ADR 0001. From ETAPA2 A9.

- [x] Whether Render deploys from the project's `Dockerfile`. Closed by
  task 0.11, step 6: Language set to Docker, built from the repository's
  `Dockerfile`. See `docs/task-slices/0016`.
- [x] How the Neon database URL is set as an environment variable in
  Render's dashboard. Closed by task 0.11, step 6: pasted as
  `DATABASE_URL` under Advanced → Environment Variables. See
  `docs/task-slices/0016`.
- [x] Confirm in Neon's dashboard (not documentation) that the created
  project runs PostgreSQL 15+. Closed by task 0.11, step 4:
  `SELECT version();` in the SQL Editor returned `PostgreSQL 18.6`. See
  `docs/task-slices/0016`.
- [x] How production redeploys automatically on every merge to main,
  and whether Render's free plan supports it (added 2026-08-27). Closed
  by task 0.11, step 11 and the order proof in step 14: Auto-Deploy set
  to "After CI Checks Pass", confirmed on the free plan — no separate
  task 0.12 needed. See `docs/task-slices/0016`.
