#!/usr/bin/env bash
# outlook-whoami.sh — Show which Microsoft account is authenticated
set -euo pipefail

APP_DIR="/opt/todoapp"

ENV_ARGS=()
while IFS='=' read -r key value; do
    [[ -z "$key" || "$key" == \#* ]] && continue
    ENV_ARGS+=("${key}=${value}")
done < "${APP_DIR}/.env"

cd "${APP_DIR}"
env "${ENV_ARGS[@]}" DJANGO_SETTINGS_MODULE=todoapp.settings uv run python -c "
import django; django.setup()
from tasks.services.outlook_auth import load_token_cache, get_msal_app
cache = load_token_cache()
app = get_msal_app(cache)
accounts = app.get_accounts()
if not accounts:
    print('No authenticated account found. Run: manage.py outlook_auth')
else:
    for a in accounts:
        print(a.get('username', 'unknown'))
"
