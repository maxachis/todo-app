## Purpose

Defines the Network route group structure and sub-tab navigation for Relationships and Graph pages.

## Requirements

### Requirement: Network route group with nested sub-routes
The system SHALL provide a `/network` route group using SvelteKit nested routes. The group SHALL contain sub-routes at `/network/relationships` and `/network/graph`. Navigating to `/network` SHALL redirect to `/network/relationships` via client-side `goto()`.

#### Scenario: Navigate to /network redirects to /network/relationships
- **WHEN** a user navigates to `/network`
- **THEN** the browser redirects to `/network/relationships` and the Relationships sub-page loads

#### Scenario: Navigate to /network/relationships
- **WHEN** a user navigates to `/network/relationships`
- **THEN** the Relationships page loads within the Network layout

#### Scenario: Navigate to /network/graph
- **WHEN** a user navigates to `/network/graph`
- **THEN** the Graph visualization page loads within the Network layout

### Requirement: Network sub-tab navigation bar
The Network layout SHALL render a sub-tab navigation bar with links to Relationships and Graph. The active sub-tab SHALL be highlighted based on the current route path. The sub-tab bar SHALL be visible on all Network sub-routes.

#### Scenario: Sub-tab bar displays on all Network pages
- **WHEN** the user is on any `/network/*` route
- **THEN** a sub-tab bar is visible with links to Relationships and Graph

#### Scenario: Active sub-tab is highlighted
- **WHEN** the user is on `/network/graph`
- **THEN** the Graph sub-tab is visually highlighted as active

#### Scenario: Clicking a sub-tab navigates without full reload
- **WHEN** the user clicks a sub-tab link
- **THEN** the corresponding sub-page loads via client-side navigation without a full page reload
