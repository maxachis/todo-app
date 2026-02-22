## 1. Configuration & Dependencies

- [x] 1.1 Add `msal` and `html2text` to project dependencies (`pyproject.toml` / `uv`)
- [x] 1.2 Add Outlook Graph API settings to `todoapp/settings.py`: `OUTLOOK_CLIENT_ID` (required), `OUTLOOK_TENANT_ID` (default `consumers`), `OUTLOOK_SOURCE_CATEGORY` (default `ToDo`), `OUTLOOK_PROCESSED_CATEGORY` (default `ToDo-Imported`), `OUTLOOK_INBOX_LIST_NAME` (default `Email Inbox`), `OUTLOOK_TOKEN_CACHE_FILE` (default `BASE_DIR / "outlook_token_cache.json"`), `OUTLOOK_POLL_STATUS_FILE` (default `BASE_DIR / "outlook_poll_status.json"`), all read from `os.environ`

## 2. OAuth Authentication

- [x] 2.1 Create `tasks/services/outlook_auth.py` with functions: `get_msal_app()` (creates MSAL PublicClientApplication with serializable token cache), `load_token_cache()`, `save_token_cache()`, `acquire_token_silent()` (returns access token or None), `initiate_device_code_flow()`, `acquire_token_by_device_code()`
- [x] 2.2 Create `tasks/management/commands/outlook_auth.py` management command: initiates Device Code flow, prints URL and code, waits for authorization, saves tokens to cache file
- [x] 2.3 Add `Mail.ReadWrite` as the required Graph API scope in the auth module

## 3. Graph API Client

- [x] 3.1 Create `tasks/services/outlook_client.py` with a function `fetch_emails_by_category(category: str) -> list[dict]` that calls `GET /me/messages?$filter=categories/any(c:c eq '{category}')&$select=id,subject,body,sender,internetMessageId,isRead` with the access token
- [x] 3.2 Add function `update_email_categories(message_id: str, categories: list[str])` that calls `PATCH /me/messages/{id}` to replace categories
- [x] 3.3 Handle pagination: follow `@odata.nextLink` if the response includes it
- [x] 3.4 Handle token expiry: attempt silent token acquisition before each poll, surface auth errors clearly

## 4. Email Parsing Service

- [x] 4.1 Create `tasks/services/outlook_import.py` with a function `parse_graph_message(message: dict) -> dict` that extracts subject, sender (name + email), internetMessageId, and body (HTML → plaintext via `html2text`)
- [x] 4.2 Add body truncation to 10,000 characters with a truncation indicator
- [x] 4.3 Add sender line prepended to body: `"From: {sender}\n\n{body}"`
- [x] 4.4 Create function `create_task_from_email(parsed: dict, section: Section) -> Task | None` that creates a Task with title from subject, notes from body, external_id from internetMessageId, skipping if external_id already exists

## 5. Polling Management Command

- [x] 5.1 Create `tasks/management/commands/poll_outlook.py` with a `Command` class
- [x] 5.2 Validate required settings on startup — exit with clear error if `OUTLOOK_CLIENT_ID` is missing or token cache doesn't exist
- [x] 5.3 Acquire access token silently via `outlook_auth.acquire_token_silent()`, fail with re-auth message if token unavailable
- [x] 5.4 Fetch emails with source category via `outlook_client.fetch_emails_by_category()`
- [x] 5.5 For each email: parse with `parse_graph_message`, create task with `create_task_from_email`, swap category via `update_email_categories` (remove source, add processed)
- [x] 5.6 Auto-create the "Email Inbox" list and default section if they don't exist (using `get_or_create`)
- [x] 5.7 Write poll status JSON file on completion: `{"timestamp": ..., "status": "success"|"error", "tasks_created": N, "tasks_skipped": N, "error": "..."}`. Use atomic write (write to temp file, rename)

## 6. Poll Status API Endpoint

- [x] 6.1 Add `GET /api/import/outlook/status/` endpoint in `tasks/api/import_tasks.py` (or a new router file) that reads and returns the poll status JSON file
- [x] 6.2 Return `{"status": "no_data"}` if the status file doesn't exist yet

## 7. Frontend Error Toast

- [x] 7.1 On app load (in `+layout.svelte` or the main tasks page), fetch `/api/import/outlook/status/` and show an error toast via `addToast()` if `status === "error"`, including the error message

## 8. Tests

- [x] 8.1 Unit tests for `outlook_auth.py`: token cache load/save, silent acquisition with valid/expired tokens (`tasks/tests/test_outlook_auth.py`)
- [x] 8.2 Unit tests for `outlook_client.py`: mock Graph API responses, pagination, error handling (`tasks/tests/test_outlook_client.py`)
- [x] 8.3 Unit tests for `parse_graph_message`: HTML email, plain-text body, truncation, sender extraction (`tasks/tests/test_outlook_import.py`)
- [x] 8.4 Unit tests for `create_task_from_email`: task creation, deduplication via external_id, section assignment
- [x] 8.5 Integration test for `poll_outlook` command: mock Graph API, verify tasks created, categories swapped, status file written (`tasks/tests/test_poll_outlook_command.py`)
- [x] 8.6 API test for `/api/import/outlook/status/` endpoint: status file present, status file missing

## 9. Deployment

- [x] 9.1 Document Azure app registration: portal.azure.com → App registrations → New → Add Mail.ReadWrite permission → Enable public client flows → Copy client ID
- [x] 9.2 Document one-time auth: `uv run python manage.py outlook_auth`
- [x] 9.3 Document cron setup: `*/5 * * * * cd /path/to/app && uv run python manage.py poll_outlook >> /var/log/poll_outlook.log 2>&1`
- [x] 9.4 Add environment variables to production `.env` or deployment config
