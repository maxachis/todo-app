## ADDED Requirements

### Requirement: Delete button in task detail panel
The task detail panel SHALL display a "Delete" button that allows the user to delete the currently selected task.

#### Scenario: Delete button is visible when a task is selected
- **WHEN** a task is selected and the detail panel is displayed
- **THEN** a "Delete" button SHALL be visible at the bottom of the detail panel

#### Scenario: Delete button is not visible when no task is selected
- **WHEN** no task is selected
- **THEN** the "Delete" button SHALL NOT be displayed

### Requirement: Confirmation before deletion
The system SHALL prompt the user for confirmation before deleting a task via the detail panel button.

#### Scenario: User confirms deletion
- **WHEN** the user clicks the "Delete" button
- **AND** confirms the confirmation dialog
- **THEN** the task SHALL be deleted
- **AND** the detail panel SHALL clear (no task selected)
- **AND** the task SHALL be removed from the task list

#### Scenario: User cancels deletion
- **WHEN** the user clicks the "Delete" button
- **AND** dismisses the confirmation dialog
- **THEN** the task SHALL NOT be deleted
- **AND** the detail panel SHALL continue showing the task

### Requirement: Delete button styling
The delete button SHALL use destructive/danger styling to visually distinguish it from other actions in the detail panel.

#### Scenario: Button appears as a destructive action
- **WHEN** the delete button is rendered
- **THEN** it SHALL use a red/error color scheme consistent with the app's design system
