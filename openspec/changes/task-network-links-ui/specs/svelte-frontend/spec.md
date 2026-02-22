## MODIFIED Requirements

### Requirement: Three-panel layout shell
The system SHALL render a three-panel layout: left sidebar (list navigation), center panel (task list), and right panel (task detail). A top navigation bar SHALL provide links to Tasks, Upcoming, Projects, Timesheet, Import, and a "Network" group containing People, Organizations, Interactions, Relationships, and Graph pages. The navigation bar SHALL also include a theme toggle control.

#### Scenario: Top navbar includes network pages
- **WHEN** the navigation bar renders
- **THEN** it displays links for Tasks, Upcoming, Projects, Timesheet, Import, People, Organizations, Interactions, Relationships, and Graph

#### Scenario: Bottom tab bar on mobile includes network pages
- **WHEN** the viewport is narrower than 1024px
- **THEN** a bottom tab bar shows navigation links including People, Organizations, Interactions, Relationships, and Graph in addition to the existing tabs

#### Scenario: Non-task routes hide task side panels
- **WHEN** the user navigates to People, Organizations, Interactions, Relationships, Graph, Projects, Timesheet, or Import routes
- **THEN** the list sidebar and task detail panel are not shown

#### Scenario: Active state highlights current network page
- **WHEN** the user is on the People page
- **THEN** the People link in the navigation bar has the active visual style

### Requirement: Task detail panel
The system SHALL display a task's full details in the right panel when selected. All detail fields SHALL auto-save on blur. A recurrence editor SHALL be displayed below the due date field. A "Linked People & Orgs" section SHALL be displayed below the tags section.

#### Scenario: Selecting a task shows detail
- **WHEN** the user clicks a task row
- **THEN** the right panel displays the task's title, notes, due date, priority, tags, parent link, recurrence settings, and linked people & organizations

#### Scenario: Linked section appears in detail panel
- **WHEN** a task is selected
- **THEN** the detail panel includes a "Linked People & Orgs" section after the tags section, showing linked entities with add/remove controls
