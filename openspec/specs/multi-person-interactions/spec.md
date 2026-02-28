### Requirement: Interaction supports multiple people
The Interaction model SHALL use a many-to-many relationship with Person via a `people` ManyToManyField (blank=True), replacing the previous single-person ForeignKey. An interaction MAY have zero or more associated people.

#### Scenario: Create interaction with multiple people
- **WHEN** an interaction is created and associated with persons Alice, Bob, and Carol
- **THEN** all three person associations are persisted and retrievable from the interaction

#### Scenario: Create interaction with one person
- **WHEN** an interaction is created and associated with a single person
- **THEN** the association is persisted, preserving the existing single-person workflow

#### Scenario: Create interaction with no people
- **WHEN** an interaction is created without associating any people
- **THEN** the interaction is created with an empty people set

#### Scenario: Update interaction people set
- **WHEN** an interaction's people set is replaced with a new set of person IDs
- **THEN** the previous associations are removed and the new associations are persisted

### Requirement: Data migration preserves existing person associations
The system SHALL migrate existing interaction data so that each interaction's previous single `person` ForeignKey value becomes the sole entry in its new M2M people set. No existing associations SHALL be lost during migration.

#### Scenario: Existing interaction migrated
- **WHEN** the migration runs on an interaction that had `person_id = 5`
- **THEN** the interaction's `people` M2M set contains exactly person ID 5

#### Scenario: All existing interactions migrated
- **WHEN** the migration completes
- **THEN** every pre-existing interaction has exactly one person in its M2M set matching its former `person_id`

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

### Requirement: Frontend interaction form supports multi-person selection
The interaction create and edit forms SHALL provide a multi-person selection UI using the TypeaheadSelect component in onSelect callback mode. Selected people SHALL be displayed as removable chips. The user SHALL be able to add people one at a time via the typeahead and remove them by clicking a remove control on each chip.

#### Scenario: Add multiple people in create form
- **WHEN** the user selects "Alice" then "Bob" from the person typeahead in the create form
- **THEN** both appear as removable chips and both are included when the form is submitted

#### Scenario: Remove a person from selection
- **WHEN** the user clicks the remove control on a person chip
- **THEN** that person is removed from the selection

#### Scenario: Edit form loads with existing people
- **WHEN** the user selects an interaction that has people Alice and Bob
- **THEN** the edit form shows Alice and Bob as chips in the person selection area

### Requirement: Interaction list displays all attendee names
The interaction list view SHALL display the names of all associated people for each interaction. When an interaction has more than 3 people, the display SHALL show the first 2 names followed by a "+N more" indicator.

#### Scenario: Interaction with one person in list
- **WHEN** an interaction associated with "Doe, Jane" appears in the list
- **THEN** the list item title shows "Doe, Jane"

#### Scenario: Interaction with two people in list
- **WHEN** an interaction associated with "Doe, Jane" and "Smith, Bob" appears in the list
- **THEN** the list item title shows both names

#### Scenario: Interaction with many people in list
- **WHEN** an interaction associated with 5 people appears in the list
- **THEN** the list item title shows the first 2 names followed by "+3 more"
