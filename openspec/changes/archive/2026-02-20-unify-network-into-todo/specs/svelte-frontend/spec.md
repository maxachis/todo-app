## MODIFIED Requirements

### Requirement: Three-panel layout shell
The system SHALL render a three-panel layout: left sidebar (list navigation), center panel (task list), and right panel (task detail). A top navigation bar SHALL provide links to Tasks, People, Organizations, Interactions, Relationships, Graph, Projects, Timesheet, and Import pages.

#### Scenario: Desktop layout shows all three panels
- **WHEN** the viewport is wider than 1024px
- **THEN** the sidebar, center panel, and detail panel are all visible simultaneously

#### Scenario: Mobile layout collapses panels
- **WHEN** the viewport is narrower than 1024px
- **THEN** the sidebar is hidden behind a hamburger menu, and the detail panel slides in as an overlay

#### Scenario: Bottom tab bar on mobile
- **WHEN** the viewport is narrower than 1024px
- **THEN** a bottom tab bar shows navigation links for Tasks, People, Organizations, Interactions, Relationships, Graph, Projects, Timesheet, and Import

#### Scenario: Non-task routes hide task side panels
- **WHEN** the user navigates to People, Organizations, Interactions, Relationships, Graph, Projects, Timesheet, or Import routes
- **THEN** the list sidebar and task detail panel are not shown

## ADDED Requirements

### Requirement: Network navigation in Svelte UI
The system SHALL provide Svelte routes and navigation entries for People, Organizations, Interactions, Relationships, and Graph.

#### Scenario: Navigate to People view
- **WHEN** a user selects People from the main navigation
- **THEN** the People view loads in the Svelte app without full-page reload

### Requirement: Network list and detail views
The system SHALL provide list and detail views for people, organizations, and interactions in the Svelte UI.

#### Scenario: View person detail
- **WHEN** a user selects a person from the list
- **THEN** the detail panel shows the person data and related interactions

### Requirement: Graph visualization parity
The system SHALL present the network graph in Svelte with equivalent behavior to the existing network app visualization.

#### Scenario: View graph
- **WHEN** a user opens the Graph view
- **THEN** the graph renders with the same data and interactions as the legacy network app
