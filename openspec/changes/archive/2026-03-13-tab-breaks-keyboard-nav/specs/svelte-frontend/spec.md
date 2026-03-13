## MODIFIED Requirements

### Requirement: Keyboard navigation with Tab indent/outdent
The keyboard action SHALL restore focus to the indented/outdented task's row element after the async move operation completes and the DOM re-renders. The `selectedTaskStore` SHALL remain set to the moved task's ID throughout the operation.

#### Scenario: Focus restored after Tab indent
- **WHEN** user presses Tab with a task selected and a valid previous sibling exists
- **THEN** the task is indented as a subtask of the previous sibling AND the task's row element receives focus AND arrow key / j/k navigation continues working immediately

#### Scenario: Focus restored after Shift+Tab outdent
- **WHEN** user presses Shift+Tab with a nested task selected
- **THEN** the task is outdented one level AND the task's row element receives focus AND arrow key / j/k navigation continues working immediately

#### Scenario: Keyboard navigation continues after indent
- **WHEN** user presses Tab to indent a task, then presses ArrowDown
- **THEN** the next task in the section is selected (focus was not lost)

#### Scenario: No-op indent preserves focus
- **WHEN** user presses Tab on a task with no valid previous sibling (cannot indent)
- **THEN** the task's row element retains focus and keyboard navigation continues
