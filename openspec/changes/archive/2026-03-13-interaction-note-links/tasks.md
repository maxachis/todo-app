## 1. Backend Model & Migration

- [x] 1.1 Add `InteractionPageLink` model to `network/models/task_links.py` with `interaction` FK, `page` FK, `created_at`, and unique constraint on `(interaction, page)`
- [x] 1.2 Register model in `network/models/__init__.py`
- [x] 1.3 Generate and apply migration (`python manage.py makemigrations network`)
- [x] 1.4 Add `"interaction"` to `entity_type` choices in `PageEntityMention` model (`notebook/models.py`)
- [x] 1.5 Generate and apply migration for notebook (`python manage.py makemigrations notebook`)

## 2. Backend API — Interaction-Page Link Endpoints

- [x] 2.1 Add schemas for interaction-page links in `network/api/schemas.py` (`InteractionPageLinkIn`, `LinkedPageOut`)
- [x] 2.2 Create API endpoints in `network/api/task_links.py`: `GET/POST /interactions/{id}/pages/`, `DELETE /interactions/{id}/pages/{page_id}/`
- [x] 2.3 Register new routes in `network/api/__init__.py` router (already registered via existing task_links router)

## 3. Backend API — Reverse Endpoint & Mention Parser

- [x] 3.1 Add `GET /notebook/pages/{slug}/interactions/` endpoint in `notebook/api/pages.py` returning linked interactions with type, date, person names
- [x] 3.2 Add `LinkedInteractionOut` schema in `notebook/api/schemas.py`
- [x] 3.3 Update mention parser regex in `notebook/mentions.py` to recognize `[[interaction:ID|Label]]` and map to `entity_type="interaction"` in `reconcile_mentions()`

## 4. Frontend API Client & Types

- [x] 4.1 Add `InteractionPageLink` and `LinkedPage` types to `frontend/src/lib/api/types.ts`
- [x] 4.2 Add `LinkedInteraction` type for the reverse direction
- [x] 4.3 Add API client methods in `frontend/src/lib/api/index.ts`: `taskLinks.interactionPages.list()`, `.add()`, `.remove()`, and `notebook.pages.interactions()`

## 5. Frontend — Interaction Detail Panel

- [x] 5.1 Add "Linked Notes" section to `frontend/src/routes/crm/interactions/+page.svelte` below existing "Linked Tasks", using a typeahead selector for notebook pages
- [x] 5.2 Load all notebook pages for the typeahead and linked pages for the selected interaction
- [x] 5.3 Wire add/remove callbacks to API client methods

## 6. Frontend — Notebook Page

- [x] 6.1 Add "Linked Interactions" section to `frontend/src/routes/notebook/+page.svelte` below backlinks, showing interactions linked to the current page
- [x] 6.2 Fetch linked interactions via `notebook.pages.interactions(slug)` on page selection
- [x] 6.3 Each entry shows interaction type, date, people — clicking navigates to `/crm/interactions?selected={id}`
- [x] 6.4 Add interactions to the CM6 entity autocomplete data so `[[interaction:` triggers completion

## 7. Backend Tests

- [x] 7.1 Add API tests for interaction-page link CRUD in `network/tests/` or `tasks/tests/` (create, list, duplicate, delete, cascade)
- [x] 7.2 Add test for `GET /notebook/pages/{slug}/interactions/` endpoint
- [x] 7.3 Add test for mention parser recognizing `[[interaction:ID|Label]]` syntax
