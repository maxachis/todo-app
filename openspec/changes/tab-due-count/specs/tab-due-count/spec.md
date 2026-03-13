## ADDED Requirements

### Requirement: Tab title displays count of actionable tasks
The browser tab title SHALL display the number of overdue and due-today incomplete tasks in the format `(N) Nexus`, where N is the combined count.

#### Scenario: Tasks are due today and overdue
- **WHEN** there are 2 overdue tasks and 1 task due today
- **THEN** the document title SHALL be `(3) Nexus`

#### Scenario: No actionable tasks
- **WHEN** there are no overdue or due-today tasks
- **THEN** the document title SHALL be `Nexus` (no count badge)

#### Scenario: Only future tasks exist
- **WHEN** all tasks have due dates in the future (tomorrow or later)
- **THEN** the document title SHALL be `Nexus` (no count badge)

### Requirement: Tab title updates reactively
The tab title count SHALL update automatically when the underlying task data changes, without requiring a page refresh.

#### Scenario: Task completed reduces count
- **WHEN** the user completes a task that was due today and the count was `(3) Nexus`
- **THEN** the document title SHALL update to `(2) Nexus`

#### Scenario: Count reaches zero
- **WHEN** the user completes the last overdue/due-today task
- **THEN** the document title SHALL update to `Nexus`

### Requirement: Upcoming data loads on app initialization
The upcoming task data SHALL be fetched when the app loads, regardless of which page the user navigates to first, so the tab title count is available on all routes.

#### Scenario: User opens the app on the Tasks page
- **WHEN** the user navigates directly to `/`
- **THEN** the upcoming data SHALL be loaded and the tab title SHALL reflect the current count

#### Scenario: User opens the app on the Timesheet page
- **WHEN** the user navigates directly to `/timesheet`
- **THEN** the upcoming data SHALL be loaded and the tab title SHALL reflect the current count
