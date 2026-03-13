## MODIFIED Requirements

### Requirement: CRM route group with nested sub-routes
The system SHALL provide a `/crm` route group using SvelteKit nested routes. The group SHALL contain sub-routes at `/crm/people`, `/crm/orgs`, `/crm/interactions`, `/crm/leads`, and `/crm/relationships`. Navigating to `/crm` SHALL redirect to `/crm/people` via client-side `goto()`.

#### Scenario: Navigate to /crm redirects to /crm/people
- **WHEN** a user navigates to `/crm`
- **THEN** the browser redirects to `/crm/people` and the People sub-page loads

#### Scenario: Navigate to /crm/relationships
- **WHEN** a user navigates to `/crm/relationships`
- **THEN** the Relationships page loads within the CRM layout showing person-person and org-person relationship management

### Requirement: CRM sub-tab navigation bar
The CRM layout SHALL render a sub-tab navigation bar with links to Inbox, People, Orgs, Interactions, Leads, and Relationships. The active sub-tab SHALL be highlighted based on the current route path. The sub-tab bar SHALL be visible on all CRM sub-routes.

#### Scenario: Sub-tab bar displays on all CRM pages
- **WHEN** the user is on any `/crm/*` route
- **THEN** a sub-tab bar is visible with links to Inbox, People, Orgs, Interactions, Leads, and Relationships

#### Scenario: Active sub-tab is highlighted
- **WHEN** the user is on `/crm/relationships`
- **THEN** the "Relationships" sub-tab is visually highlighted as active
