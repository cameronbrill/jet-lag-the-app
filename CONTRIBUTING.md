# Contributing

## Tooling

Install [mise](https://mise.jdx.dev/) and run `mise install` at the repo root and in `backend/` / `client/` config roots as needed.

- **Python**: `mise run //backend:deps` (uses `uv`).
- **Kotlin**: JDK **17+** is required for the Android Gradle Plugin — `client/mise.toml` pins a Temurin distribution via mise.
- **Hooks**: `hk install --mise` (hk delegates to `mise run` tasks). On macOS x86_64, install hk via Homebrew.
- **Docker + Tilt**: Required for the local dev stack. Run `docker compose up -d` to start Postgres 18 and Valkey 9, then `mise run :dev` to launch Tilt.

## Secrets

This project uses **[fnox](https://fnox.jdx.dev/guide/what-is-fnox.html)** (active) instead of `.env` files. Replace the stub `fnox.toml` with `fnox init` output and encrypt values (`fnox set … --provider age`). Document required keys in PRs and in `README.md`, not in dotenv samples.

## Graphite

Use the Graphite CLI (`gt`) for stacked branches/PRs — see the [cheatsheet](https://graphite.com/docs/cheatsheet). Prefer `gt submit` / `gt submit --stack` over ad-hoc multi-branch `git push` for stacked work.

## Commits

Follow conventional commits (`feat(client): …`). Each commit should be a coherent, **CI-green** unit; fold red-only milestones before pushing if they would break `mise run :check`.

## Local checks

- `mise run :format` — format all files (dprint).
- `mise run :lint` — Markdown only (`markdownlint`); use `mise run //backend:lint` and `mise run //client:lint` for code.
- `mise run //backend:test` — backend tests (add `--ci` for CI mode, `--cov` for coverage).
- `mise run //client:test` — client tests.
- `mise run :check` — full monorepo gate (format check, markdownlint, backend lint/typecheck/tests, client lint/tests).

## Schema changes

The database stack uses **Atlas** for migrations and **sqlc** for typed query generation. When modifying the schema or queries:

1. Edit `backend/db/schema.sql` with schema changes.
2. `mise run //backend:db-diff <name>` — plan a migration file via Atlas.
3. `mise run //backend:codegen` — regenerate typed Python code in `db/generated/`.
4. `mise run //backend:test` — verify against real Postgres.

**Important**: `mise run //backend:codegen` must be run after any query file changes. Do not hand-edit files in `db/generated/`.
