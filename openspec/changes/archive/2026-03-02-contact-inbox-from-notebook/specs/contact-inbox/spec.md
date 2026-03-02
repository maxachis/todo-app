## ADDED Requirements

### Requirement: ContactDraft model for staging quick-captured contacts
The system SHALL include a `ContactDraft` model in the `network` app with the following fields: `name` (CharField, max 255), `quick_notes` (TextField, blank), `source_page` (FK → Page, nullable, SET_NULL on delete), `promoted_to_person` (FK → Person, nullable, SET_NULL on delete), `promoted_to_org` (FK → Organization, nullable, SET_NULL on delete), `dismissed` (BooleanField, default False), `created_at` (DateTimeField, auto_now_add). At most one of `promoted_to_person` or `promoted_to_org` may be non-null. A draft is "pending" when both promotion FKs are null and `dismissed` is False.

#### Scenario: Draft created from notebook save
- **WHEN** a notebook page is saved containing `@new[Jane Smith](works at Stripe)`
- **THEN** a ContactDraft is created with `name="Jane Smith"`, `quick_notes="works at Stripe"`, and `source_page` set to the saved page

#### Scenario: Draft created without notes
- **WHEN** a notebook page is saved containing `@new[Bob Chen]`
- **THEN** a ContactDraft is created with `name="Bob Chen"`, `quick_notes=""`, and `source_page` set to the saved page

#### Scenario: Draft starts as pending
- **WHEN** a ContactDraft is created
- **THEN** `promoted_to_person` is null, `promoted_to_org` is null, and `dismissed` is False

### Requirement: ContactDraft CRUD API endpoints
The system SHALL provide API endpoints under `/api/network/contact-drafts/` for managing drafts: `GET /` (list pending drafts, ordered by `-created_at`), `GET /:id/` (retrieve single draft), `DELETE /:id/` (hard delete).

#### Scenario: List pending drafts
- **WHEN** a client sends `GET /api/network/contact-drafts/`
- **THEN** the server responds with a JSON array of drafts where `promoted_to_person` is null, `promoted_to_org` is null, and `dismissed` is False, ordered by most recently created first, each including `id`, `name`, `quick_notes`, `source_page_id`, `source_page_slug`, `source_page_title`, `dismissed`, `created_at`

#### Scenario: Retrieve a draft
- **WHEN** a client sends `GET /api/network/contact-drafts/:id/`
- **THEN** the server responds with the full draft object

#### Scenario: Delete a draft
- **WHEN** a client sends `DELETE /api/network/contact-drafts/:id/`
- **THEN** the draft is deleted and the server responds with 204

### Requirement: Dismiss a contact draft
The system SHALL provide a `POST /api/network/contact-drafts/:id/dismiss/` endpoint that sets `dismissed=True` on the draft. Dismissed drafts SHALL NOT appear in the pending list.

#### Scenario: Dismiss a draft
- **WHEN** a client sends `POST /api/network/contact-drafts/:id/dismiss/`
- **THEN** the draft's `dismissed` field is set to True and the server responds with the updated draft

#### Scenario: Dismissed draft excluded from list
- **WHEN** a draft has been dismissed
- **THEN** it does not appear in the `GET /api/network/contact-drafts/` response

### Requirement: Promote a contact draft to Person
The system SHALL provide a `POST /api/network/contact-drafts/:id/promote/person/` endpoint that accepts Person creation fields (`first_name`, `last_name`, and optional `middle_name`, `email`, `linkedin_url`, `follow_up_cadence_days`, `notes`). The endpoint SHALL create a Person record, set `promoted_to_person` on the draft, and trigger a notebook content rewrite replacing all `@new[Name](...)` occurrences across all pages with `@[person:ID|Name]`. The quick notes from the draft SHALL be used as the Person's `notes` field if no explicit `notes` is provided in the payload.

#### Scenario: Promote draft to new person
- **WHEN** a client sends `POST /api/network/contact-drafts/:id/promote/person/` with `{"first_name": "Jane", "last_name": "Smith"}`
- **THEN** a Person is created, `promoted_to_person` is set on the draft, and all pages containing `@new[Jane Smith]` are rewritten to `@[person:ID|Jane Smith]`

#### Scenario: Quick notes migrate to person notes
- **WHEN** a draft with `quick_notes="works at Stripe"` is promoted to a Person without explicit `notes` in the payload
- **THEN** the created Person has `notes="works at Stripe"`

