### Requirement: TaskRow accessibility keydown handler ignores text entry targets
The `.task-row` element's `onkeydown` handler SHALL NOT intercept `Space` or `Enter` key events when the event originates from a text-entry element (`input`, `textarea`, `select`, or `[contenteditable="true"]`) within the row. This allows normal text input behavior during inline task title editing.

#### Scenario: Space key inserts a space during inline title editing
- **WHEN** the user is inline-editing a task title (via double-click) and presses the space bar
- **THEN** a space character is inserted into the input field, and the task selection state does not change

#### Scenario: Enter key still commits inline title edit
- **WHEN** the user is inline-editing a task title and presses Enter
- **THEN** the edit is committed (via the input's own keydown handler), and the parent row's handler does not additionally trigger `handleClick`

#### Scenario: Space key still activates task row when not editing
- **WHEN** the user focuses a task row (not inline editing) and presses the space bar
- **THEN** the task is selected, preserving the existing accessibility behavior
