## MODIFIED Requirements

### Requirement: Network route group with nested sub-routes
The system SHALL provide a `/network` route group using SvelteKit nested routes. The group SHALL contain a sub-route at `/network/graph`. Navigating to `/network` SHALL redirect to `/network/graph` via client-side `goto()`.

#### Scenario: Navigate to /network redirects to /network/graph
- **WHEN** a user navigates to `/network`
- **THEN** the browser redirects to `/network/graph` and the Graph visualization page loads

#### Scenario: Navigate to /network/graph
- **WHEN** a user navigates to `/network/graph`
- **THEN** the Graph visualization page loads within the Network layout

## REMOVED Requirements

### Requirement: Network sub-tab navigation bar
**Reason**: With only Graph remaining under Network, a sub-tab bar with a single item is unnecessary. The Network layout renders content directly without sub-tab navigation.
