## ADDED Requirements

### Requirement: Update time entry description via API
The system SHALL expose a PUT endpoint at `/api/timesheet/{entry_id}/` that accepts an `UpdateTimeEntryInput` with an optional `description` field. When called, the endpoint SHALL update the entry's description and return the updated `TimeEntrySchema`.

#### Scenario: Update description on existing entry
- **WHEN** PUT /api/timesheet/{entry_id}/ is called with `{"description": "Updated notes"}`
- **THEN** the entry's description is updated to "Updated notes" and the full entry is returned

#### Scenario: Update with empty description
- **WHEN** PUT /api/timesheet/{entry_id}/ is called with `{"description": ""}`
- **THEN** the entry's description is cleared and the full entry is returned

#### Scenario: Update nonexistent entry
- **WHEN** PUT /api/timesheet/{entry_id}/ is called with an invalid entry_id
- **THEN** the system returns a 404 error

### Requirement: Inline description editing in timesheet entry rows
The timesheet frontend SHALL allow users to edit the description of an entry inline. Clicking the description text (or an empty description placeholder) SHALL reveal an input field pre-filled with the current description. On blur, the updated description SHALL be saved via the PUT API endpoint. The local store SHALL update optimistically.

#### Scenario: Click description to edit
- **WHEN** the user clicks on an entry's description text
- **THEN** the text is replaced by an input field containing the current description

#### Scenario: Save on blur
- **WHEN** the user edits the description and the input loses focus
- **THEN** the updated description is saved via PUT API and the entry row reflects the change

#### Scenario: Edit empty description
- **WHEN** the user clicks the description area of an entry with no description
- **THEN** an empty input field appears, allowing the user to add a description
