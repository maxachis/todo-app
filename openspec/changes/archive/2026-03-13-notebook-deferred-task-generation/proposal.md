## Why

The notebook editor auto-saves content after 1 second of inactivity via debounced saves. Every save calls `reconcile_mentions()` on the server, which runs `create_tasks_from_checkboxes()` — detecting `- [ ] text` patterns and creating tasks in the Inbox. This means a task is created the moment the user pauses typing for 1 second, even if they're still composing the checkbox line. The premature task creation is disruptive: the server rewrites the line content with a `[[task:ID|...]]` link mid-edit.

Task generation should only run when the user has clearly finished editing a checkbox line — by pressing Enter (moving to the next line) or by leaving the editor (blur).

## What Changes

- Add a `process_checkboxes` flag to the page update API, defaulting to `true` for backward compatibility
- Frontend debounced saves (typing) pass `process_checkboxes: false` — content is saved but no tasks are generated
- Frontend blur saves pass `process_checkboxes: true` — tasks are generated from finalized checkboxes
- Frontend detects Enter keypress after a checkbox line in the CodeMirror editor and triggers an immediate save with `process_checkboxes: true`

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `note-checkbox-tasks`: Task generation is deferred from every save to only blur and newline events

## Non-goals

- Changing the 1-second debounce interval
- Client-side task creation (task creation stays server-side)
- Changing how `@new[...]` contact draft creation is triggered (it doesn't rewrite content, so premature triggering is harmless)

## Impact

- **Backend**: `notebook/api/schemas.py` — add `process_checkboxes` field to `PageUpdateInput`
- **Backend**: `notebook/mentions.py` — `reconcile_mentions` accepts flag to skip checkbox processing
- **Backend**: `notebook/api/pages.py` — pass flag through to `reconcile_mentions`
- **Frontend**: `frontend/src/routes/notebook/+page.svelte` — pass flag to save calls
- **Frontend**: `frontend/src/lib/api/` — update notebook API client to support the flag
- **Frontend**: `frontend/src/lib/components/notebook/createEditor.ts` — add Enter-after-checkbox detection callback
