#!/usr/bin/env bash
# auto-update.sh — Check for new commits and deploy if found
# Designed to run via systemd timer. Logs to journald.
set -euo pipefail

APP_DIR="/opt/todoapp"

# Fetch latest without merging
git -C "${APP_DIR}" fetch origin main --quiet

LOCAL=$(git -C "${APP_DIR}" rev-parse HEAD)
REMOTE=$(git -C "${APP_DIR}" rev-parse origin/main)

if [[ "${LOCAL}" == "${REMOTE}" ]]; then
    echo "Already up to date."
    exit 0
fi

echo "New commits detected (${LOCAL:0:7} -> ${REMOTE:0:7}), deploying..."
bash "${APP_DIR}/deploy/update.sh"
