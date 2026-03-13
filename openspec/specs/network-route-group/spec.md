## Purpose

Defines the Network route group structure for the Graph visualization page.

## Requirements

### Requirement: Network route group with nested sub-routes
The system SHALL provide a `/network` route group using SvelteKit nested routes. The group SHALL contain a sub-route at `/network/graph`. Navigating to `/network` SHALL redirect to `/network/graph` via client-side `goto()`.

#### Scenario: Navigate to /network redirects to /network/graph
- **WHEN** a user navigates to `/network`
- **THEN** the browser redirects to `/network/graph` and the Graph visualization page loads

#### Scenario: Navigate to /network/graph
- **WHEN** a user navigates to `/network/graph`
- **THEN** the Graph visualization page loads within the Network layout
