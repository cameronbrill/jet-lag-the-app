# jet-lag-the-app — agent guide

## Commands

Run everything through **mise** tasks from the repo root:

- `mise run :fmt` — format (dprint)
- `mise run :format-ci` — check formatting
- `mise run :backend:deps` — install Python deps (`uv`)
- `mise run :backend:test` — pytest
- `mise run :backend:lint` / `:backend:typecheck` — ruff / ty
- `mise run :client:test` — `./gradlew allTests` (requires **JDK 17+** for Android Gradle Plugin)
- `mise run :check` — aggregate quality gate

Pre-commit: install hooks with `hk install --mise` (hk steps call `mise run …` only).

## Architecture

Monorepo with `backend/` (FastAPI) and `client/` (Kotlin Multiplatform + Compose). Feature modules in the client must not depend on each other; share code via `core*` modules.

## Secrets

Use **fnox** only — no `.env` files. See `fnox.toml` stub and `CONTRIBUTING.md`.

## Commits / PRs

Conventional commits. Each pushed commit should be CI-green. Use Graphite `gt` for stacked PRs (see `CONTRIBUTING.md`).
