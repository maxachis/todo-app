# Notebook Core

## Purpose

Backend models and API for the notebook feature, supporting daily and wiki pages with content storage, mention parsing, and CRUD operations.

## Requirements

### Requirement: Page model with daily and wiki types
The system SHALL include a `Page` model in a `notebook` Django app with the following fields: `title` (CharField, max 255), `slug` (SlugField, max 255, unique), `content` (TextField, blank), `page_type` (CharField, max 10, choices: `daily` or `wiki`, default `wiki`), `date` (DateField, nullable, unique where not null — set for daily pages, null for wiki pages), `created_at` (DateTimeField, auto_now_add), `updated_at` (DateTimeField, auto_now). The slug SHALL be auto-generated from the title on create if not provided. For daily pages, the slug SHALL be the ISO date string (e.g., `2026-02-28`).

#### Scenario: Create a wiki page
- **WHEN** a page is created with `page_type: "wiki"` and `title: "Migration Runbook"`
- **THEN** the page is persisted with `slug` auto-generated as `migration-runbook`, `date` as null, and `page_type` as `wiki`

#### Scenario: Create a daily page
- **WHEN** a page is created with `page_type: "daily"` and `date: "2026-02-28"`
- **THEN** the page is persisted with `title` set to `"2026-02-28"`, `slug` set to `"2026-02-28"`, and `page_type` as `daily`

#### Scenario: Duplicate daily page date rejected
- **WHEN** a page is created with `page_type: "daily"` and `date: "2026-02-28"` and a daily page for that date already exists
- **THEN** the creation fails with a uniqueness constraint error

#### Scenario: Slug uniqueness enforced
- **WHEN** a page is created with a title that generates a slug already in use
- **THEN** the system appends a numeric suffix to make the slug unique (e.g., `migration-runbook-2`)

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

### Requirement: Mention parsing extracts entity references on save
The system SHALL parse page content on every create and update to extract entity references. The parser SHALL recognize two patterns: `@[person:ID|Label]` for people and `[[type:ID|Label]]` for pages, tasks, organizations, and projects (where type is one of `page`, `task`, `org`, `project`). Additionally, the parser SHALL detect unchecked checkbox lines matching `- [ ] <text>` where `<text>` does not contain `[[task:` — for each, it SHALL create a task in the system Inbox section and rewrite the line to `- [ ] [[task:ID|Title]]`. **The parser SHALL also detect `@new[Name](optional notes)` patterns and create ContactDraft records for each new occurrence (where no draft with the same name and source page exists).** After all checkbox and contact-draft processing, the system SHALL reconcile the `PageEntityMention` and `PageLink` join tables — adding new references, removing stale ones — so the tables always reflect the current content.

#### Scenario: Content with people and task mentions
- **WHEN** a page is saved with content `"Met with @[person:7|John Smith] about [[task:189|Deploy fix]]"`
- **THEN** the system creates a `PageEntityMention` for (page, person, 7) and (page, task, 189)

#### Scenario: Content with page link
- **WHEN** a page is saved with content `"See [[page:12|Migration Runbook]] for details"`
- **THEN** the system creates a `PageLink` from this page to page 12

#### Scenario: Mention removed from content
- **WHEN** a page previously mentioned person 7 and is updated with content that no longer contains `@[person:7|...]`
- **THEN** the `PageEntityMention` for (page, person, 7) is deleted

#### Scenario: Content with no mentions
- **WHEN** a page is saved with content containing no mention syntax
- **THEN** no `PageEntityMention` or `PageLink` records are created (or existing ones are cleared)

#### Scenario: Duplicate mentions in content
- **WHEN** a page mentions `@[person:7|John Smith]` twice in the content
- **THEN** only one `PageEntityMention` record exists for (page, person, 7)

#### Scenario: Checkbox line creates task and rewrites content
- **WHEN** a page is saved with content containing `- [ ] Review contract`
- **THEN** a task titled "Review contract" is created in the Inbox section, the line is rewritten to `- [ ] [[task:ID|Review contract]]`, and a `PageEntityMention` for (page, task, ID) is created

#### Scenario: @new pattern creates contact draft during save
- **WHEN** a page is saved with content `"Had coffee with @new[Jane Smith](works at Stripe)"`
- **THEN** the system creates a ContactDraft with `name="Jane Smith"`, `quick_notes="works at Stripe"`, and `source_page` set to this page, and the page content is NOT rewritten

#### Scenario: @new and checkbox patterns coexist
- **WHEN** a page is saved with content containing both `- [ ] Follow up with Jane` and `@new[Jane Smith](Stripe)`
- **THEN** a task is created from the checkbox line (content rewritten), a ContactDraft is created from the @new pattern (content NOT rewritten), and mention reconciliation runs on the final content
