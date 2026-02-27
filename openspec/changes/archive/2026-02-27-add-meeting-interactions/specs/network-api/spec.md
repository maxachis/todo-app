## MODIFIED Requirements

### Requirement: Network API endpoints for interactions and relationships
The system SHALL expose JSON API endpoints to create, read, update, and delete interactions and relationship records. The interaction create schema SHALL accept a `person_ids` field (list of integers, at least one required) instead of a single `person_id`. The interaction update schema SHALL accept an optional `person_ids` field that replaces the full set when provided. The interaction response schema SHALL include a `person_ids` field (list of integers) instead of `person_id`.

#### Scenario: Create an interaction
- **WHEN** a client sends POST to `/api/interactions/` with `person_ids`, type, date, and notes
- **THEN** the server creates the interaction, associates all specified people, and responds with status 201 and the interaction object including `person_ids`

#### Scenario: Update an interaction's people
- **WHEN** a client sends PUT to `/api/interactions/{id}/` with `person_ids: [2, 3]`
- **THEN** the server replaces the interaction's people set and responds with the updated interaction object

#### Scenario: Get interaction includes person_ids
- **WHEN** a client sends GET to `/api/interactions/{id}/`
- **THEN** the response includes `person_ids` as a list of associated person IDs

### Requirement: Network API endpoints for people
The system SHALL expose JSON API endpoints to create, read, update, and delete people under the `/api/` prefix. The create and update schemas SHALL accept optional `email` and `linkedin_url` fields. The response schema SHALL include `email`, `linkedin_url`, `last_interaction_date`, and `last_interaction_type` fields. The `last_interaction_date` SHALL be the date of the most recent Interaction record where the person is in the interaction's `people` M2M set (null if no interactions). The `last_interaction_type` SHALL be the name of the interaction type of the most recent such Interaction record (null if no interactions).

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

#### Scenario: Person response includes last interaction data
- **WHEN** a client sends GET to `/api/people/` or `/api/people/{id}/`
- **THEN** each person object includes `last_interaction_date` (date or null) and `last_interaction_type` (string or null), derived from the M2M relationship

#### Scenario: Person with no interactions returns null interaction fields
- **WHEN** a client sends GET for a person who has no Interaction records via the M2M set
- **THEN** `last_interaction_date` is null and `last_interaction_type` is null

#### Scenario: Person with interactions returns most recent
- **WHEN** a client sends GET for a person who is in the people set of interactions on Jan 10 (Email) and Jan 20 (DM)
- **THEN** `last_interaction_date` is "2026-01-20" and `last_interaction_type` is "DM"
