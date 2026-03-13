## ADDED Requirements

### Requirement: Org-org relationship model with symmetric semantics
The system SHALL provide a `RelationshipOrganizationOrganization` model with two ForeignKey fields (`org_1`, `org_2`) to Organization, an optional ForeignKey to `OrgOrgRelationshipType` (`relationship_type`, null=True, blank=True, on_delete=SET_NULL), a `notes` TextField (blank), and `created_at`/`updated_at` timestamps. The model SHALL enforce `org_1_id < org_2_id` ordering via a CheckConstraint and normalize ordering in the `save()` method, identical to the person-person relationship pattern. The model SHALL have a CheckConstraint preventing self-relationships (`org_1 != org_2`) and a UniqueConstraint on `(org_1, org_2)`.

#### Scenario: Create org-org relationship
- **WHEN** an org-org relationship is created between Organization A (id=1) and Organization B (id=5)
- **THEN** the relationship is persisted with `org_1_id=1` and `org_2_id=5`

#### Scenario: Ordering normalization on save
- **WHEN** an org-org relationship is created with `org_1_id=5` and `org_2_id=1`
- **THEN** the save method normalizes to `org_1_id=1` and `org_2_id=5`

#### Scenario: Self-relationship prevented
- **WHEN** an org-org relationship is attempted with `org_1_id=3` and `org_2_id=3`
- **THEN** the database rejects the record via the CheckConstraint

#### Scenario: Duplicate relationship prevented
- **WHEN** a relationship between org 1 and org 5 already exists and another is attempted
- **THEN** the database rejects the duplicate via the UniqueConstraint

#### Scenario: Org-org relationship with type
- **WHEN** an org-org relationship is created with `relationship_type` set to an `OrgOrgRelationshipType` record
- **THEN** the relationship is persisted with the type FK set

#### Scenario: Org-org relationship without type
- **WHEN** an org-org relationship is created without specifying a relationship type
- **THEN** the relationship is persisted with `relationship_type` set to null

#### Scenario: Deleting an org-org relationship type nullifies references
- **WHEN** an `OrgOrgRelationshipType` is deleted and relationships reference it
- **THEN** those relationships have their `relationship_type` field set to null

### Requirement: OrgOrgRelationshipType lookup table
The system SHALL provide an `OrgOrgRelationshipType` model with a `name` CharField (max 255) for categorizing org-org relationships (e.g., "Partner", "Subsidiary", "Competitor", "Vendor/Client").

#### Scenario: Create org-org relationship type
- **WHEN** an `OrgOrgRelationshipType` is created with name "Partner"
- **THEN** the type record is persisted and available for selection

### Requirement: Org-org relationship CRUD API endpoints
The system SHALL expose JSON API endpoints for org-org relationships: list (GET `/api/relationships/org-org/`), create (POST `/api/relationships/org-org/`), update (PUT `/api/relationships/org-org/{id}/`), and delete (DELETE `/api/relationships/org-org/{id}/`). The create schema SHALL accept `org_1_id`, `org_2_id`, optional `relationship_type_id`, and `notes`. The response schema SHALL include `id`, `org_1_id`, `org_2_id`, `relationship_type_id`, `relationship_type_name`, `notes`, `created_at`, and `updated_at`.

#### Scenario: List org-org relationships
- **WHEN** a client sends GET to `/api/relationships/org-org/`
- **THEN** the server responds with all org-org relationships ordered by id, each including type info

#### Scenario: Create org-org relationship via API
- **WHEN** a client sends POST to `/api/relationships/org-org/` with `org_1_id`, `org_2_id`, and `relationship_type_id`
- **THEN** the server creates the relationship (normalizing order) and responds with status 201

#### Scenario: Create org-org relationship without type
- **WHEN** a client sends POST to `/api/relationships/org-org/` with `org_1_id` and `org_2_id` but no `relationship_type_id`
- **THEN** the server creates the relationship with null type and responds with status 201

