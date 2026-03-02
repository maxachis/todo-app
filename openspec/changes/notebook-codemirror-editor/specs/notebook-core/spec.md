## MODIFIED Requirements

### Requirement: Page CRUD API endpoints
The system SHALL expose JSON API endpoints under `/api/notebook/` for page operations: `GET /api/notebook/pages/` (list all pages, ordered by `-updated_at`, with optional `search` query param filtering by title substring and optional `page_type` query param), `POST /api/notebook/pages/` (create), `GET /api/notebook/pages/{slug}/` (retrieve by slug), `PUT /api/notebook/pages/{slug}/` (update), `DELETE /api/notebook/pages/{slug}/` (delete). The create endpoint SHALL accept `title`, `content` (optional), `page_type` (optional, default `wiki`), and `date` (required if `page_type` is `daily`). The update endpoint SHALL accept `title` and `content`. The update endpoint SHALL return the potentially-rewritten content (from server-side checkbox-to-task processing) in the response, and the frontend editor SHALL apply returned content differences via targeted CM6 transactions that preserve cursor position, rather than via textarea value binding.

#### Scenario: List all pages
- **WHEN** a client sends `GET /api/notebook/pages/`
- **THEN** the server responds with all pages ordered by most recently updated first, each including `id`, `title`, `slug`, `page_type`, `date`, `created_at`, `updated_at`

#### Scenario: List pages filtered by type
- **WHEN** a client sends `GET /api/notebook/pages/?page_type=daily`
- **THEN** the server responds with only daily pages

#### Scenario: Search pages by title
- **WHEN** a client sends `GET /api/notebook/pages/?search=migration`
- **THEN** the server responds with pages whose title contains "migration" (case-insensitive)

#### Scenario: Create a wiki page
- **WHEN** a client sends `POST /api/notebook/pages/` with `{"title": "Migration Runbook", "content": "Notes here"}`
- **THEN** the server creates the page, extracts entity mentions from content, and responds with status 201 and the full page object

#### Scenario: Create a daily page
- **WHEN** a client sends `POST /api/notebook/pages/` with `{"page_type": "daily", "date": "2026-02-28"}`
- **THEN** the server creates the page with title and slug set to `"2026-02-28"` and responds with status 201

#### Scenario: Create daily page for existing date returns existing
- **WHEN** a client sends `POST /api/notebook/pages/` with `{"page_type": "daily", "date": "2026-02-28"}` and a daily page for that date exists
- **THEN** the server responds with the existing page (get-or-create behavior)

#### Scenario: Retrieve page by slug
- **WHEN** a client sends `GET /api/notebook/pages/migration-runbook/`
- **THEN** the server responds with the full page object including `content`, `entity_mentions`, and `backlinks`

#### Scenario: Update page content with CM6 content sync
- **WHEN** a client sends `PUT /api/notebook/pages/migration-runbook/` with `{"content": "Updated notes with @[person:7|John Smith]"}`
- **THEN** the server updates the content, re-extracts entity mentions, reconciles the join tables, and responds with the updated page object including potentially-rewritten content, which the CM6 editor applies via targeted line-level transactions

#### Scenario: Delete a page
- **WHEN** a client sends `DELETE /api/notebook/pages/migration-runbook/`
- **THEN** the page and its associated `PageEntityMention` and `PageLink` records are deleted
