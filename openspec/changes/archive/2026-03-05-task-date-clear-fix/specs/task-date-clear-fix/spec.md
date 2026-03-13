## ADDED Requirements

### Requirement: Task detail form state resets only on task switch
The TaskDetail component SHALL reset local form values (title, due date, priority, notes) only when the selected task ID changes, not on every task object mutation from the store.

#### Scenario: Clearing due date persists
- **WHEN** the user clears the due date field in the task detail panel and the save triggers
- **THEN** the date field remains empty and the task's due_date is set to null

#### Scenario: Switching tasks resets form state
- **WHEN** the user selects a different task in the task list
- **THEN** all form fields in the detail panel are populated with the newly selected task's values

#### Scenario: Store update after save does not overwrite local edits
- **WHEN** a save completes and the store updates the task object
- **THEN** the local form values are NOT reset to the store values
