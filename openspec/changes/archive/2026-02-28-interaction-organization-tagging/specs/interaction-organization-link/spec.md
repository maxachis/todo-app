## ADDED Requirements

### Requirement: Interaction supports tagging organizations
The Interaction model SHALL include a many-to-many relationship with Organization via an `organizations` ManyToManyField (blank=True). An interaction MAY have zero or more associated organizations.

#### Scenario: Create interaction with organizations
- **WHEN** an interaction is created and associated with organizations Acme Corp and Globex
- **THEN** both organization associations are persisted and retrievable from the interaction

#### Scenario: Create interaction without organizations
- **WHEN** an interaction is created without associating any organizations
- **THEN** the interaction is created with an empty organizations set

#### Scenario: Update interaction organizations
- **WHEN** an interaction's organizations set is replaced with a new set of organization IDs
- **THEN** the previous associations are removed and the new associations are persisted

### Requirement: Interaction API accepts and returns organization IDs
The interaction API create and update endpoints SHALL accept an optional `organization_ids` field (list of integers, defaults to empty list). The response schema SHALL include an `organization_ids` field (list of integers).

#### Scenario: Create interaction via API with organizations
- **WHEN** a client sends POST to `/api/interactions/` with `organization_ids: [1, 2]`, `person_ids: [1]`, type, and date
- **THEN** the server creates the interaction, associates both organizations, and responds with status 201 including `organization_ids: [1, 2]`

#### Scenario: Create interaction via API without organizations
- **WHEN** a client sends POST to `/api/interactions/` without an `organization_ids` field
- **THEN** the interaction is created with an empty organizations set and the response includes `organization_ids: []`

#### Scenario: Update interaction organizations via API
- **WHEN** a client sends PUT to `/api/interactions/{id}/` with `organization_ids: [3]`
- **THEN** the server replaces the interaction's organizations set with organization 3

#### Scenario: Update interaction without changing organizations
- **WHEN** a client sends PUT to `/api/interactions/{id}/` without an `organization_ids` field
- **THEN** the interaction's organizations set remains unchanged

#### Scenario: Interaction response includes organization_ids
- **WHEN** a client sends GET to `/api/interactions/` or `/api/interactions/{id}/`
- **THEN** each interaction object includes an `organization_ids` field containing the list of associated organization IDs

### Requirement: Frontend interaction form supports organization selection
The interaction create and edit forms SHALL provide an organization multi-select UI using the TypeaheadSelect component. Selected organizations SHALL be displayed as removable chips. The organization selector SHALL appear below the people selector.

#### Scenario: Add organizations in create form
- **WHEN** the user selects "Acme Corp" then "Globex" from the organization typeahead in the create form
- **THEN** both appear as removable chips and both are included when the form is submitted

#### Scenario: Remove an organization from selection
- **WHEN** the user clicks the remove control on an organization chip
- **THEN** that organization is removed from the selection

#### Scenario: Edit form loads with existing organizations
- **WHEN** the user selects an interaction that has organizations Acme Corp and Globex
- **THEN** the edit form shows Acme Corp and Globex as chips in the organization selection area

#### Scenario: Submit form with no organizations selected
- **WHEN** the user submits the create form without selecting any organizations
- **THEN** the interaction is created successfully with an empty organizations set

### Requirement: Interaction list displays tagged organization names
The interaction list view SHALL display the names of associated organizations for each interaction, in addition to people names.

#### Scenario: Interaction with organizations in list
- **WHEN** an interaction associated with organization "Acme Corp" appears in the list
- **THEN** the list item displays the organization name

#### Scenario: Interaction with no organizations in list
- **WHEN** an interaction with no associated organizations appears in the list
- **THEN** no organization names are shown for that list item
