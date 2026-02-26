## MODIFIED Requirements

### Requirement: Keyboard navigation
The system SHALL support full keyboard navigation for tasks. Navigation state SHALL be managed in a Svelte store.

#### Scenario: Arrow key navigation
- **WHEN** the user presses Arrow Up or Arrow Down (or j/k)
- **THEN** the focus moves to the previous/next non-completed task, scrolling into view

#### Scenario: Click-to-keyboard continuity
- **WHEN** the user clicks a task row and then presses Arrow Up or Arrow Down
- **THEN** keyboard navigation applies immediately without requiring an additional focus click

#### Scenario: Arrow key navigation from task-add input
- **WHEN** the user is focused on a task-add input ("Add task..." or "Add subtask...") and presses Arrow Up or Arrow Down
- **THEN** the input SHALL be blurred and keyboard navigation SHALL select the nearest task in the pressed direction immediately, without requiring a second keypress

#### Scenario: Escape in task-add input
- **WHEN** the user is focused on a task-add input and presses Escape
- **THEN** any typed text SHALL be cleared and the input SHALL be blurred

#### Scenario: Tab indent / Shift+Tab outdent
- **WHEN** the user presses Tab on a focused task
- **THEN** the task becomes a subtask of the previous sibling; Shift+Tab promotes it

#### Scenario: Tab indent is section-bounded
- **WHEN** the user presses Tab and the previous visible task is in a different section
- **THEN** no cross-section indent/reparent occurs and the task remains in its current section

#### Scenario: Tab indent is same-level bounded
- **WHEN** the user presses Tab on a task and the closest previous visible task is a deeper child level
- **THEN** the task does not indent under that child and instead uses the closest previous task at the same current level

#### Scenario: Outdent places task after former parent
- **WHEN** the user presses Shift+Tab on a subtask
- **THEN** the task is promoted one level and inserted immediately after its former parent in sibling order

#### Scenario: Shift+Tab applies on first press
- **WHEN** the user presses Shift+Tab on a focused subtask
- **THEN** outdent is applied immediately without requiring a second keypress

#### Scenario: Browser tab traversal is suppressed for task hierarchy shortcuts
- **WHEN** a task is selected and the user presses Tab or Shift+Tab outside text-entry fields
- **THEN** browser focus traversal does not run, and task indent/outdent is applied immediately

#### Scenario: Complete with x key
- **WHEN** the user presses x on a focused task
- **THEN** the task is completed (same behavior as clicking the checkbox)

#### Scenario: Delete with Delete key
- **WHEN** the user presses Delete on a focused task
- **THEN** a confirmation dialog appears; confirming deletes the task

#### Scenario: Escape clears selection
- **WHEN** the user presses Escape
- **THEN** the task selection is cleared and the detail panel shows empty state

#### Scenario: Section jumping
- **WHEN** the user presses Ctrl+Arrow Down or Ctrl+Arrow Up
- **THEN** focus jumps to the first task of the next/previous section

#### Scenario: List cycling
- **WHEN** the user presses Ctrl+Arrow Left or Ctrl+Arrow Right
- **THEN** the previous/next list in the sidebar is selected

#### Scenario: Collapsed sections are skipped
- **WHEN** navigating with arrow keys and a section is collapsed
- **THEN** tasks inside that section are skipped
