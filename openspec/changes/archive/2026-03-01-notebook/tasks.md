## Tasks

### Phase 1: Backend — Models & Migrations

- [x] Create `notebook/` Django app with `Page` model (title, slug, content, page_type, date, timestamps)
- [x] Create `PageEntityMention` model (page FK, entity_type, entity_id, unique constraint)
- [x] Create `PageLink` model (source_page FK, target_page FK, unique constraint)
- [x] Write mention parser utility: extract `@[person:ID|Label]` and `[[type:ID|Label]]` patterns from content
- [x] Write mention reconciliation logic: diff parsed mentions against stored records, add/remove as needed
- [x] Generate and run migrations

### Phase 2: Backend — API

- [x] Register `notebook/` app and wire API router in project `urls.py` / Django Ninja
- [x] Implement `GET /api/notebook/pages/` — list pages with optional `search` and `page_type` filters
- [x] Implement `POST /api/notebook/pages/` — create page with auto-slug, get-or-create for daily pages, mention extraction on save
- [x] Implement `GET /api/notebook/pages/{slug}/` — retrieve page with content, entity_mentions, and backlinks
- [x] Implement `PUT /api/notebook/pages/{slug}/` — update page with mention re-extraction and reconciliation
- [x] Implement `DELETE /api/notebook/pages/{slug}/` — delete page (cascades mentions and links)
- [x] Implement `GET /api/notebook/mentions/{entity_type}/{entity_id}/` — entity backlinks endpoint
- [x] Add API schemas (PageOut, PageCreateInput, PageUpdateInput, MentionOut, BacklinkOut)

### Phase 3: Backend — Tests

- [x] Test page CRUD (create wiki, create daily, get-or-create daily, update, delete)
- [x] Test mention parsing and reconciliation (add mentions, remove mentions, duplicates)
- [x] Test backlinks endpoint (person mentions, task mentions, empty results)
- [x] Test page list filters (search, page_type)

### Phase 4: Frontend — Types & API Client

- [x] Add TypeScript types: `Page`, `PageCreateInput`, `PageUpdateInput`, `PageMention`, `PageBacklink`
- [x] Add API client methods: `notebook.pages.list()`, `.create()`, `.get(slug)`, `.update(slug)`, `.delete(slug)`, `notebook.mentions(entityType, entityId)`

### Phase 5: Frontend — Notebook Route & Editor

- [x] Create `/notebook` route with two-panel layout (sidebar + editor)
- [x] Implement page sidebar: "New Page" button, "Today" button, page list grouped by type
- [x] Implement URL-based page selection (`/notebook/{slug}`)
- [x] Implement textarea editor with auto-expanding height
- [x] Implement editable title input
- [x] Implement auto-save on blur and 1-second debounced save on typing
- [x] Add save indicator

### Phase 6: Frontend — Typeahead Mentions

- [x] Implement `@` trigger detection in textarea (word-boundary aware)
- [x] Implement floating people typeahead dropdown with keyboard navigation
- [x] Implement `[[` trigger detection in textarea
- [x] Implement floating entity typeahead dropdown with grouped results (pages, tasks, orgs, projects) and type badges
- [x] Wire typeahead selection to insert mention syntax at cursor position

### Phase 7: Frontend — Backlinks & Navigation

- [x] Add "Backlinks" section below editor textarea on notebook pages
- [x] Add "Notebook Mentions" collapsible section to People detail view
- [x] Add "Notebook Mentions" collapsible section to Organization detail view
- [x] Add "Notebook Mentions" collapsible section to Task detail panel
- [x] Add "Notebook Mentions" collapsible section to Project cards
- [x] Add "Notebook" tab to top navigation bar in `+layout.svelte`
