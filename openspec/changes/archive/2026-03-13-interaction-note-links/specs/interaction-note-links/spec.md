## ADDED Requirements

### Requirement: InteractionPageLink model for explicit linking
The system SHALL include an `InteractionPageLink` model with fields: `interaction` (ForeignKey to Interaction, on_delete CASCADE), `page` (ForeignKey to Page, on_delete CASCADE), `created_at` (DateTimeField, auto_now_add). The model SHALL have a unique constraint on `(interaction, page)`.

#### Scenario: Create an interaction-page link
- **WHEN** a user adds a page link to an interaction
- **THEN** an `InteractionPageLink` record is created with the interaction and page IDs

#### Scenario: Unique constraint prevents duplicates
- **WHEN** a user attempts to link the same page to the same interaction twice
- **THEN** only one `InteractionPageLink` record exists for that combination

#### Scenario: Cascade delete on interaction deletion
- **WHEN** an interaction is deleted
- **THEN** all associated `InteractionPageLink` records are deleted

#### Scenario: Cascade delete on page deletion
- **WHEN** a notebook page is deleted
- **THEN** all associated `InteractionPageLink` records are deleted

### Requirement: API endpoints for managing interaction-page links
The system SHALL expose the following endpoints:
- `GET /api/interactions/{id}/pages/` — returns all pages linked to the interaction, each with `id`, `title`, `slug`, `page_type`, `date`
- `POST /api/interactions/{id}/pages/` — accepts `{ page_id: int }`, creates link, returns 201 (or 200 if already exists)
- `DELETE /api/interactions/{id}/pages/{page_id}/` — removes the link, returns 204

#### Scenario: List linked pages for an interaction
- **WHEN** a client sends `GET /api/interactions/5/pages/`
- **AND** interaction 5 has 2 linked pages
- **THEN** the response contains an array of 2 page objects with `id`, `title`, `slug`, `page_type`, `date`

#### Scenario: Add a page link to an interaction
- **WHEN** a client sends `POST /api/interactions/5/pages/` with `{ "page_id": 3 }`
- **THEN** the server creates an `InteractionPageLink` and responds with 201

#### Scenario: Add duplicate link returns 200
- **WHEN** a client sends `POST /api/interactions/5/pages/` with `{ "page_id": 3 }`
- **AND** the link already exists
- **THEN** the server responds with 200

#### Scenario: Remove a page link from an interaction
- **WHEN** a client sends `DELETE /api/interactions/5/pages/3/`
- **THEN** the `InteractionPageLink` is deleted and the server responds with 204

### Requirement: Reverse API endpoint for page-to-interaction links
The system SHALL expose `GET /api/notebook/pages/{slug}/interactions/` that returns all interactions explicitly linked to the page. Each entry SHALL include `id`, `interaction_type` (with `id` and `name`), `date`, `person_names` (list of linked people's names), and `notes` (truncated to 100 characters).

#### Scenario: List interactions linked to a page
- **WHEN** a client sends `GET /api/notebook/pages/meeting-prep/interactions/`
- **AND** the page has 2 linked interactions
- **THEN** the response contains 2 interaction summary objects

#### Scenario: Page with no linked interactions
- **WHEN** a client sends `GET /api/notebook/pages/random-page/interactions/`
- **AND** the page has no linked interactions
- **THEN** the response is an empty array

### Requirement: Interaction detail panel shows linked notebook pages
The interaction detail panel SHALL display a "Linked Notes" section below the existing "Linked Tasks" section. This section SHALL use a typeahead selector to search and add notebook pages by title. Each linked page SHALL display its title and page type badge. Users SHALL be able to remove links via a remove button on each entry.

#### Scenario: View linked notes on interaction
- **WHEN** the user selects an interaction that has 2 linked pages
- **THEN** the "Linked Notes" section shows 2 entries with page titles

#### Scenario: Add a note link from interaction detail
- **WHEN** the user uses the typeahead in the "Linked Notes" section to select a page
- **THEN** the page is added to the linked list and persisted via API

#### Scenario: Remove a note link from interaction detail
- **WHEN** the user clicks the remove button on a linked note
- **THEN** the note is removed from the linked list and the link is deleted via API

### Requirement: Notebook page shows linked interactions
When viewing a notebook page, the editor area SHALL display a "Linked Interactions" section (below existing backlinks) showing interactions linked to this page via explicit `InteractionPageLink` records. Each entry SHALL show the interaction type, date, and people involved. Clicking an entry SHALL navigate to the CRM interactions page with that interaction selected.

#### Scenario: View linked interactions on notebook page
- **WHEN** the user views a notebook page that has 3 linked interactions
- **THEN** the "Linked Interactions" section shows 3 entries with type, date, and people

#### Scenario: Notebook page with no linked interactions
- **WHEN** the user views a page with no linked interactions
- **THEN** the "Linked Interactions" section is not displayed

#### Scenario: Click linked interaction navigates to CRM
- **WHEN** the user clicks a linked interaction entry
- **THEN** the browser navigates to `/crm/interactions?selected={id}`
