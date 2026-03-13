## MODIFIED Requirements

### Requirement: Page CRUD API endpoints
The system SHALL expose JSON API endpoints under `/api/notebook/` for page operations: `GET /api/notebook/pages/` (list all pages, with optional `search` query param filtering by title substring, optional `page_type` query param, and optional `ordering` query param), `POST /api/notebook/pages/` (create), `GET /api/notebook/pages/{slug}/` (retrieve by slug), `PUT /api/notebook/pages/{slug}/` (update), `DELETE /api/notebook/pages/{slug}/` (delete). The `ordering` query param SHALL accept the values `-updated_at` (default), `-created_at`, and `title`. Any other value SHALL be ignored and the default ordering SHALL be used. The create endpoint SHALL accept `title`, `content` (optional), `page_type` (optional, default `wiki`), and `date` (required if `page_type` is `daily`). The update endpoint SHALL accept `title` and `content`. The update endpoint SHALL return the potentially-rewritten content (from server-side checkbox-to-task processing) in the response, and the frontend editor SHALL apply returned content differences via targeted CM6 transactions that preserve cursor position, rather than via textarea value binding.

#### Scenario: List pages with default ordering
- **WHEN** a client sends `GET /api/notebook/pages/` without an `ordering` parameter
- **THEN** the server responds with all pages ordered by most recently updated first

#### Scenario: List pages ordered by creation date
- **WHEN** a client sends `GET /api/notebook/pages/?ordering=-created_at`
- **THEN** the server responds with all pages ordered by most recently created first

#### Scenario: List pages ordered by title
- **WHEN** a client sends `GET /api/notebook/pages/?ordering=title`
- **THEN** the server responds with all pages ordered alphabetically by title (A-Z)

#### Scenario: Invalid ordering value falls back to default
- **WHEN** a client sends `GET /api/notebook/pages/?ordering=invalid`
- **THEN** the server responds with all pages ordered by most recently updated first (default)
