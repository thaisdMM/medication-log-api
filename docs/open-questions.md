# Open Questions

## Hosting: pending verifications for task 0.11

Source: `DECISAO_HOSPEDAGEM.md`, partly closed by ADR 0001. From ETAPA2 A9.

- [ ] Whether Render deploys from the project's `Dockerfile`.
- [ ] How the Neon database URL is set as an environment variable in Render's dashboard.
- [ ] Confirm in Neon's dashboard (not documentation) that the created project runs PostgreSQL 15+.
- [ ] How production redeploys automatically on every merge to main, and whether Render's free plan supports it (added 2026-08-27) — if not, this becomes task 0.12.