#### Scenario: Explicit notes override quick notes
- **WHEN** a draft is promoted with `{"first_name": "Jane", "last_name": "Smith", "notes": "Key contact for Stripe deal"}`
- **THEN** the Person is created with `notes="Key contact for Stripe deal"` regardless of quick_notes

### Requirement: Promote a contact draft to Organization
The system SHALL provide a `POST /api/network/contact-drafts/:id/promote/org/` endpoint that accepts Organization creation fields (`name`, `org_type_id`, and optional `notes`). The endpoint SHALL create an Organization record, set `promoted_to_org` on the draft, and trigger a notebook content rewrite replacing all `@new[Name](...)` occurrences across all pages with `[[org:ID|Name]]`.

#### Scenario: Promote draft to new organization
- **WHEN** a client sends `POST /api/network/contact-drafts/:id/promote/org/` with `{"name": "Acme Corp", "org_type_id": 1}`
- **THEN** an Organization is created, `promoted_to_org` is set on the draft, and all pages containing `@new[Acme Corp]` are rewritten to `[[org:ID|Acme Corp]]`

#### Scenario: Quick notes migrate to org notes
- **WHEN** a draft with `quick_notes="potential Q3 partner"` is promoted to an Organization without explicit `notes`
- **THEN** the created Organization has `notes="potential Q3 partner"`

### Requirement: Link a contact draft to an existing record
The system SHALL provide a `POST /api/network/contact-drafts/:id/link/` endpoint that accepts `{"person_id": ID}` or `{"org_id": ID}`. The endpoint SHALL set the appropriate promotion FK, append the draft's `quick_notes` to the existing record's `notes` field (separated by `\n---\n` with a date and source page reference if notes already exist), and trigger the notebook content rewrite.

#### Scenario: Link draft to existing person
- **WHEN** a client sends `POST /api/network/contact-drafts/:id/link/` with `{"person_id": 42}`
- **THEN** `promoted_to_person` is set to Person 42, quick notes are appended to Person 42's notes, and notebook pages are rewritten

#### Scenario: Link draft to existing org
- **WHEN** a client sends `POST /api/network/contact-drafts/:id/link/` with `{"org_id": 5}`
- **THEN** `promoted_to_org` is set to Organization 5, quick notes are appended to Organization 5's notes, and notebook pages are rewritten

#### Scenario: Notes appended with separator
- **WHEN** a draft with `quick_notes="met at conference"` is linked to Person 42 who already has `notes="Sales lead from 2025"`
- **THEN** Person 42's notes become `"Sales lead from 2025\n---\nmet at conference"` (with source page context)

### Requirement: Match hints for existing records
The system SHALL provide a `GET /api/network/contact-drafts/:id/matches/` endpoint that returns potential matches from existing Person and Organization records based on the draft's name. For people, the system SHALL split the name on whitespace (first token → first_name, last token → last_name) and search with case-insensitive containment. For organizations, the system SHALL search `name__icontains` on the full draft name.

#### Scenario: Exact person match found
- **WHEN** a draft has `name="Jane Smith"` and a Person with `first_name="Jane"`, `last_name="Smith"` exists
- **THEN** the matches endpoint returns that Person in the `people` array

#### Scenario: Partial person match found
- **WHEN** a draft has `name="Jane Smith"` and a Person with `first_name="Janet"`, `last_name="Smith"` exists
- **THEN** the matches endpoint returns that Person in the `people` array (containment match on last name)

#### Scenario: Organization match found
- **WHEN** a draft has `name="Acme Corp"` and an Organization named "Acme Corporation" exists
- **THEN** the matches endpoint returns that Organization in the `organizations` array

#### Scenario: No matches
- **WHEN** a draft has `name="Completely New Name"` and no similar records exist
- **THEN** the matches endpoint returns empty `people` and `organizations` arrays

### Requirement: Auto-dismiss related drafts after promotion
When a draft is promoted or linked, the system SHALL search for other pending drafts with the same `name` (case-insensitive) and auto-dismiss them, since their notebook references have been rewritten by the promotion.

#### Scenario: Sibling drafts auto-dismissed
- **WHEN** two drafts exist with `name="Jane Smith"` (from different pages) and one is promoted to Person
- **THEN** the other draft is automatically set to `dismissed=True`
