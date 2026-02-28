## MODIFIED Requirements

### Requirement: Three-panel layout shell
The system SHALL render a three-panel layout: left sidebar (list navigation), center panel (task list), and right panel (task detail). The panel widths SHALL be user-adjustable via draggable resize handles on desktop viewports. A top navigation bar SHALL provide links to Tasks, Dashboard, Projects, Timesheet, CRM, and Network pages. The navigation bar SHALL also include a settings cog button and a theme toggle control. The Import page SHALL NOT appear as a primary navigation tab; it SHALL be accessible via the settings dropdown menu. On phone viewports (640px and below), the app shell SHALL use `100dvh` (with `100vh` fallback) instead of `100vh` to account for mobile browser chrome resizing. All interactive elements in the navigation bar SHALL meet a 44px minimum touch target height on phone viewports. The CRM nav tab SHALL be highlighted as active when the current path starts with `/crm`. The Network nav tab SHALL be highlighted as active when the current path starts with `/network`.

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
- **THEN** a bottom tab bar shows navigation links for Tasks, Dashboard, Projects, Timesheet, CRM, and Network (Import is NOT included)

#### Scenario: Non-task routes hide task side panels
- **WHEN** the user navigates to CRM, Network, Dashboard, Projects, Timesheet, or Import routes
- **THEN** the list sidebar and task detail panel are not shown

#### Scenario: Navigation bar includes theme toggle and settings cog
- **WHEN** the navigation bar renders
- **THEN** a settings cog button and theme toggle control are displayed in the right area of the navigation bar

#### Scenario: Phone viewport uses dynamic viewport height
- **WHEN** the viewport is 640px or narrower
- **THEN** the app shell height uses `dvh` units (with `vh` fallback) so content is not hidden behind mobile browser chrome

#### Scenario: Phone viewport touch targets in navbar
- **WHEN** the viewport is 640px or narrower
- **THEN** all navbar buttons (hamburger, settings cog, theme toggle, detail panel toggle) have a minimum touch target of 44px height

#### Scenario: CRM nav tab active on CRM sub-routes
- **WHEN** the user is on `/crm/people`, `/crm/orgs`, `/crm/interactions`, or `/crm/leads`
- **THEN** the CRM tab in the top navbar is highlighted as active

#### Scenario: Network nav tab active on Network sub-routes
- **WHEN** the user is on `/network/relationships` or `/network/graph`
- **THEN** the Network tab in the top navbar is highlighted as active

### Requirement: Relationships page phone layout
The system SHALL render the Relationships page at `/network/relationships` without text overflow on phone viewports (640px and below). Relationship titles SHALL be truncated with ellipsis and action buttons SHALL meet minimum touch target sizes.

#### Scenario: Phone viewport relationship title truncation
- **WHEN** the viewport is 640px or narrower and a relationship title (e.g., "Person A ↔ Person B") exceeds the card width
- **THEN** the title is truncated with ellipsis

#### Scenario: Phone viewport relationship action buttons are touch-sized
- **WHEN** the viewport is 640px or narrower
- **THEN** relationship card action buttons have a minimum touch target of 44px height
