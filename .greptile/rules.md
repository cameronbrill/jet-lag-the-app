# Greptile review rules

- Public behavior changes should include tests (pytest / `commonTest`) in the same PR.
- No `TODO` / `FIXME` without a tracked issue link.
- PR titles follow conventional commits.
- Python: ruff + ty clean; avoid unexplained `type: ignore`.
- Kotlin: respect detekt; avoid unjustified `@Suppress`.
- Client feature modules must not depend on other feature modules.
- `expect/actual` pairs must cover Android, iOS, and desktop targets.
- Format with **dprint**; do not introduce parallel TOML formatters (no taplo fmt).
- Secrets only via **fnox** — reject `.env*` files and plaintext secrets in `fnox.toml`.
- Prefer small, CI-green commits; flag mixed unrelated changes or unclear stack boundaries.
