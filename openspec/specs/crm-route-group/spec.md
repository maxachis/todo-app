## Purpose

Defines the CRM route group structure, sub-tab navigation, shared linked-tasks logic module, and shared CRM CSS for all CRM entity pages.

## Requirements

### Requirement: CRM route group with nested sub-routes
The system SHALL provide a `/crm` route group using SvelteKit nested routes. The group SHALL contain sub-routes at `/crm/people`, `/crm/orgs`, `/crm/interactions`, and `/crm/leads`. Navigating to `/crm` SHALL redirect to `/crm/people` via client-side `goto()`.

#### Scenario: Navigate to /crm redirects to /crm/people
- **WHEN** a user navigates to `/crm`
- **THEN** the browser redirects to `/crm/people` and the People sub-page loads

#### Scenario: Navigate to /crm/people
- **WHEN** a user navigates to `/crm/people`
- **THEN** the People list and detail view loads within the CRM layout

#### Scenario: Navigate to /crm/orgs
- **WHEN** a user navigates to `/crm/orgs`
- **THEN** the Organizations list and detail view loads within the CRM layout

#### Scenario: Navigate to /crm/interactions
- **WHEN** a user navigates to `/crm/interactions`
- **THEN** the Interactions list and detail view loads within the CRM layout

#### Scenario: Navigate to /crm/leads
- **WHEN** a user navigates to `/crm/leads`
- **THEN** the Leads list and detail view loads within the CRM layout

### Requirement: CRM sub-tab navigation bar
The CRM layout SHALL render a sub-tab navigation bar with links to People, Orgs, Interactions, and Leads. The active sub-tab SHALL be highlighted based on the current route path using exact path matching. The sub-tab bar SHALL be visible on all CRM sub-routes.

#### Scenario: Sub-tab bar displays on all CRM pages
- **WHEN** the user is on any `/crm/*` route
- **THEN** a sub-tab bar is visible with links to People, Orgs, Interactions, and Leads

#### Scenario: Active sub-tab is highlighted
- **WHEN** the user is on `/crm/interactions`
- **THEN** the Interactions sub-tab is visually highlighted as active

#### Scenario: Clicking a sub-tab navigates without full reload
- **WHEN** the user clicks a sub-tab link
- **THEN** the corresponding sub-page loads via client-side navigation without a full page reload

### Requirement: Shared linked-tasks logic module
The system SHALL provide a shared TypeScript module that encapsulates the linked-tasks management logic used across all CRM entity pages. The module SHALL export a factory function that accepts an entity type and returns functions for loading all tasks, loading linked task IDs, adding a task link, removing a task link, and resolving a task name from its ID.

#### Scenario: Linked tasks load for a person
- **WHEN** the People page calls the shared linked-tasks loader for a selected person
- **THEN** the linked task IDs are fetched from `api.taskLinks.people.listByPerson` and the full task list is available for name resolution

#### Scenario: Linked tasks load for an organization
- **WHEN** the Organizations page calls the shared linked-tasks loader for a selected organization
- **THEN** the linked task IDs are fetched from `api.taskLinks.organizations.listByOrg`

#### Scenario: Linked tasks load for an interaction
- **WHEN** the Interactions page calls the shared linked-tasks loader for a selected interaction
- **THEN** the linked task IDs are fetched from `api.taskLinks.interactions.list`

#### Scenario: Linked tasks load for a lead
- **WHEN** the Leads page calls the shared linked-tasks loader for a selected lead
- **THEN** the linked task IDs are fetched from `api.taskLinks.leads.listByLead`

#### Scenario: Add and remove task links via shared module
- **WHEN** a CRM entity page adds or removes a task link using the shared module
- **THEN** the appropriate `api.taskLinks.<entity>.add` or `api.taskLinks.<entity>.remove` endpoint is called and the local linked IDs list is updated

### Requirement: Shared CRM CSS
The system SHALL provide a shared CSS stylesheet for CRM pages containing the common layout classes: page shell (`.crm-page`), two-column grid (`.crm-grid`), panel, create form, list, list item (with active state), detail header, detail form, danger button, linked-tasks section, empty state, and responsive breakpoint at 1024px. Entity-specific styles SHALL remain in their respective page components.

#### Scenario: CRM pages use shared layout classes
- **WHEN** any CRM sub-page renders
- **THEN** the page uses the shared `.crm-page`, `.crm-grid`, and `.panel` classes for its two-column list+detail layout

#### Scenario: Shared styles include responsive breakpoint
- **WHEN** the viewport is narrower than 1024px on a CRM sub-page
- **THEN** the `.crm-grid` collapses to a single-column layout
