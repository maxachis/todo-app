#!/usr/bin/env bash
# outlook-debug.sh — List recent emails and their categories from Graph API
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
from tasks.services.outlook_auth import acquire_token_silent
import requests

token = acquire_token_silent()
if not token:
    print('ERROR: Could not acquire token. Run: manage.py outlook_auth')
    exit(1)

resp = requests.get(
    'https://graph.microsoft.com/v1.0/me/messages'
    '?\$select=subject,categories&\$top=10',
    headers={'Authorization': f'Bearer {token}'},
    timeout=30,
)
resp.raise_for_status()
messages = resp.json().get('value', [])
if not messages:
    print('No messages found in mailbox.')
else:
    for m in messages:
        cats = m.get('categories', [])
        subj = m.get('subject', '(no subject)')
        print(f'{cats} -- {subj}')
"
