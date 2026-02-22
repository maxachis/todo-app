## MODIFIED Requirements

### Requirement: Network list and detail views
The system SHALL provide list and detail views for people, organizations, and interactions in the Svelte UI. Each detail view SHALL include a "Linked Tasks" section showing tasks associated with the entity. Entity selection fields in create and edit forms SHALL use typeahead inputs instead of native dropdown selects.

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
