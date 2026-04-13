#!/usr/bin/env bash
set -euo pipefail

FILE_PATH="${!#}"
BACKEND_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BACKEND_ROOT"

mise x -- uv run ssort "$FILE_PATH" > /dev/null
mise x -- uv run ruff format "$FILE_PATH" > /dev/null
cat "$FILE_PATH"
