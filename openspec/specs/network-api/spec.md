### Requirement: Network API endpoints for people
The system SHALL expose JSON API endpoints to create, read, update, and delete people under the `/api/` prefix. The create and update schemas SHALL accept optional `email` and `linkedin_url` fields. The response schema SHALL include `email`, `linkedin_url`, `last_interaction_date`, `last_interaction_type`, and `tags` fields. The `tags` field SHALL be an array of objects with `id` and `name`. The `last_interaction_date` SHALL be the date of the most recent Interaction record where the person is in the interaction's `people` M2M set (null if no interactions). The `last_interaction_type` SHALL be the name of the interaction type of the most recent such Interaction record (null if no interactions). The people list endpoint SHALL accept an optional `tag` query parameter to filter results to only people with the specified tag.

#### Scenario: Create a person
- **WHEN** a client sends POST to `/api/people/` with person fields
- **THEN** the server creates the person and responds with status 201 and the person object

#### Scenario: Create a person with contact fields
- **WHEN** a client sends POST to `/api/people/` with `email` and `linkedin_url` in the payload
- **THEN** the server creates the person with those contact fields and includes them in the 201 response

#### Scenario: Update a person's contact fields
- **WHEN** a client sends PUT to `/api/people/{id}/` with `email` or `linkedin_url`
- **THEN** the server updates the specified contact fields and returns the updated person object

#### Scenario: Person response includes contact fields
- **WHEN** a client sends GET to `/api/people/{id}/`
- **THEN** the response includes `email` and `linkedin_url` fields (empty string if not set)

#### Scenario: Person response includes tags
- **WHEN** a client sends GET to `/api/people/` or `/api/people/{id}/`
- **THEN** each person object includes a `tags` array of objects with `id` and `name`

#### Scenario: Person response includes last interaction data
- **WHEN** a client sends GET to `/api/people/` or `/api/people/{id}/`
- **THEN** each person object includes `last_interaction_date` (date or null) and `last_interaction_type` (string or null), derived from the M2M relationship

#### Scenario: Person with no interactions returns null interaction fields
- **WHEN** a client sends GET for a person who has no Interaction records via the M2M set
- **THEN** `last_interaction_date` is null and `last_interaction_type` is null

#### Scenario: Person with interactions returns most recent
- **WHEN** a client sends GET for a person who is in the people set of interactions on Jan 10 (Email) and Jan 20 (DM)
- **THEN** `last_interaction_date` is "2026-01-20" and `last_interaction_type` is "DM"

#### Scenario: Filter people by tag
- **WHEN** a client sends GET to `/api/people/?tag=investor`
- **THEN** the server responds with only people who have the "investor" tag

### Requirement: Person tag management API endpoints
The system SHALL expose JSON API endpoints to list person tags, add a tag to a person, and remove a tag from a person. The list endpoint SHALL support an optional `exclude_person` query parameter to exclude tags already assigned to a specific person. The add-tag endpoint SHALL use get_or_create to auto-create tags on first use. The add-tag endpoint SHALL reject blank tag names with status 400.

#### Scenario: List person tags
- **WHEN** a client sends GET to `/api/person-tags/`
- **THEN** the server responds with all PersonTag objects ordered by name

#### Scenario: List person tags with exclude_person filter
- **WHEN** a client sends GET to `/api/person-tags/?exclude_person=1`
- **THEN** the server responds with all PersonTag objects except those assigned to person 1

#### Scenario: Add tag to person
- **WHEN** a client sends POST to `/api/people/{id}/tags/` with `{"name": "investor"}`
- **THEN** the server get_or_creates the tag, adds it to the person, and responds with the person's tag list

#### Scenario: Remove tag from person
- **WHEN** a client sends DELETE to `/api/people/{id}/tags/{tag_id}/`
- **THEN** the server removes the tag association and responds with 204

### Requirement: Network API endpoints for organizations and types
The system SHALL expose JSON API endpoints to create, read, update, and delete organizations, org types, and interaction types.

#### Scenario: Create an organization
- **WHEN** a client sends POST to `/api/organizations/` with organization fields and an org type
- **THEN** the server creates the organization and responds with status 201 and the organization object

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

### Requirement: Network API endpoints for task links
The system SHALL expose JSON API endpoints to create and remove links between tasks and people, organizations, and interactions.

#### Scenario: Link a task to a person
- **WHEN** a client sends POST to `/api/tasks/:id/people/` with a person id
- **THEN** the server creates the link and responds with status 201
