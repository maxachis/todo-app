## ADDED Requirements

### Requirement: Network API endpoints for org-org relationships
The system SHALL expose JSON API endpoints to create, read, update, and delete org-org relationship records. The create schema SHALL accept `org_1_id`, `org_2_id`, optional `relationship_type_id`, and `notes`. The update schema SHALL accept optional `notes` and `relationship_type_id`. The response schema SHALL include `id`, `org_1_id`, `org_2_id`, `relationship_type_id`, `relationship_type_name`, `notes`, `created_at`, and `updated_at`.

#### Scenario: Create org-org relationship with type
- **WHEN** a client sends POST to `/api/relationships/org-org/` with `org_1_id`, `org_2_id`, and `relationship_type_id`
- **THEN** the server creates the relationship with the specified type and responds with status 201 including `relationship_type_id` and `relationship_type_name`

#### Scenario: Create org-org relationship without type
- **WHEN** a client sends POST to `/api/relationships/org-org/` with `org_1_id` and `org_2_id` but no `relationship_type_id`
- **THEN** the server creates the relationship with null type and responds with status 201

#### Scenario: Update org-org relationship type
- **WHEN** a client sends PUT to `/api/relationships/org-org/{id}/` with `relationship_type_id`
- **THEN** the server updates the relationship type and responds with the updated relationship object

#### Scenario: Get org-org relationships includes type info
- **WHEN** a client sends GET to `/api/relationships/org-org/`
- **THEN** each relationship object includes `relationship_type_id` and `relationship_type_name`

### Requirement: Network API endpoints for org-org relationship types
The system SHALL expose JSON API endpoints to list and create org-org relationship types, following the same pattern as person-person and org-person relationship type endpoints.

#### Scenario: List org-org relationship types
- **WHEN** a client sends GET to `/api/relationship-types/org-org/`
- **THEN** the server responds with all org-org relationship types ordered by name

#### Scenario: Create org-org relationship type
- **WHEN** a client sends POST to `/api/relationship-types/org-org/` with `{"name": "Partner"}`
- **THEN** the server creates the type and responds with status 201

### Requirement: Graph API includes org-org edges
The graph API endpoint SHALL include org-org relationships as edges with type `organization-organization`.

#### Scenario: Graph data includes org-org edges
- **WHEN** a client sends GET to `/api/graph/` and org-org relationships exist
- **THEN** the response edges array includes entries with type `organization-organization`, source `organization-{org_1_id}`, and target `organization-{org_2_id}`

## MODIFIED Requirements

### Requirement: Network API endpoints for interactions and relationships
The system SHALL expose JSON API endpoints to create, read, update, and delete interactions and relationship records. The interaction create schema SHALL accept a `person_ids` field (list of integers, at least one required) instead of a single `person_id`. The interaction update schema SHALL accept an optional `person_ids` field that replaces the full set when provided. The interaction response schema SHALL include a `person_ids` field (list of integers) instead of `person_id`. The relationship create schemas SHALL accept an optional `relationship_type_id` field (integer, nullable). The relationship update schemas SHALL accept an optional `relationship_type_id` field (integer, nullable). The relationship response schemas SHALL include `relationship_type_id` (integer or null) and `relationship_type_name` (string or null) fields. The org-org relationship create schema SHALL accept `org_1_id`, `org_2_id`, optional `relationship_type_id`, and `notes`. The org-org relationship response schema SHALL include `org_1_id`, `org_2_id`, `relationship_type_id`, `relationship_type_name`, `notes`, `created_at`, and `updated_at`.

#### Scenario: Create an interaction
- **WHEN** a client sends POST to `/api/interactions/` with `person_ids`, type, date, and notes
- **THEN** the server creates the interaction, associates all specified people, and responds with status 201 and the interaction object including `person_ids`

#### Scenario: Update an interaction's people
- **WHEN** a client sends PUT to `/api/interactions/{id}/` with `person_ids: [2, 3]`
- **THEN** the server replaces the interaction's people set and responds with the updated interaction object

#### Scenario: Get interaction includes person_ids
- **WHEN** a client sends GET to `/api/interactions/{id}/`
- **THEN** the response includes `person_ids` as a list of associated person IDs

#### Scenario: Create person-person relationship with type
- **WHEN** a client sends POST to `/api/relationships/people/` with `person_1_id`, `person_2_id`, and `relationship_type_id`
- **THEN** the server creates the relationship with the specified type and responds with status 201 including `relationship_type_id` and `relationship_type_name`

#### Scenario: Create person-person relationship without type
- **WHEN** a client sends POST to `/api/relationships/people/` with `person_1_id` and `person_2_id` but no `relationship_type_id`
- **THEN** the server creates the relationship with null type and responds with status 201

#### Scenario: Update person-person relationship type
- **WHEN** a client sends PUT to `/api/relationships/people/{id}/` with `relationship_type_id`
- **THEN** the server updates the relationship type and responds with the updated relationship object

#### Scenario: Clear person-person relationship type
- **WHEN** a client sends PUT to `/api/relationships/people/{id}/` with `relationship_type_id: null`
- **THEN** the server sets the relationship type to null

#### Scenario: Get person-person relationships includes type info
- **WHEN** a client sends GET to `/api/relationships/people/`
- **THEN** each relationship object includes `relationship_type_id` and `relationship_type_name`

#### Scenario: Create org-person relationship with type
- **WHEN** a client sends POST to `/api/relationships/organizations/` with `organization_id`, `person_id`, and `relationship_type_id`
- **THEN** the server creates the relationship with the specified type and responds with status 201 including `relationship_type_id` and `relationship_type_name`

#### Scenario: Update org-person relationship type
- **WHEN** a client sends PUT to `/api/relationships/organizations/{id}/` with `relationship_type_id`
- **THEN** the server updates the relationship type and responds with the updated relationship object

#### Scenario: Get org-person relationships includes type info
- **WHEN** a client sends GET to `/api/relationships/organizations/`
- **THEN** each relationship object includes `relationship_type_id` and `relationship_type_name`

#### Scenario: Create org-org relationship with type
- **WHEN** a client sends POST to `/api/relationships/org-org/` with `org_1_id`, `org_2_id`, and `relationship_type_id`
- **THEN** the server creates the relationship with the specified type and responds with status 201 including `relationship_type_id` and `relationship_type_name`

#### Scenario: Create org-org relationship without type
- **WHEN** a client sends POST to `/api/relationships/org-org/` with `org_1_id` and `org_2_id` but no `relationship_type_id`
- **THEN** the server creates the relationship with null type and responds with status 201

#### Scenario: Get org-org relationships includes type info
- **WHEN** a client sends GET to `/api/relationships/org-org/`
- **THEN** each relationship object includes `relationship_type_id` and `relationship_type_name`
