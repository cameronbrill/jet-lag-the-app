# Contributing

## Tooling

Install [mise](https://mise.jdx.dev/) and run `mise install` at the repo root and in `backend/` / `client/` config roots as needed.

- **Python**: `mise run //backend:deps` (uses `uv`).
- **Kotlin**: JDK **17+** is required for the Android Gradle Plugin — `client/mise.toml` pins a Temurin distribution via mise.
- **Hooks**: `hk install --mise` (hk delegates to `mise run` tasks).

## Secrets

This project uses **[fnox](https://fnox.jdx.dev/guide/what-is-fnox.html)** instead of `.env` files. Replace the stub `fnox.toml` with `fnox init` output and encrypt values (`fnox set … --provider age`). Document required keys in PRs and in `README.md`, not in dotenv samples.

## Graphite

Use the Graphite CLI (`gt`) for stacked branches/PRs — see the [cheatsheet](https://graphite.com/docs/cheatsheet). Prefer `gt submit` / `gt submit --stack` over ad-hoc multi-branch `git push` for stacked work.

## Commits

Follow conventional commits (`feat(client): …`). Each commit should be a coherent, **CI-green** unit; fold red-only milestones before pushing if they would break `mise run :check`.

## Local checks

- `mise run :check` — full monorepo gate (format check, hk, backend lint/typecheck/tests, client lint/tests).
