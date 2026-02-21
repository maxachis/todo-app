## MODIFIED Requirements

### Requirement: Task list rendering
The system SHALL display tasks within sections, showing title, tags, due date, subtask count, pin button, and a recurrence indicator. Completed tasks SHALL appear in a separate "Completed" group at the bottom.

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

### Requirement: Task detail panel
The system SHALL display a task's full details in the right panel when selected. All detail fields SHALL auto-save on blur. A recurrence editor SHALL be displayed below the due date field.

#### Scenario: Selecting a task shows detail
- **WHEN** the user clicks a task row
- **THEN** the right panel displays the task's title, notes, due date, priority, tags, parent link, and recurrence settings

#### Scenario: Auto-save on blur
- **WHEN** the user edits the title, due date, or notes and then blurs the field
- **THEN** the change is saved to the API and the center panel task row updates reactively

#### Scenario: Empty state when no task selected
- **WHEN** no task is selected
- **THEN** the detail panel shows "Select a task to view details"

#### Scenario: Parent task link
- **WHEN** viewing a subtask's detail
- **THEN** a link to the parent task is shown with a "jump to" action that scrolls to and highlights the parent in the center panel

### Requirement: Task completion with optimistic UI
The system SHALL provide task completion with immediate visual feedback. Completing a parent SHALL cascade to non-completed subtasks. Completing a recurring task SHALL display a toast indicating the next occurrence.

#### Scenario: Complete a task with animation
- **WHEN** the user checks a task's completion checkbox
- **THEN** the task fades out (180ms), moves to the "Completed" section, and a toast appears offering undo

#### Scenario: Complete a recurring task shows next occurrence toast
- **WHEN** the user completes a recurring task
- **THEN** a toast appears with the message "Next: [due date]" and the new task instance appears in the section

#### Scenario: Undo via toast
- **WHEN** the user clicks "Undo" on the toast within 5 seconds
- **THEN** the task is uncompleted and returns to its original position

#### Scenario: Toast auto-dismisses
- **WHEN** 5 seconds pass after a completion toast appears
- **THEN** the toast dismisses automatically

#### Scenario: Cascade completion to subtasks
- **WHEN** the user completes a parent task
- **THEN** all non-completed subtasks are also marked complete, with the UI updating reactively

## ADDED Requirements

### Requirement: Recurrence editor in task detail
The system SHALL provide a recurrence editor in the task detail panel that allows setting and modifying repeat schedules. The editor SHALL appear below the due date field.

#### Scenario: Recurrence type selector
- **WHEN** the user views a task's detail panel
- **THEN** a "Repeat" dropdown is shown with options: None, Daily, Weekly, Monthly, Yearly, Custom Dates

#### Scenario: Weekly recurrence shows day picker
- **WHEN** the user selects "Weekly" from the repeat dropdown
- **THEN** a row of weekday toggles (Mon–Sun) appears for selecting which days the task repeats

#### Scenario: Monthly recurrence shows day-of-month input
- **WHEN** the user selects "Monthly" from the repeat dropdown
- **THEN** a numeric input appears for selecting the day of the month (1-31)

#### Scenario: Yearly recurrence shows month and day inputs
- **WHEN** the user selects "Yearly" from the repeat dropdown
- **THEN** month and day inputs appear for selecting the annual date

#### Scenario: Custom dates shows date list editor
- **WHEN** the user selects "Custom Dates" from the repeat dropdown
- **THEN** an interface appears to add/remove MM-DD date entries, displayed as a list

#### Scenario: Recurrence changes auto-save on blur
- **WHEN** the user changes the recurrence type or rule parameters and blurs the editor
- **THEN** the recurrence settings are saved to the API via the task update endpoint

#### Scenario: Daily recurrence has no extra options
- **WHEN** the user selects "Daily" from the repeat dropdown
- **THEN** no additional configuration inputs appear (daily is the only option needed)

#### Scenario: Clearing recurrence
- **WHEN** the user selects "None" from the repeat dropdown on a recurring task
- **THEN** the recurrence is removed and the task behaves as a one-off task on next completion

### Requirement: Recurrence-aware TypeScript types
The system SHALL extend the frontend Task type to include recurrence fields for type-safe access throughout the UI.

#### Scenario: Task type includes recurrence fields
- **WHEN** the frontend TypeScript types are defined
- **THEN** the `Task` interface includes `recurrence_type: string`, `recurrence_rule: object`, and `next_occurrence_id: number | null`

#### Scenario: UpdateTaskInput includes recurrence fields
- **WHEN** the frontend update input type is defined
- **THEN** the `UpdateTaskInput` interface includes optional `recurrence_type?: string` and `recurrence_rule?: object`
