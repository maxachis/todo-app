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

info "Installing dependencies"
"${APP_DIR}/venv/bin/pip" install --quiet django markdown bleach gunicorn

info "Running migrations"
sudo -u "${APP_USER}" bash -c "
    set -a
    source ${APP_DIR}/.env
    set +a
    ${APP_DIR}/venv/bin/python ${APP_DIR}/manage.py migrate --noinput
    ${APP_DIR}/venv/bin/python ${APP_DIR}/manage.py collectstatic --noinput
"

info "Restarting app"
systemctl restart todoapp

info "Done! App is live."
