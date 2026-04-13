#!/usr/bin/env bash
set -euo pipefail

FILE_PATH="${!#}"
if command -v mise >/dev/null 2>&1; then
  mise exec -- ktlint -F "$FILE_PATH"
else
  ktlint -F "$FILE_PATH"
fi
cat "$FILE_PATH"
