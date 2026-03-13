## 1. Backend — API ordering parameter

- [x] 1.1 Add `ordering` query parameter to `GET /api/notebook/pages/` in `notebook/api/pages.py` with allowlist (`-updated_at`, `-created_at`, `title`) and default `-updated_at`
- [x] 1.2 Add API test for ordering parameter in `notebook/tests.py` — test each valid value and invalid fallback

## 2. Frontend — API client update

- [x] 2.1 Add `ordering` parameter to the `api.notebook.pages.list()` call in `frontend/src/lib/api/index.ts`

## 3. Frontend — Timestamp formatting utility

- [x] 3.1 Create a timestamp formatting helper in the notebook page component (or inline) using `Intl.RelativeTimeFormat` / `Intl.DateTimeFormat` — relative for <7 days, short date for older, full datetime for tooltips

## 4. Frontend — Sidebar timestamps and sort selector

- [x] 4.1 Add sort selector (dropdown or button group) above the page list in the notebook sidebar in `frontend/src/routes/notebook/+page.svelte`
- [x] 4.2 Persist sort preference in localStorage (`notebook-sort-order`) and restore on load
- [x] 4.3 Pass selected ordering to the API call when fetching pages
- [x] 4.4 Display timestamp on each sidebar page item — show `updated_at` by default, switch to `created_at` when sorted by creation date

## 5. Frontend — Page editor metadata timestamps

- [x] 5.1 Display "Created" and "Updated" timestamps in the page editor area below the title in `frontend/src/routes/notebook/+page.svelte` — show only "Created" when timestamps are within 1 second of each other
