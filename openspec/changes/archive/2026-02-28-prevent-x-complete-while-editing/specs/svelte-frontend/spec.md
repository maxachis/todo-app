## MODIFIED Requirements

### Requirement: Keyboard navigation
The system SHALL support full keyboard navigation for tasks. Navigation state SHALL be managed in a Svelte store. Destructive single-key shortcuts ("x" for complete, "Delete" for delete) SHALL only fire when the keyboard event originates from within a task row element (`[data-task-id]`). Non-destructive navigation shortcuts (j/k, arrow keys, Tab/Shift+Tab, Ctrl+arrows, Escape) SHALL continue to work from any focused element within the keyboard scope.

#### Scenario: Navigate with j/k or arrow keys
- **WHEN** the user presses j/ArrowDown or k/ArrowUp
- **THEN** the focus moves to the previous/next non-completed task, scrolling into view

#### Scenario: Click-to-keyboard continuity
- **WHEN** the user clicks a task and then presses j, k, ArrowUp, or ArrowDown
- **THEN** keyboard navigation applies immediately without requiring an additional focus click

#### Scenario: Downward navigation from create-form resumes task selection
- **WHEN** a create-form input is focused and the user presses ArrowDown or j
- **THEN** the input SHALL be blurred and keyboard navigation SHALL select the nearest task in the pressed direction immediately, without requiring a second keypress

#### Scenario: Complete with x key when focused on task row
- **WHEN** the user presses "x" and focus is on a task row element (`[data-task-id]`)
- **THEN** the task is completed (same behavior as clicking the checkbox)

#### Scenario: x key ignored when focus is not on task row
- **WHEN** the user presses "x" and focus is NOT on a task row element (e.g., focus is on a section header, button, or any other element inside the keyboard scope)
- **THEN** the keystroke SHALL be ignored and no task SHALL be completed

#### Scenario: Delete with Delete key when focused on task row
- **WHEN** the user presses Delete and focus is on a task row element (`[data-task-id]`)
- **THEN** a confirmation dialog appears; confirming deletes the task

#### Scenario: Delete key ignored when focus is not on task row
- **WHEN** the user presses Delete and focus is NOT on a task row element
- **THEN** the keystroke SHALL be ignored and no task SHALL be deleted

#### Scenario: Escape clears selection
- **WHEN** the user presses Escape
- **THEN** the selected task is deselected

#### Scenario: Tab indents, Shift+Tab outdents
- **WHEN** the user presses Tab on a focused task
- **THEN** the task is indented under the previous sibling

#### Scenario: Shift+Tab applies on first press
- **WHEN** the user presses Shift+Tab on a focused subtask
- **THEN** outdent is applied immediately without requiring a second keypress

#### Scenario: Browser tab traversal is suppressed for task hierarchy shortcuts
- **WHEN** a task is selected and the user presses Tab or Shift+Tab outside text-entry fields
- **THEN** browser focus traversal does not run, and task indent/outdent is applied immediately

#### Scenario: Cycle lists with Ctrl+Arrow
- **WHEN** the user presses Ctrl+ArrowLeft or Ctrl+ArrowRight
- **THEN** the selected list cycles to the previous or next list

#### Scenario: Jump between sections with Ctrl+Up/Down
- **WHEN** the user presses Ctrl+ArrowUp or Ctrl+ArrowDown on a focused task
- **THEN** focus jumps to the first task in the adjacent section
