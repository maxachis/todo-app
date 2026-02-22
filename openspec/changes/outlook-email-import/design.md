## Context

The ToDo app is a single-user, Tailscale-VPN'd Django + SvelteKit application with SQLite. It has no auth system, no background task runner, and no existing management commands. Import infrastructure exists for file uploads (JSON, CSV, TickTick) via `tasks/services/native_import.py`, and the Task model already has an `external_id` field (unique, nullable CharField) designed for third-party integration. The frontend has a toast notification system (`frontend/src/lib/stores/toast.ts`) supporting info/success/error types. Django settings use `os.environ.get()` for configuration.

The user has a personal Outlook.com account and wants to tag emails with a category in Outlook and have them appear as tasks. The server can make outbound connections but is not publicly reachable (Tailscale), ruling out webhooks but allowing pull-based polling.

## Goals / Non-Goals

**Goals:**
- Poll Microsoft Graph API on a cron schedule for emails tagged with a specific Outlook category
- Swap the category to mark emails as processed, without changing read/unread status or moving them
- Provide a clean triage experience: emails land in a dedicated list, user reviews/edits, then moves to final destination
- Deduplicate using Message-ID so re-runs are safe (idempotent)
- Surface polling errors to the user via the existing toast system
- Establish an OAuth foundation reusable for future Outlook integrations

**Non-Goals:**
- Two-way sync (tasks back to Outlook)
- Calendar, contacts, or To Do sync (v2 — same auth works)
- Sender → Person linkage (v2)
- Browsing the Outlook inbox from within the app
- Real-time push (webhooks not viable behind Tailscale)

## Decisions

### 1. Microsoft Graph API over IMAP

**Choice:** Use the Microsoft Graph REST API (`https://graph.microsoft.com/v1.0/me/messages`) with OAuth 2.0 Device Code flow.

**Alternatives considered:**
- *IMAP with app password:* Simpler auth (no OAuth), but IMAP has per-folder search only, unreliable category-to-keyword mapping, and requires MIME parsing. The user's desired workflow — tag any email with a category anywhere in the mailbox — isn't achievable with IMAP.
- *IMAP with OAuth (XOAUTH2):* Same IMAP limitations plus the same OAuth complexity as Graph API, with none of the benefits.

**Rationale:** Graph API provides cross-mailbox search by category (`$filter=categories/any(c:c eq 'ToDo')`), first-class category manipulation, and structured JSON responses (no MIME parsing). The auth overhead is bounded (~120 lines + `msal` dependency) and creates a foundation for future integrations. The category-based workflow the user wants is a native Graph API feature.

### 2. OAuth Device Code flow for authentication

**Choice:** A `manage.py outlook_auth` command that initiates the Device Code flow: the user visits a URL and enters a code to authorize.

**Alternatives considered:**
- *Browser-based Authorization Code flow:* Requires a callback URL, which means adding a route to Django and having the browser reach the server. Works, but more moving parts for a single-user CLI-friendly setup.
- *Client credentials (app-only):* No user interaction, but requires admin consent and accesses all mailboxes in the tenant — not appropriate for a personal account.

**Rationale:** Device Code flow is designed for headless/CLI scenarios. No callback URL needed (perfect for Tailscale-only server). The user runs the command once, authorizes in a browser, and tokens are stored. MSAL handles token caching and refresh automatically.

### 3. MSAL token cache in a JSON file

**Choice:** Use MSAL's built-in `SerializableTokenCache` persisted to a JSON file on disk (e.g., `outlook_token_cache.json`).

**Alternatives considered:**
- *Django model:* Adds a migration for a single row of token data in a single-user app.
- *Environment variable:* Tokens change on refresh, so a static env var doesn't work.
- *Encrypted file:* More secure but adds encryption key management. The server is Tailscale-only and the file permissions are sufficient.

**Rationale:** MSAL's token cache handles access token refresh, expiry, and multi-token management automatically. Persisting to a JSON file is the pattern recommended by MSAL documentation for daemon/CLI apps. No migration needed.

### 4. Category swap for processing markers

**Choice:** Search for emails with a "source" category (default: `ToDo`), process them, then replace with a "processed" category (default: `ToDo-Imported`) via `PATCH /me/messages/{id}`.

**Rationale:** This is a first-class Graph API operation. Categories are visible in the Outlook UI, so the user can see at a glance which emails have been imported. The swap is atomic per-email and doesn't affect read/unread status, folder location, or any other email property. The user applies the "ToDo" category from anywhere in their mailbox — no folder management needed.

### 5. html2text for HTML-to-plaintext conversion

**Choice:** Use the `html2text` library to convert email HTML to readable plain text.

**Alternatives considered:**
- *BeautifulSoup `.get_text()`:* Strips HTML but loses all formatting — paragraphs become one blob of text.
- *Use Graph API's `text` body format:* Graph can return `body.contentType: "text"`, but this is a server-side conversion that can lose structure. Requesting HTML and converting client-side gives better results.
- *Store raw HTML:* Security risk (XSS from email content) and doesn't match the existing plain-text `notes` field pattern.

**Rationale:** `html2text` produces readable plain text with basic structure preserved (paragraphs, lists, links). The Graph API returns structured `body.content` (HTML), which is cleaner input than raw MIME parts.

### 6. Dedicated "Email Inbox" list as triage queue

**Choice:** Auto-create a list named "Email Inbox" (configurable via settings) with a single default section. All imported email-tasks land there.

**Rationale:** Uses the existing List model with no schema changes. The user reviews tasks in this list, edits title/notes as needed, then uses the existing move functionality to place them in the right list/section.

### 7. Message-ID deduplication via external_id

**Choice:** Store the email's `internetMessageId` (from Graph API response) in `task.external_id`. Before creating a task, check if a task with that `external_id` already exists.

**Rationale:** The field already exists, is unique and indexed. No migration. Graph API provides `internetMessageId` as a stable identifier that persists across category changes.

### 8. Error surfacing via status file + API endpoint

**Choice:** The management command writes a JSON status file after each run. A lightweight API endpoint reads and returns it. The frontend checks on page load and shows a toast for errors.

**Rationale:** No migration needed. The command writes it, the API reads it, the frontend toasts it. Simple and stateless. Covers auth failures, API errors, and partial processing failures.

## Risks / Trade-offs

**[Azure app registration required]** → One-time setup (~5 minutes) in the Azure portal. The app is registered as a "public client" with `Mail.ReadWrite` permission. Personal Microsoft accounts are supported directly.

**[Refresh token expiry after 90 days of inactivity]** → If the cron job runs regularly (every 5 minutes), the token stays alive indefinitely. If the server is down for >90 days, re-run `manage.py outlook_auth`. The status file will surface an auth error via toast if this happens.

**[Graph API rate limits]** → Microsoft allows 10,000 requests per 10 minutes for personal accounts. A single poll is 1 request (list messages) + N requests (patch categories). At 5-minute intervals with typical email volume, this is nowhere near the limit.

**[Large/malicious email bodies]** → Truncate `task.notes` to a reasonable limit (e.g., 10,000 characters after HTML-to-text conversion). Graph API's `body.content` is already the primary body part, no attachment content included.

**[Overlapping cron runs]** → The command is idempotent (dedup via Message-ID + category check). Two concurrent runs might both try to create the same task, but the unique constraint on `external_id` will cause one to fail gracefully. Add a file-based lock as a simple guard.

**[Category doesn't exist in Outlook]** → The user needs to create the "ToDo" category in Outlook once. The command should document this and fail clearly if no emails match (which is the normal "nothing to do" case, not an error).
