#!/usr/bin/env bash
# update.sh — Pull latest code and restart the app
# Run as root: bash /opt/todoapp/deploy/update.sh
set -euo pipefail

APP_DIR="/opt/todoapp"
APP_USER="todoapp"

info() { echo -e "\n\033[1;34m==>\033[0m \033[1m$*\033[0m"; }
error() { echo -e "\n\033[1;31mERROR:\033[0m $*" >&2; exit 1; }

[[ $EUID -eq 0 ]] || error "This script must be run as root."

info "Pulling latest code"
git -C "${APP_DIR}" pull

info "Fixing file ownership"
chown -R "${APP_USER}:${APP_USER}" "${APP_DIR}"

info "Installing dependencies"
"${APP_DIR}/venv/bin/pip" install --quiet django markdown bleach gunicorn django-ninja pydantic

info "Building frontend"
sudo -u "${APP_USER}" bash -lc "cd '${APP_DIR}/frontend' && npm install && npm run build"

info "Running migrations"
# Load .env line-by-line to handle special chars (parens, $, etc.) in values
ENV_ARGS=()
while IFS='=' read -r key value; do
    [[ -z "$key" || "$key" == \#* ]] && continue
    ENV_ARGS+=("${key}=${value}")
done < "${APP_DIR}/.env"

sudo -u "${APP_USER}" env "${ENV_ARGS[@]}" \
    "${APP_DIR}/venv/bin/python" "${APP_DIR}/manage.py" migrate --noinput
sudo -u "${APP_USER}" env "${ENV_ARGS[@]}" \
    "${APP_DIR}/venv/bin/python" "${APP_DIR}/manage.py" collectstatic --noinput

info "Restarting app"
systemctl restart todoapp
systemctl reload nginx || true

info "Done! App is live."
