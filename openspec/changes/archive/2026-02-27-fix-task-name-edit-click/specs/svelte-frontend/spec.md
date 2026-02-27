## MODIFIED Requirements

### Requirement: Task list rendering
The system SHALL display tasks within sections, showing title, tags, due date, subtask count, pin button, and a recurrence indicator. Completed tasks SHALL appear in a separate "Completed" group at the bottom. On phone viewports (640px and below), task row metadata SHALL wrap instead of overflowing, and interactive elements SHALL meet minimum touch target sizes. The inline task title edit input SHALL stop click event propagation so that clicks within the input do not exit edit mode.

#### Scenario: Tasks render with metadata
- **WHEN** a section is displayed
- **THEN** each task row shows its title, tag badges, abbreviated due date, subtask count label, and a repeat icon if the task has recurrence

#### Scenario: Recurring task shows repeat indicator
- **WHEN** a task has `recurrence_type` other than `none`
- **THEN** the task row displays a small repeat icon (e.g., circular arrows) near the due date

#### Scenario: Completed tasks grouped separately
- **WHEN** a section contains completed tasks
- **THEN** completed tasks appear under a collapsible "Completed" subsection

#### Scenario: Subtask count label
- **WHEN** a task has subtasks
- **THEN** the task row displays a label like "3 subtasks — 1 open" that updates reactively

#### Scenario: Subtask nesting display
- **WHEN** a task has subtasks
- **THEN** subtasks are rendered nested below the parent with visual indentation, collapsible via a toggle

#### Scenario: Phone viewport task row metadata wraps
- **WHEN** the viewport is 640px or narrower and a task row has metadata (tags, due date, subtask count)
- **THEN** the metadata section wraps to a second line instead of overflowing horizontally

#### Scenario: Phone viewport task row touch targets
- **WHEN** the viewport is 640px or narrower
- **THEN** task row checkboxes and pin buttons have a minimum touch target of 44px

#### Scenario: Inline title edit stays active on click
- **WHEN** the user has double-clicked a task title to enter edit mode and then clicks inside the title input
- **THEN** the input SHALL retain focus and edit mode SHALL remain active
- **AND** the click SHALL NOT propagate to the parent task row's click handler
