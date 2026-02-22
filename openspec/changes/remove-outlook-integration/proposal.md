## Why

The Outlook email import feature (added in `89e225b`) uses Microsoft Graph API to poll for categorized emails and create tasks. However, the Graph API can only access the Microsoft mailbox — it cannot see emails from linked accounts (e.g., Gmail connected via IMAP in Outlook desktop). Since the primary email account is Gmail, categories applied in Outlook desktop are stored locally and invisible to the API, making the feature non-functional for the intended workflow.

## What Changes

- **BREAKING**: Remove the Outlook email import feature entirely
- Remove `tasks/services/outlook_auth.py`, `outlook_client.py`, `outlook_import.py`
- Remove management commands `outlook_auth` and `poll_outlook` (`tasks/management/`)
- Remove all Outlook-related tests (`test_outlook_*.py`, `test_poll_outlook_command.py`)
- Remove `/import/outlook/status/` API endpoint from `tasks/api/import_tasks.py`
- Remove Outlook status check from `frontend/src/routes/+layout.svelte`
- Remove Outlook settings from `todoapp/settings.py`
- Remove `msal`, `html2text`, `requests` dependencies from `pyproject.toml` and regenerate `uv.lock`
- Remove Outlook env vars from `deploy/.env.example`
- Remove deploy helper scripts: `outlook-whoami.sh`, `outlook-debug.sh`
- Remove/archive the `openspec/changes/outlook-email-import/` change artifacts

## Capabilities

### New Capabilities

None — this is a removal-only change.

### Modified Capabilities

- `native-import`: Remove the Outlook status endpoint from the import API router. Core file import (JSON/CSV) is unaffected.

## Impact

- **Backend**: `tasks/api/import_tasks.py` loses the `/import/outlook/status/` endpoint. Outlook services and management commands are deleted. Settings file shrinks.
- **Frontend**: `+layout.svelte` loses the `onMount` Outlook status check. No other frontend changes.
- **Dependencies**: `msal`, `html2text`, `requests` removed from `pyproject.toml`. Lock file regenerated.
- **Deploy**: `.env.example` loses Outlook config block. Helper scripts removed. Crontab entry (if added on server) should be removed manually.
- **Server cleanup**: `outlook_token_cache.json` and `outlook_poll_status.json` on the production server should be manually deleted.
