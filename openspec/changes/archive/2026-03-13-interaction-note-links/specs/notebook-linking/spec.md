## MODIFIED Requirements

### Requirement: PageEntityMention model for entity references
The system SHALL include a `PageEntityMention` model with fields: `page` (ForeignKey to Page, on_delete CASCADE), `entity_type` (CharField, max 20, choices: `person`, `organization`, `task`, `project`, `interaction`), `entity_id` (PositiveIntegerField). The model SHALL have a unique constraint on `(page, entity_type, entity_id)`.

#### Scenario: Store a person mention
- **WHEN** a page's content includes `@[person:7|John Smith]`
- **THEN** a `PageEntityMention` record exists with `page=<page>`, `entity_type="person"`, `entity_id=7`

#### Scenario: Store a task mention
- **WHEN** a page's content includes `[[task:189|Deploy fix]]`
- **THEN** a `PageEntityMention` record exists with `entity_type="task"`, `entity_id=189`

#### Scenario: Store an interaction mention
- **WHEN** a page's content includes `[[interaction:42|Meeting with John (2026-03-13)]]`
- **THEN** a `PageEntityMention` record exists with `entity_type="interaction"`, `entity_id=42`

#### Scenario: Unique constraint prevents duplicates
- **WHEN** a page mentions the same person twice in content
- **THEN** only one `PageEntityMention` record exists for that (page, person, id) combination

#### Scenario: Cascade delete on page deletion
- **WHEN** a page is deleted
- **THEN** all associated `PageEntityMention` records are deleted

#### Scenario: Query interaction backlinks
- **WHEN** a client sends `GET /api/notebook/mentions/interaction/42/`
- **THEN** the server responds with all pages that contain a mention of interaction 42
