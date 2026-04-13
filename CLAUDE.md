# jet-lag-the-app — agent guide

## Commands

Run everything through **mise** tasks from the repo root:

- `mise run :format` — format (dprint)
- `mise run :format --check` — check formatting
- `mise run //backend:deps` — install Python deps (`uv`)
- `mise run //backend:test` — pytest (against real Postgres)
- `mise run //backend:lint` / `//backend:typecheck` — ruff / ty
- `mise run //client:test` — `./gradlew allTests` (requires **JDK 17+** for Android Gradle Plugin)
- `mise run :check` — aggregate quality gate
- `mise run :dev` — start Tilt dev stack (Postgres, Valkey, backend)
- `mise run //backend:codegen` — sqlc code generation (writes `db/generated/`)
- `mise run //backend:db-diff <name>` — Atlas migration planning (schema.sql → migration file)
- `mise run //backend:migrate` — apply pending Atlas migrations

Pre-commit: install hooks with `hk install --mise` (hk steps call `mise run …` only).

## Architecture

Monorepo with `backend/` (FastAPI) and `client/` (Kotlin Multiplatform + Compose). Feature modules in the client must not depend on each other; share code via `core*` modules.

### Database

Uses **Atlas** for schema migrations and **sqlc** (sqlc-gen-python) for typed query generation — not SQLAlchemy ORM or Alembic. Generated code lives in `db/generated/` and must not be hand-edited; run `mise run //backend:codegen` to regenerate.

## Secrets

Use **fnox** only (active for this project) — no `.env` files. See `fnox.toml` stub and `CONTRIBUTING.md`.

## Commits / PRs

Conventional commits. Each pushed commit should be CI-green. Use Graphite `gt` for stacked PRs (see `CONTRIBUTING.md`).
