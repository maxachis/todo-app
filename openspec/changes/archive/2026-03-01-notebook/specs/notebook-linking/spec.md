## ADDED Requirements

### Requirement: PageEntityMention model for entity references
The system SHALL include a `PageEntityMention` model with fields: `page` (ForeignKey to Page, on_delete CASCADE), `entity_type` (CharField, max 20, choices: `person`, `organization`, `task`, `project`), `entity_id` (PositiveIntegerField). The model SHALL have a unique constraint on `(page, entity_type, entity_id)`.

#### Scenario: Store a person mention
- **WHEN** a page's content includes `@[person:7|John Smith]`
- **THEN** a `PageEntityMention` record exists with `page=<page>`, `entity_type="person"`, `entity_id=7`

#### Scenario: Store a task mention
- **WHEN** a page's content includes `[[task:189|Deploy fix]]`
- **THEN** a `PageEntityMention` record exists with `entity_type="task"`, `entity_id=189`

#### Scenario: Unique constraint prevents duplicates
- **WHEN** a page mentions the same person twice in content
- **THEN** only one `PageEntityMention` record exists for that (page, person, id) combination

#### Scenario: Cascade delete on page deletion
- **WHEN** a page is deleted
- **THEN** all associated `PageEntityMention` records are deleted

### Requirement: PageLink model for page-to-page references
The system SHALL include a `PageLink` model with fields: `source_page` (ForeignKey to Page, on_delete CASCADE, related_name `outgoing_links`), `target_page` (ForeignKey to Page, on_delete CASCADE, related_name `incoming_links`). The model SHALL have a unique constraint on `(source_page, target_page)`.

#### Scenario: Store a page-to-page link
- **WHEN** page A's content includes `[[page:B_id|Page B Title]]`
- **THEN** a `PageLink` record exists with `source_page=A`, `target_page=B`

#### Scenario: Bidirectional query
- **WHEN** page A links to page B via `PageLink`
- **THEN** querying page B's `incoming_links` returns page A

#### Scenario: Cascade delete on source page deletion
- **WHEN** a page that is the source of a `PageLink` is deleted
- **THEN** the `PageLink` record is deleted

#### Scenario: Cascade delete on target page deletion
- **WHEN** a page that is the target of a `PageLink` is deleted
- **THEN** the `PageLink` record is deleted

### Requirement: Backlinks displayed on notebook pages
The page detail API response SHALL include a `backlinks` array containing pages that link to this page (via `PageLink.incoming_links`). Each backlink entry SHALL include `id`, `title`, `slug`, `page_type`, `date`, and `snippet` (first 150 characters of the linking page's content). The editor area SHALL display a "Backlinks" section below the content textarea listing these linking pages.

#### Scenario: Page with backlinks
- **WHEN** the user views a page that is referenced by 3 other pages
- **THEN** the "Backlinks" section shows 3 entries with title, type badge, and content snippet

#### Scenario: Page with no backlinks
- **WHEN** the user views a page with no incoming links
- **THEN** the "Backlinks" section is not displayed

#### Scenario: Click backlink navigates to source page
- **WHEN** the user clicks a backlink entry
- **THEN** the editor navigates to the source page

### Requirement: Entity backlinks API endpoint
The system SHALL expose `GET /api/notebook/mentions/{entity_type}/{entity_id}/` that returns all pages mentioning the specified entity. Each entry SHALL include `id`, `title`, `slug`, `page_type`, `date`, and `snippet` (first 150 characters of the page's content). Results SHALL be ordered by `-updated_at`.

#### Scenario: Query person backlinks
- **WHEN** a client sends `GET /api/notebook/mentions/person/7/`
- **THEN** the server responds with all pages that contain a mention of person 7, ordered by most recently updated

#### Scenario: Query task backlinks
- **WHEN** a client sends `GET /api/notebook/mentions/task/189/`
- **THEN** the server responds with all pages that contain a mention of task 189

#### Scenario: Entity with no mentions
- **WHEN** a client sends `GET /api/notebook/mentions/person/999/`
- **AND** no pages mention person 999
- **THEN** the server responds with an empty array
