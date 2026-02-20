#!/usr/bin/env bash
# configure-caddy.sh — Set up Caddy with Tailscale HTTPS after joining the tailnet
# Usage: bash configure-caddy.sh <tailscale-hostname>
# Example: bash configure-caddy.sh ubuntu-2gb-ash-1.tail865b93.ts.net
set -euo pipefail

info()  { echo -e "\n\033[1;34m==>\033[0m \033[1m$*\033[0m"; }
error() { echo -e "\n\033[1;31mERROR:\033[0m $*" >&2; exit 1; }

[[ $EUID -eq 0 ]] || error "This script must be run as root."
[[ $# -eq 1 ]] || error "Usage: bash configure-caddy.sh <tailscale-hostname>"

HOSTNAME="$1"
APP_DIR="/opt/todoapp"

info "Generating Tailscale TLS certs for ${HOSTNAME}"
mkdir -p /etc/caddy/certs
tailscale cert \
    --cert-file /etc/caddy/certs/tailscale.crt \
    --key-file /etc/caddy/certs/tailscale.key \
    "${HOSTNAME}"
chown caddy:caddy /etc/caddy/certs/tailscale.crt /etc/caddy/certs/tailscale.key

info "Writing Caddyfile"
sed "s|HOSTNAME_PLACEHOLDER|${HOSTNAME}|" "${APP_DIR}/deploy/Caddyfile" > /etc/caddy/Caddyfile

info "Updating ALLOWED_HOSTS in .env"
sed -i "s|^ALLOWED_HOSTS=.*|ALLOWED_HOSTS=${HOSTNAME}|" "${APP_DIR}/.env"

info "Restarting services"
systemctl restart caddy todoapp

info "Done! Visit https://${HOSTNAME}"
