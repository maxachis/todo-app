## 1. Backend: API Filter

- [x] 1.1 Add `entity_type` and `entity_id` query params to `GET /api/notebook/pages/` in `notebook/api/pages.py`. Filter pages via `PageEntityMention` join when both params are present.
- [x] 1.2 Add API tests for entity filtering: filter by person, filter by org, combined with search, no matches returns empty, missing entity_id ignores filter. (`notebook/tests.py`)

## 2. Frontend: API Client

- [x] 2.1 Update `api.notebook.pages.list()` in `frontend/src/lib/api/index.ts` to accept optional `entity_type` and `entity_id` params.
- [x] 2.2 Update `PageListParams` type in `frontend/src/lib/api/types.ts` if needed.

## 3. Frontend: Entity Filter UI

- [x] 3.1 Add entity filter TypeaheadSelect to the notebook sidebar in `frontend/src/routes/notebook/+page.svelte`. Use existing people/orgs data (already loaded on mount). Group options by type.
- [x] 3.2 Wire the filter selection to re-fetch the page list with `entity_type` and `entity_id` params. Show a filter chip with the selected entity name and a clear (x) button.
- [x] 3.3 Handle empty state when filter returns no pages — show "No pages mention this entity" message.

## 4. Frontend: Type Check

- [x] 4.1 Run `cd frontend && npm run check` and fix any TypeScript errors.
