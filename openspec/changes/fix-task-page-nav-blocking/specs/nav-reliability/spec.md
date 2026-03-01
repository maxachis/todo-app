## ADDED Requirements

### Requirement: Navbar navigation works from the task page with large datasets
The system SHALL allow the user to navigate to any page via the navbar when on the task page, regardless of how many tasks are loaded in the current list.

#### Scenario: Navigate from task page to Dashboard with large dataset
- **WHEN** the task page has 150+ tasks loaded across multiple sections
- **AND** the user clicks the "Dashboard" navbar link
- **THEN** the app SHALL navigate to `/dashboard` within 2 seconds
- **AND** the Dashboard page content SHALL be visible

#### Scenario: Navigate from task page to CRM with large dataset
- **WHEN** the task page has 150+ tasks loaded across multiple sections
- **AND** the user clicks the "CRM" navbar link
- **THEN** the app SHALL navigate to `/crm` within 2 seconds

#### Scenario: Navigate from task page after interacting with tasks
- **WHEN** the user has clicked on one or more tasks in the task list (selecting them)
- **AND** the user then clicks a navbar link
- **THEN** the app SHALL navigate to the target page within 2 seconds

### Requirement: Navbar links use explicit programmatic navigation
The navbar links SHALL use SvelteKit's `goto()` function for navigation to ensure clicks are not blocked by event propagation interference from task page components.

#### Scenario: Navigation bypasses event delegation
- **WHEN** a navbar link is clicked
- **THEN** `goto()` SHALL be called with the link's href
- **AND** navigation SHALL succeed even if other components on the page use `stopPropagation()` on pointer events

### Requirement: TaskList reactive updates do not cause re-render cascades
The TaskList component SHALL NOT trigger cascading re-renders when recalculating active tasks, to prevent main-thread blocking that could delay event processing.

#### Scenario: Large list selection does not block main thread
- **WHEN** the user selects a list with 100+ tasks
- **THEN** the DnD zone SHALL configure once per task prop change (not multiple times due to reactive loops)
- **AND** the UI SHALL remain responsive to navbar clicks during and after rendering
