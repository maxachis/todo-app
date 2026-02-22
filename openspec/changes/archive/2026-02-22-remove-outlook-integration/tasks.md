## 1. Remove Backend Services and Management Commands

- [x] 1.1 Delete `tasks/services/outlook_auth.py`
- [x] 1.2 Delete `tasks/services/outlook_client.py`
- [x] 1.3 Delete `tasks/services/outlook_import.py`
- [x] 1.4 Delete `tasks/management/` directory (commands: `outlook_auth`, `poll_outlook`, plus `__init__.py` files)

## 2. Remove API Endpoint and Settings

- [x] 2.1 Remove `/import/outlook/status/` endpoint and `json` import from `tasks/api/import_tasks.py`
- [x] 2.2 Remove all Outlook settings (`OUTLOOK_CLIENT_ID`, `OUTLOOK_TENANT_ID`, `OUTLOOK_SOURCE_CATEGORY`, `OUTLOOK_PROCESSED_CATEGORY`, `OUTLOOK_INBOX_LIST_NAME`, `OUTLOOK_TOKEN_CACHE_FILE`, `OUTLOOK_POLL_STATUS_FILE`) from `todoapp/settings.py`

## 3. Remove Frontend Status Check

- [x] 3.1 Remove the `onMount` Outlook status check block and unused imports (`onMount`, `apiRequest`, `addToast`) from `frontend/src/routes/+layout.svelte` (only remove imports if no other code uses them)

## 4. Remove Tests

- [x] 4.1 Delete `tasks/tests/test_outlook_auth.py`
- [x] 4.2 Delete `tasks/tests/test_outlook_client.py`
- [x] 4.3 Delete `tasks/tests/test_outlook_import.py`
- [x] 4.4 Delete `tasks/tests/test_poll_outlook_command.py`

## 5. Remove Dependencies

- [x] 5.1 Remove `msal` and `html2text` from `pyproject.toml` (verify `requests` is not used elsewhere before removing)
- [x] 5.2 Regenerate `uv.lock` with `uv lock`

## 6. Remove Deploy Config and Scripts

- [x] 6.1 Remove Outlook env var block from `deploy/.env.example`
- [x] 6.2 Delete `deploy/outlook-whoami.sh`
- [x] 6.3 Delete `deploy/outlook-debug.sh`

## 7. Remove Change Artifacts

- [x] 7.1 Delete `openspec/changes/outlook-email-import/` directory

## 8. Verify

- [x] 8.1 Run `uv run python -m pytest tasks/tests/test_api_setup.py -q` to confirm backend tests pass
- [x] 8.2 Run `cd frontend && npm run check` to confirm frontend type checks pass
