#!/usr/bin/env bash
# run-manage.sh — Run manage.py with .env loaded
# Handles special chars (parens, $, etc.) in values.
# Usage: bash /opt/todoapp/deploy/run-manage.sh <command> [args...]
set -euo pipefail

APP_DIR="/opt/todoapp"

ENV_ARGS=()
while IFS='=' read -r key value; do
    [[ -z "$key" || "$key" == \#* ]] && continue
    ENV_ARGS+=("${key}=${value}")
done < "${APP_DIR}/.env"

exec env "${ENV_ARGS[@]}" uv run python "${APP_DIR}/manage.py" "$@"
