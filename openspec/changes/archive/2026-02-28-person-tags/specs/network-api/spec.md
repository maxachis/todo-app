## ADDED Requirements

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

## MODIFIED Requirements

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
