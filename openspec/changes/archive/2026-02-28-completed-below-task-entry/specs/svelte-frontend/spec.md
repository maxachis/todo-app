## MODIFIED Requirements

### Requirement: Section layout ordering
Within each section in the Tasks view, elements SHALL render in the following order:
1. Section header
2. Active (incomplete) tasks with drag-and-drop
3. Task creation form
4. Completed tasks (collapsible)

The completed tasks section SHALL retain its existing collapsible toggle, count display, and styling. The task creation form SHALL appear directly after active tasks, before any completed tasks.

#### Scenario: Task create form appears before completed tasks
- **WHEN** a section contains both active and completed tasks
- **THEN** the task creation form SHALL render between the active tasks and the completed tasks section

#### Scenario: Section with no completed tasks
- **WHEN** a section has no completed tasks
- **THEN** the task creation form SHALL render directly after active tasks with no completed section visible

#### Scenario: Completed section collapse state preserved
- **WHEN** the user toggles the completed section open or closed
- **THEN** the toggle behavior SHALL work identically to the current implementation, just in its new position below the task creation form
