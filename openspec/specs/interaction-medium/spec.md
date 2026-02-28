## Purpose

Interaction medium capability: allows classifying interactions by the communication channel used (e.g., Email, Phone, In-Person, Video), with full CRUD, frontend integration via TypeaheadSelect, and display in the interaction list.

## Requirements

### Requirement: InteractionMedium model
The system SHALL provide an `InteractionMedium` model with `id` (auto primary key) and `name` (CharField, max 255) fields, representing the communication channel used for an interaction (e.g., Email, Phone, In-Person, Video).

#### Scenario: Create an interaction medium
- **WHEN** an InteractionMedium is created with name "Email"
- **THEN** the record is persisted with an auto-assigned id and the name "Email"

#### Scenario: Medium name is stored as provided
- **WHEN** an InteractionMedium is created with name "In-Person"
- **THEN** the name is stored exactly as "In-Person"

### Requirement: InteractionMedium CRUD API
The system SHALL expose CRUD endpoints for InteractionMedium at `/api/interaction-mediums/`.

#### Scenario: List all mediums
- **WHEN** a GET request is sent to `/api/interaction-mediums/`
- **THEN** the response contains all mediums ordered by name, each with `id` and `name`

#### Scenario: Create a medium
- **WHEN** a POST request is sent to `/api/interaction-mediums/` with `{"name": "Phone"}`
- **THEN** the medium is created and returned with status 201, including its `id` and `name`

#### Scenario: Create a medium with blank name is rejected
- **WHEN** a POST request is sent to `/api/interaction-mediums/` with `{"name": "  "}`
- **THEN** the request is rejected with status 422

#### Scenario: Update a medium
- **WHEN** a PUT request is sent to `/api/interaction-mediums/{id}/` with `{"name": "Video Call"}`
- **THEN** the medium name is updated and the updated record is returned

#### Scenario: Delete a medium
- **WHEN** a DELETE request is sent to `/api/interaction-mediums/{id}/`
- **THEN** the medium is deleted with status 204
- **AND** any interactions referencing this medium have their medium set to null

### Requirement: Frontend API client supports interaction mediums
The frontend API client SHALL provide methods on `interactionMediums` for `getAll` (GET), `create` (POST with `{ name: string }`), `update` (PUT), and `remove` (DELETE), returning `InteractionMedium` objects with `id` and `name`.

#### Scenario: Fetch all mediums via API client
- **WHEN** `api.interactionMediums.getAll()` is called
- **THEN** a GET request is sent to `/api/interaction-mediums/` and the response is parsed as an array of `InteractionMedium`

#### Scenario: Create a medium via API client
- **WHEN** `api.interactionMediums.create({ name: "Chat" })` is called
- **THEN** a POST request is sent to `/api/interaction-mediums/` with body `{"name": "Chat"}` and the created medium is returned

### Requirement: Interaction form includes medium TypeaheadSelect
The Interactions page SHALL display a TypeaheadSelect for medium (with `onCreate` for inline creation) on both the create form and the edit detail panel. The medium field SHALL be optional — the form SHALL submit successfully without a medium selected.

#### Scenario: Medium TypeaheadSelect on create form
- **WHEN** the interaction create form is displayed
- **THEN** a TypeaheadSelect with placeholder "Medium" is shown, listing all available mediums

#### Scenario: Inline creation of a new medium
- **WHEN** the user types "Slack" in the medium TypeaheadSelect and no matching medium exists
- **THEN** a "Create Slack" option appears, and selecting it creates the medium via the API and selects it

#### Scenario: Create interaction without medium
- **WHEN** the user submits the interaction form with type, people, and date filled but no medium selected
- **THEN** the interaction is created successfully with `interaction_medium_id` as null

#### Scenario: Create interaction with medium
- **WHEN** the user submits the interaction form with a medium selected
- **THEN** the interaction is created with the selected `interaction_medium_id`

#### Scenario: Edit interaction medium
- **WHEN** an interaction is selected in the detail panel
- **THEN** the medium TypeaheadSelect displays the current medium (or empty if null) and allows changing or clearing it

### Requirement: Interaction list shows medium when present
The interaction list items SHALL display the medium alongside the type and date in the metadata line when a medium is set.

#### Scenario: List item with medium
- **WHEN** an interaction has type "Meeting" and medium "Video" and date "2026-02-28"
- **THEN** the list item metadata displays "Meeting · Video · 2026-02-28"

#### Scenario: List item without medium
- **WHEN** an interaction has type "Meeting" and no medium and date "2026-02-28"
- **THEN** the list item metadata displays "Meeting · 2026-02-28" (unchanged from current behavior)
