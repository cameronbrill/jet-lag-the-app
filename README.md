# jet-lag-the-app

Creator-focused companion for playing **Jet Lag: The Game** in real life — Kotlin Multiplatform clients (Android, iOS, desktop) with a FastAPI backend for real-time game sync.

## Repository layout

- `backend/` — FastAPI + WebSocket game sync, pytest suites under `backend/tests/`.
- `client/` — Gradle KMP workspace (`:core*`, `:feature-*`, `:app:*`).
- `.toolchain/` — shared ruff/ty/detekt/ktlint baselines.
- `.mise/tasks/` — repo-wide file tasks (`format`, `lint`, `check`, …).

## Prerequisites

- [mise](https://mise.jdx.dev/) for pinned CLIs (`dprint`, `hk`, `ktlint`, `fnox`, …).
- **JDK 17+** for Gradle (Android). `client/mise.toml` documents a pinned Temurin build.
- **Python 3.14+** for the backend (see `backend/pyproject.toml`).
- **Docker** + [Tilt](https://tilt.dev/) for the local dev stack.

## Infrastructure

Local development uses `docker-compose.yml` to run:

- **Postgres 18** — primary data store
- **Valkey 9** — caching / pub-sub

[Tilt](https://tilt.dev/) orchestrates services on top of docker-compose for live-reload development (`mise run :dev`).

## Quickstart

```bash
mise install
mise run :dev
```

That installs pinned tools and starts the Tilt stack (Postgres 18, Valkey 9, backend, and related local resources). Apply database migrations when the database is up (`mise run //backend:migrate`). Run the desktop client from `client/` with `./gradlew :app:desktopApp:run` after `mise install` in that directory if you need the JVM toolchain.

Full quality gate:

```bash
mise run :check
```

CI uses Buildkite (`.buildkite/pipeline.yml`) calling the same mise tasks.

## Database

Schema management uses **Atlas** for migrations and **sqlc** (sqlc-gen-python) for generating typed Python query code.

### Schema change workflow

1. Edit `backend/db/schema.sql` with the desired schema changes.
2. `mise run //backend:db-diff <name>` — Atlas plans a migration file.
3. `mise run //backend:codegen` — sqlc regenerates typed Python in `db/generated/`.
4. `mise run //backend:test` — verify against real Postgres.

Generated code in `db/generated/` must not be hand-edited.

## Docs

- `CONTRIBUTING.md` — Graphite (`gt`), fnox, commit discipline.
- `CLAUDE.md` — concise agent-oriented command reference.
