## ADDED Requirements

### Requirement: Person-person relationship type model
The system SHALL include a `PersonPersonRelationshipType` model with a `name` field (CharField, max 255). The model SHALL follow the same pattern as `OrgType` and `InteractionType`.

#### Scenario: Create a person-person relationship type
- **WHEN** a `PersonPersonRelationshipType` is created with name "Coworker"
- **THEN** the record is persisted with the given name

#### Scenario: Multiple person-person relationship types exist
- **WHEN** relationship types "Coworker", "Friend", and "Mentor" are created
- **THEN** all three are independently stored and retrievable

### Requirement: Org-person relationship type model
The system SHALL include an `OrgPersonRelationshipType` model with a `name` field (CharField, max 255). The model SHALL follow the same pattern as `OrgType` and `InteractionType`.

#### Scenario: Create an org-person relationship type
- **WHEN** an `OrgPersonRelationshipType` is created with name "CEO"
- **THEN** the record is persisted with the given name

### Requirement: Person-person relationship type CRUD API
The system SHALL expose JSON API endpoints to list, create, update, and delete person-person relationship types at `/api/relationship-types/people/`. The create endpoint SHALL strip whitespace and reject blank names with status 422. The list endpoint SHALL order results by name, then id.

#### Scenario: List person-person relationship types
- **WHEN** a client sends GET to `/api/relationship-types/people/`
- **THEN** the server responds with all `PersonPersonRelationshipType` records ordered by name, id

#### Scenario: Create person-person relationship type
- **WHEN** a client sends POST to `/api/relationship-types/people/` with `{"name": "Coworker"}`
- **THEN** the server creates the type and responds with status 201 and the type object

#### Scenario: Reject blank person-person relationship type name
- **WHEN** a client sends POST to `/api/relationship-types/people/` with `{"name": "  "}`
- **THEN** the server responds with status 422

#### Scenario: Update person-person relationship type
- **WHEN** a client sends PUT to `/api/relationship-types/people/{id}/` with `{"name": "Colleague"}`
- **THEN** the server updates the type name and responds with the updated type object

#### Scenario: Delete person-person relationship type
- **WHEN** a client sends DELETE to `/api/relationship-types/people/{id}/`
- **THEN** the server deletes the type and responds with status 204

### Requirement: Org-person relationship type CRUD API
The system SHALL expose JSON API endpoints to list, create, update, and delete org-person relationship types at `/api/relationship-types/organizations/`. The create endpoint SHALL strip whitespace and reject blank names with status 422. The list endpoint SHALL order results by name, then id.

#### Scenario: List org-person relationship types
- **WHEN** a client sends GET to `/api/relationship-types/organizations/`
- **THEN** the server responds with all `OrgPersonRelationshipType` records ordered by name, id

#### Scenario: Create org-person relationship type
- **WHEN** a client sends POST to `/api/relationship-types/organizations/` with `{"name": "CEO"}`
- **THEN** the server creates the type and responds with status 201 and the type object

#### Scenario: Reject blank org-person relationship type name
- **WHEN** a client sends POST to `/api/relationship-types/organizations/` with `{"name": ""}`
- **THEN** the server responds with status 422

#### Scenario: Update org-person relationship type
- **WHEN** a client sends PUT to `/api/relationship-types/organizations/{id}/` with `{"name": "CTO"}`
- **THEN** the server updates the type name and responds with the updated type object

#### Scenario: Delete org-person relationship type
- **WHEN** a client sends DELETE to `/api/relationship-types/organizations/{id}/`
- **THEN** the server deletes the type and responds with status 204
