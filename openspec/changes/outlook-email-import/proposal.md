## Why

Emails frequently represent actionable work — requests, follow-ups, decisions — but they live in Outlook, disconnected from the task management system. Manually re-typing email subjects and details into the ToDo app is friction that causes tasks to be lost. A category-based workflow lets the user tag any email with a "ToDo" category in Outlook, and have it appear as an editable task in the app, ready to be triaged into the appropriate list and section.

## What Changes

- Add a **`manage.py poll_outlook`** management command that queries the Microsoft Graph API for emails with a configurable Outlook category (default: "ToDo"), creates tasks from them, and replaces the category with a "processed" category (default: "ToDo-Imported") — without moving or marking them as read.
- Add a **`manage.py outlook_auth`** management command that performs the OAuth 2.0 Device Code flow for one-time authentication. Tokens are stored in a local JSON file and auto-refreshed.
- Create a **dedicated "Email Inbox" list** that serves as a triage queue for imported email-tasks. New email-tasks land here for review before the user moves them to their final list/section.
- **Strip email HTML to plain text** for the task notes field, so the email body is readable without HTML artifacts.
- Store the email **Internet Message-ID in `task.external_id`** for deduplication — if an email has already been imported, skip it.
- The imported task's **title and notes are editable** in the UI before the user moves it to a destination list/section (this is existing behavior — the triage workflow of reviewing and moving tasks from the inbox list is the intended flow).
- Add **Django settings for Graph API configuration**: Azure client ID, tenant ID, category names, and target list name, all sourced from environment variables.
- Show a **toast notification on import failure** so the user knows if polling encountered errors (e.g., expired tokens, API failures).
- The command is designed to run as a **cron job** (e.g., every 5 minutes) on the server.

## Capabilities

### New Capabilities
- `outlook-email-import`: Microsoft Graph API polling for category-tagged emails, email-to-task conversion with HTML-to-text extraction, OAuth Device Code authentication, deduplication via Message-ID, and cron-friendly management command.

### Modified Capabilities
_(none — this is a new import channel that doesn't change existing import, task, or list behavior)_

## Impact

- **Backend**: Two new management commands in `tasks/management/commands/` (auth + polling), new Django settings for Graph API config, new service module for Graph API client and email parsing.
- **API**: New endpoint to surface import errors as toast notifications.
- **Frontend**: Minimal — toast trigger for polling errors. The "Email Inbox" list behaves like any other list. No new pages or components required.
- **Infrastructure**: Cron job entry on the production server. One-time Azure app registration. No database migrations needed (`external_id` field already exists on Task).
- **Dependencies**: `msal` (Microsoft Authentication Library) for OAuth. `html2text` for HTML-to-plaintext conversion. `requests` for Graph API calls (likely already available).
- **Non-goals (v2)**: Sender → Person linkage via the network module. Two-way sync. Calendar/contacts integration (though the same auth foundation enables these later). Browsing the Outlook inbox from within the app.
