## MODIFIED Requirements

### Requirement: Network API endpoints for interactions and relationships
The system SHALL expose JSON API endpoints to create, read, update, and delete interactions and relationship records. The interaction create schema SHALL accept a `person_ids` field (list of integers, at least one required) instead of a single `person_id`. The interaction update schema SHALL accept an optional `person_ids` field that replaces the full set when provided. The interaction response schema SHALL include a `person_ids` field (list of integers) instead of `person_id`. The relationship create schemas SHALL accept an optional `relationship_type_id` field (integer, nullable). The relationship update schemas SHALL accept an optional `relationship_type_id` field (integer, nullable). The relationship response schemas SHALL include `relationship_type_id` (integer or null) and `relationship_type_name` (string or null) fields.

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
