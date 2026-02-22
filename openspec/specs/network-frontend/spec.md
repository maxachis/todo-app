### Requirement: Network navigation in Svelte UI
The system SHALL provide Svelte routes and navigation entries for People, Organizations, Interactions, Relationships, and Graph.

#### Scenario: Navigate to People view
- **WHEN** a user selects People from the main navigation
- **THEN** the People view loads in the Svelte app without full-page reload

### Requirement: Network list and detail views
The system SHALL provide list and detail views for people, organizations, and interactions in the Svelte UI. Each detail view SHALL include a "Linked Tasks" section showing tasks associated with the entity. Entity selection fields in create and edit forms SHALL use typeahead inputs instead of native dropdown selects. The Interactions page SHALL include an inline form for creating new interaction types, following the same pattern as org type creation on the Organizations page.

#### Scenario: View person detail with linked tasks
- **WHEN** a user selects a person from the list
- **THEN** the detail panel shows the person data, related interactions, and a "Linked Tasks" section listing tasks linked to that person

#### Scenario: View organization detail with linked tasks
- **WHEN** a user selects an organization from the list
- **THEN** the detail panel shows the organization data and a "Linked Tasks" section listing tasks linked to that organization

#### Scenario: View interaction detail with linked tasks
- **WHEN** a user selects an interaction from the list
- **THEN** the detail panel shows the interaction data and a "Linked Tasks" section listing tasks linked to that interaction

#### Scenario: Linked tasks section supports add and remove
- **WHEN** a person, organization, or interaction detail view is displayed
- **THEN** the "Linked Tasks" section provides a typeahead input to search and link new tasks and a remove button on each linked task to unlink it

#### Scenario: Create interaction type inline on Interactions page
- **WHEN** a user enters a type name and submits the type creation form on the Interactions page
- **THEN** the new interaction type is created and appears in the interaction type dropdown

#### Scenario: Select person via typeahead in interaction create form
- **WHEN** a user types into the person field of the interaction create form
- **THEN** a filtered list of people appears matching the typed text, and selecting one sets the person for the new interaction

#### Scenario: Select interaction type via typeahead in interaction create form
- **WHEN** a user types into the interaction type field of the interaction create form
- **THEN** a filtered list of interaction types appears matching the typed text, and selecting one sets the type for the new interaction

#### Scenario: Select person via typeahead in interaction edit form
- **WHEN** a user types into the person field of the interaction edit form
- **THEN** a filtered list of people appears matching the typed text, and selecting one updates the person for the interaction

#### Scenario: Select interaction type via typeahead in interaction edit form
- **WHEN** a user types into the interaction type field of the interaction edit form
- **THEN** a filtered list of interaction types appears matching the typed text, and selecting one updates the type for the interaction

#### Scenario: Select org type via typeahead in organization create form
- **WHEN** a user types into the org type field of the organization create form
- **THEN** a filtered list of org types appears matching the typed text, and selecting one sets the org type for the new organization

#### Scenario: Select org type via typeahead in organization edit form
- **WHEN** a user types into the org type field of the organization edit form
- **THEN** a filtered list of org types appears matching the typed text, and selecting one updates the org type for the organization

### Requirement: Editable relationship notes on the Relationships page
The system SHALL allow users to edit the notes field on existing person-to-person and organization-to-person relationships directly from the Relationships page.

#### Scenario: Edit person-to-person relationship notes via inline edit
- **WHEN** the user clicks on a person-to-person relationship's notes area (or edit button)
- **THEN** the notes area switches to an editable textarea pre-filled with the current notes text

#### Scenario: Save edited notes on blur
- **WHEN** the user edits relationship notes and blurs the textarea
- **THEN** the updated notes are saved via PUT to `/relationships/people/{id}/` (or `/relationships/organizations/{id}/`) and the display updates immediately

#### Scenario: Cancel edit with Escape
- **WHEN** the user presses Escape while editing relationship notes
- **THEN** the edit is cancelled, the textarea reverts to the display view, and no API call is made

#### Scenario: Edit organization-to-person relationship notes
- **WHEN** the user clicks on an organization-to-person relationship's notes area (or edit button)
- **THEN** the notes area switches to an editable textarea, and saving works the same as for person-to-person relationships

#### Scenario: Add notes to a relationship with no existing notes
- **WHEN** a relationship has no notes and the user clicks the edit affordance
- **THEN** an empty textarea appears for entering notes, and saving persists the new notes

### Requirement: API client update methods for relationships
The system SHALL provide typed API client methods for updating existing person-to-person and organization-to-person relationships.

#### Scenario: Update person-to-person relationship
- **WHEN** the client calls `api.relationships.people.update(id, { notes })`
- **THEN** a PUT request is sent to `/relationships/people/{id}/` with the payload and the response is typed as `RelationshipPersonPerson`

#### Scenario: Update organization-to-person relationship
- **WHEN** the client calls `api.relationships.organizations.update(id, { notes })`
- **THEN** a PUT request is sent to `/relationships/organizations/{id}/` with the payload and the response is typed as `RelationshipOrganizationPerson`

### Requirement: Graph visualization parity
The system SHALL present the network graph in Svelte with equivalent behavior to the existing network app visualization.

#### Scenario: View graph
- **WHEN** a user opens the Graph view
- **THEN** the graph renders with the same data and interactions as the legacy network app
