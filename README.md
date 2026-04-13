# jet-lag-the-app

Creator-focused companion for playing **Jet Lag: The Game** in real life — Kotlin Multiplatform clients (Android, iOS, desktop) with a FastAPI backend for real-time game sync.

## Repository layout

- `backend/` — FastAPI + WebSocket game sync, pytest suites under `backend/tests/`.
- `client/` — Gradle KMP workspace (`:core*`, `:feature-*`, `:app:*`).
- `.toolchain/` — shared ruff/ty/detekt/ktlint baselines.
- `.mise/tasks/` — repo-wide file tasks (`fmt`, `format-ci`, `lint-hk`, `check`, …).

## Prerequisites

- [mise](https://mise.jdx.dev/) for pinned CLIs (`dprint`, `hk`, `ktlint`, `fnox`, …).
- **JDK 17+** for Gradle (Android). `client/mise.toml` documents a pinned Temurin build.
- **Python 3.13+** for the backend (see `backend/pyproject.toml`).

## Quickstart

```bash
mise install
mise run :backend:deps
mise run :backend:start   # uvicorn via uv

cd client
mise install               # Java toolchain for this config root
./gradlew :app:desktopApp:run
```

Full quality gate:

```bash
mise run :check
```

CI uses Buildkite (`.buildkite/pipeline.yml`) calling the same mise tasks.

## Docs

- `CONTRIBUTING.md` — Graphite (`gt`), fnox, commit discipline.
- `CLAUDE.md` — concise agent-oriented command reference.
