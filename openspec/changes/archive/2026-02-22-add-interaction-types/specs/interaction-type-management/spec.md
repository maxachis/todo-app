## ADDED Requirements

### Requirement: Frontend API client supports creating interaction types
The frontend API client SHALL provide a `create` method on `interactionTypes` that sends a POST request to `/api/interaction-types/` with a `{ name: string }` payload and returns the created `InteractionType`.

#### Scenario: Create interaction type via API client
- **WHEN** `api.interactionTypes.create({ name: "Phone Call" })` is called
- **THEN** a POST request is sent to `/api/interaction-types/` with body `{"name": "Phone Call"}`
- **AND** the response is parsed as an `InteractionType` object with `id` and `name`

### Requirement: Interactions page provides inline interaction type creation
The Interactions page SHALL display an inline form above the interaction creation form with a text input and a "+ Type" button that creates a new interaction type.

#### Scenario: Create a new interaction type from the Interactions page
- **WHEN** the user enters "Email" in the new type input and submits the form
- **THEN** the system creates the interaction type via the API
- **AND** the new type appears in the interaction type dropdown
- **AND** the type input is cleared

#### Scenario: Empty type name is rejected
- **WHEN** the user submits the type creation form with an empty or whitespace-only name
- **THEN** no API call is made and no type is created

### Requirement: Newly created type is auto-selected when no type is chosen
The system SHALL auto-select a newly created interaction type in the "new interaction" form's type dropdown if no type is currently selected.

#### Scenario: Auto-select after creation with no prior selection
- **WHEN** a new interaction type is created and the interaction form's type dropdown has no selection
- **THEN** the newly created type is automatically selected in the dropdown

#### Scenario: No auto-select when a type is already chosen
- **WHEN** a new interaction type is created and the interaction form's type dropdown already has a selection
- **THEN** the existing selection is preserved
