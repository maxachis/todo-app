## MODIFIED Requirements

### Requirement: Network list and detail views
The system SHALL provide list and detail views for people, organizations, and interactions in the Svelte UI. Each detail view SHALL include a "Linked Tasks" section showing tasks associated with the entity. Entity selection fields in create and edit forms SHALL use typeahead inputs instead of native dropdown selects. Type typeaheads on Organizations and Interactions pages SHALL support inline creation of new types via the TypeaheadSelect `onCreate` callback.

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

#### Scenario: Create org type inline via typeahead on Organizations page
- **WHEN** a user types a name into the org type typeahead (in the create or edit form) that does not match any existing org type
- **THEN** a "Create [typed name]" option appears, and selecting it creates the org type via the API, adds it to the local type list, and selects it in the typeahead

#### Scenario: Create interaction type inline via typeahead on Interactions page
- **WHEN** a user types a name into the interaction type typeahead (in the create or edit form) that does not match any existing interaction type
- **THEN** a "Create [typed name]" option appears, and selecting it creates the interaction type via the API, adds it to the local type list, and selects it in the typeahead

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

## REMOVED Requirements

### Requirement: Standalone type creation forms
**Reason**: Replaced by inline type creation via the TypeaheadSelect `onCreate` callback. The standalone "Create Type" input+button forms on Organizations and Interactions pages are no longer needed.
**Migration**: Users create new types by typing a non-matching name into any type typeahead and selecting the "Create [name]" option.
