## MODIFIED Requirements

### Requirement: Interaction API accepts and returns multiple person IDs
The interaction API create endpoint SHALL accept a `person_ids` field (list of integers, at least one required) and an optional `organization_ids` field (list of integers, defaults to empty list). The update endpoint SHALL accept optional `person_ids` and `organization_ids` fields (when provided, each replaces its full set). The response schema SHALL include both `person_ids` and `organization_ids` fields (lists of integers).

#### Scenario: Create interaction via API with multiple people
- **WHEN** a client sends POST to `/api/interactions/` with `person_ids: [1, 2, 3]`, type, date, and notes
- **THEN** the server creates the interaction, associates all three people, and responds with status 201 including `person_ids: [1, 2, 3]`

#### Scenario: Create interaction via API with people and organizations
- **WHEN** a client sends POST to `/api/interactions/` with `person_ids: [1]`, `organization_ids: [2, 3]`, type, and date
- **THEN** the server creates the interaction, associates the person and both organizations, and responds with status 201 including both `person_ids: [1]` and `organization_ids: [2, 3]`

#### Scenario: Update interaction people via API
- **WHEN** a client sends PUT to `/api/interactions/{id}/` with `person_ids: [4, 5]`
- **THEN** the server replaces the interaction's people set with persons 4 and 5

#### Scenario: Update interaction without changing people or organizations
- **WHEN** a client sends PUT to `/api/interactions/{id}/` without `person_ids` or `organization_ids` fields
- **THEN** the interaction's people and organizations sets remain unchanged

#### Scenario: Interaction response includes person_ids and organization_ids
- **WHEN** a client sends GET to `/api/interactions/` or `/api/interactions/{id}/`
- **THEN** each interaction object includes `person_ids` and `organization_ids` fields