#### Scenario: Update org-org relationship
- **WHEN** a client sends PUT to `/api/relationships/org-org/{id}/` with `notes` and/or `relationship_type_id`
- **THEN** the server updates the specified fields and responds with the updated relationship

#### Scenario: Delete org-org relationship
- **WHEN** a client sends DELETE to `/api/relationships/org-org/{id}/`
- **THEN** the server deletes the relationship and responds with status 204

### Requirement: OrgOrgRelationshipType CRUD API endpoints
The system SHALL expose JSON API endpoints for org-org relationship types: list (GET `/api/relationship-types/org-org/`) and create (POST `/api/relationship-types/org-org/`). The schema SHALL follow the same pattern as person-person and org-person relationship types.

#### Scenario: List org-org relationship types
- **WHEN** a client sends GET to `/api/relationship-types/org-org/`
- **THEN** the server responds with all types ordered by name

#### Scenario: Create org-org relationship type via API
- **WHEN** a client sends POST to `/api/relationship-types/org-org/` with `{"name": "Partner"}`
- **THEN** the server creates the type and responds with status 201

### Requirement: Frontend API client for org-org relationships
The system SHALL provide typed API client methods for org-org relationships and types following existing patterns: `api.relationships.orgOrg.getAll()`, `api.relationships.orgOrg.create(payload)`, `api.relationships.orgOrg.update(id, payload)`, `api.relationships.orgOrg.remove(id)`, `api.relationshipTypes.orgOrg.getAll()`, `api.relationshipTypes.orgOrg.create(payload)`.

#### Scenario: Fetch org-org relationships via client
- **WHEN** the client calls `api.relationships.orgOrg.getAll()`
- **THEN** a GET request is sent to `/relationships/org-org/` and the response is typed as `RelationshipOrganizationOrganization[]`

#### Scenario: Create org-org relationship via client
- **WHEN** the client calls `api.relationships.orgOrg.create({ org_1_id, org_2_id, relationship_type_id, notes })`
- **THEN** a POST request is sent to `/relationships/org-org/` and the response is typed as `RelationshipOrganizationOrganization`

#### Scenario: List org-org relationship types via client
- **WHEN** the client calls `api.relationshipTypes.orgOrg.getAll()`
- **THEN** a GET request is sent to `/relationship-types/org-org/` and the response is typed as `OrgOrgRelationshipType[]`

### Requirement: Org-org relationships in the Relationships page UI
The system SHALL display an "Org ↔ Org" tab on the Relationships page with a create form, filter, and list identical in structure to the existing person-person panel. The create form SHALL have an "Organization A" typeahead, a multi-select "Add organization..." typeahead for Organization B, an org-org relationship type typeahead with inline creation, and a notes textarea. The filter SHALL be a typeahead filtering by organization. The list SHALL display each relationship as "Org A ↔ Org B" with inline type editing, notes editing, and delete.

#### Scenario: Create org-org relationship from UI
- **WHEN** the user selects Organization A, adds one or more Organization B entries, optionally sets a type and notes, and submits
- **THEN** relationships are created via the API and appear in the list

#### Scenario: Filter org-org relationships
- **WHEN** the user selects an organization in the filter
- **THEN** only relationships involving that organization are displayed

#### Scenario: Edit org-org relationship type inline
- **WHEN** the user changes the type on an existing org-org relationship via the typeahead
- **THEN** the type is updated via the API

#### Scenario: Edit org-org relationship notes inline
- **WHEN** the user clicks the notes area on an org-org relationship
- **THEN** a textarea appears for editing, saving on blur

#### Scenario: Delete org-org relationship
- **WHEN** the user clicks delete on an org-org relationship and confirms
- **THEN** the relationship is removed via the API and disappears from the list

### Requirement: Org-org edges in the network graph
The network graph API SHALL include org-org relationships as edges with type `organization-organization`, source `organization-{org_1_id}`, and target `organization-{org_2_id}`.

#### Scenario: Graph includes org-org edges
- **WHEN** a client requests `/api/graph/` and org-org relationships exist
- **THEN** the response includes edges with type `organization-organization` connecting the appropriate organization nodes
