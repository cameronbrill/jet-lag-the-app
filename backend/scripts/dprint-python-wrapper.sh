#!/usr/bin/env bash
set -euo pipefail

# Combined Python formatting: ssort then ruff format (stdout = formatted file).
# Usage: dprint exec passes {{file_path}} as last argument.

FILE_PATH="${!#}"
BACKEND_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BACKEND_ROOT"

uv run ssort "$FILE_PATH" >/dev/null 2>&1
uv run ruff format "$FILE_PATH" >/dev/null 2>&1
cat "$FILE_PATH"
