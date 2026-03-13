## Why

Notebook pages already have `created_at` and `updated_at` timestamps in the database, but they aren't surfaced in the UI. Users can't see when a page was created or last modified, and the sidebar always sorts by most-recently-updated with no option to change. Displaying timestamps and adding sort controls makes it easier to find pages chronologically and understand recency at a glance.

## What Changes

- Display `created_at` and `updated_at` timestamps on each page in the notebook sidebar list items
- Display timestamps in the page editor/detail area (e.g., metadata line below the title)
- Add a sort selector to the notebook sidebar allowing sorting by: last updated (default), created date, and title (alphabetical)
- Backend: add `ordering` query parameter to the pages list API to support sort options

## Capabilities

### New Capabilities

- `notebook-page-sorting`: Sort controls for the notebook sidebar with multiple ordering options (updated, created, title)

### Modified Capabilities

- `notebook-core`: Add `ordering` query parameter to `GET /api/notebook/pages/` endpoint
- `notebook-frontend`: Display timestamps on sidebar list items and page detail, integrate sort selector

## Non-goals

- Filtering by date range
- Custom/manual page ordering (drag-and-drop)
- Per-page-type sort preferences (same sort applies to both wiki and daily sections)

## Impact

- **Backend**: `notebook/api/pages.py` — add `ordering` query param to list endpoint
- **Frontend**: `frontend/src/routes/notebook/+page.svelte` — timestamp display in sidebar items and editor header, sort selector UI
- **API types**: `frontend/src/lib/api/types.ts` and `frontend/src/lib/api/index.ts` — add ordering param to pages list call
