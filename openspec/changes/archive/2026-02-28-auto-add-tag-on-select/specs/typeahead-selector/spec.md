## ADDED Requirements

### Requirement: Tag selection uses TypeaheadSelect in action mode
The task detail view SHALL use the TypeaheadSelect component in action mode for adding tags to a task, replacing the previous datalist + form + submit button UI.

#### Scenario: TypeaheadSelect renders in tag field
- **WHEN** the task detail panel is displayed for a task
- **THEN** the tag field SHALL contain a TypeaheadSelect component with placeholder "Add tag..." and available (not-yet-assigned) tags as options

#### Scenario: Selecting an existing tag immediately adds it
- **WHEN** the user selects a tag from the TypeaheadSelect dropdown (via click or Enter)
- **THEN** the tag SHALL be added to the task immediately via the API
- **AND** the input SHALL clear (action mode behavior)
- **AND** the task detail SHALL refresh to show the newly added tag
- **AND** the added tag SHALL no longer appear in the dropdown options

#### Scenario: Creating a new tag via onCreate
- **WHEN** the user types a tag name that does not match any existing tag and selects the "Create …" option
- **THEN** a new tag SHALL be created and added to the task via the API
- **AND** the input SHALL clear
- **AND** the task detail SHALL refresh to show the newly created tag

#### Scenario: No submit button is present
- **WHEN** the task detail panel tag field is rendered
- **THEN** there SHALL be no "+" submit button for adding tags

#### Scenario: Available tags update after adding
- **WHEN** a tag has been added to the task (existing or newly created)
- **THEN** the available tags list SHALL refresh to exclude tags already assigned to the task
