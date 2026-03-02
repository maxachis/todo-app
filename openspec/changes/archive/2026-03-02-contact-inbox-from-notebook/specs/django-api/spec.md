## ADDED Requirements

### Requirement: ContactDraft API endpoints
The system SHALL provide API endpoints under `/api/network/contact-drafts/` for managing contact drafts. Endpoints include: list pending (`GET /`), retrieve (`GET /:id/`), delete (`DELETE /:id/`), dismiss (`POST /:id/dismiss/`), promote to person (`POST /:id/promote/person/`), promote to org (`POST /:id/promote/org/`), link to existing (`POST /:id/link/`), and match hints (`GET /:id/matches/`). All promotion and link endpoints SHALL trigger a notebook content rewrite across all pages and auto-dismiss sibling drafts with the same name.

#### Scenario: List pending contact drafts
- **WHEN** a client sends `GET /api/network/contact-drafts/`
- **THEN** the server responds with a JSON array of pending drafts (not promoted, not dismissed), ordered by `-created_at`

#### Scenario: Promote to person
- **WHEN** a client sends `POST /api/network/contact-drafts/:id/promote/person/` with `{"first_name": "Jane", "last_name": "Smith"}`
- **THEN** a Person is created, `promoted_to_person` is set, notebook pages are rewritten, and sibling drafts are auto-dismissed

#### Scenario: Promote to organization
- **WHEN** a client sends `POST /api/network/contact-drafts/:id/promote/org/` with `{"name": "Acme Corp", "org_type_id": 1}`
- **THEN** an Organization is created, `promoted_to_org` is set, notebook pages are rewritten, and sibling drafts are auto-dismissed

#### Scenario: Link to existing person
- **WHEN** a client sends `POST /api/network/contact-drafts/:id/link/` with `{"person_id": 42}`
- **THEN** `promoted_to_person` is set to Person 42, quick notes are appended to the person's notes, notebook pages are rewritten, and sibling drafts are auto-dismissed

#### Scenario: Link to existing organization
- **WHEN** a client sends `POST /api/network/contact-drafts/:id/link/` with `{"org_id": 5}`
- **THEN** `promoted_to_org` is set to Organization 5, quick notes are appended to the org's notes, notebook pages are rewritten, and sibling drafts are auto-dismissed

#### Scenario: Match hints return similar records
- **WHEN** a client sends `GET /api/network/contact-drafts/:id/matches/`
- **THEN** the server responds with `{"people": [...], "organizations": [...]}` containing records whose names match the draft's name

#### Scenario: Dismiss a draft
- **WHEN** a client sends `POST /api/network/contact-drafts/:id/dismiss/`
- **THEN** the draft is marked as dismissed and no longer appears in the pending list
