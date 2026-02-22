## MODIFIED Requirements

### Requirement: Three-panel layout shell
The system SHALL render a three-panel layout: left sidebar (list navigation), center panel (task list), and right panel (task detail). The panel widths SHALL be user-adjustable via draggable resize handles on desktop viewports. A top navigation bar SHALL provide links to Tasks, People, Organizations, Interactions, Relationships, Graph, Projects, and Timesheet pages. The navigation bar SHALL also include a settings cog button and a theme toggle control. The Import page SHALL NOT appear as a primary navigation tab; it SHALL be accessible via the settings dropdown menu.

#### Scenario: Desktop layout shows all three panels
- **WHEN** the viewport is wider than 1024px
- **THEN** the sidebar, center panel, and detail panel are all visible simultaneously

#### Scenario: Desktop layout includes resize handles
- **WHEN** the viewport is wider than 1024px and the user is on the Tasks route
- **THEN** draggable resize handles are rendered between the sidebar and center panel, and between the center panel and detail panel

#### Scenario: Desktop panel widths are user-adjustable
- **WHEN** the user drags a resize handle on the Tasks route
- **THEN** the grid column widths update to reflect the dragged position, with the center panel using remaining space

#### Scenario: Mobile layout collapses panels
- **WHEN** the viewport is narrower than 1024px
- **THEN** the sidebar is hidden behind a hamburger menu, and the detail panel slides in as an overlay

#### Scenario: Bottom tab bar on mobile
- **WHEN** the viewport is narrower than 1024px
- **THEN** a bottom tab bar shows navigation links for Tasks, People, Organizations, Interactions, Relationships, Graph, Projects, and Timesheet (Import is NOT included)

#### Scenario: Non-task routes hide task side panels
- **WHEN** the user navigates to People, Organizations, Interactions, Relationships, Graph, Projects, Timesheet, or Import routes
- **THEN** the list sidebar and task detail panel are not shown

#### Scenario: Navigation bar includes theme toggle and settings cog
- **WHEN** the navigation bar renders
- **THEN** a settings cog button and theme toggle control are displayed in the right area of the navigation bar
