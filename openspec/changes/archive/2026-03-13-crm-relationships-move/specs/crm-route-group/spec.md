## MODIFIED Requirements

### Requirement: CRM route group with nested sub-routes
The system SHALL provide a `/crm` route group using SvelteKit nested routes. The group SHALL contain sub-routes at `/crm/people`, `/crm/orgs`, `/crm/interactions`, `/crm/leads`, and `/crm/relationships`. Navigating to `/crm` SHALL redirect to `/crm/people` via client-side `goto()`. The `/crm/relationships` page SHALL display three relationship views (Person ↔ Person, Org → Person, Org ↔ Org) as internal sub-tabs, with Person ↔ Person as the default active tab.

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

#### Scenario: Navigate to /crm/relationships
- **WHEN** a user navigates to `/crm/relationships`
- **THEN** the Relationships page loads within the CRM layout showing three sub-tabs for Person ↔ Person, Org → Person, and Org ↔ Org relationship management

#### Scenario: Relationships page defaults to Person ↔ Person tab
- **WHEN** the user first navigates to `/crm/relationships`
- **THEN** the Person ↔ Person tab is active and its content is displayed

#### Scenario: Switch between relationship sub-tabs
- **WHEN** the user clicks the Org ↔ Org sub-tab on the Relationships page
- **THEN** the Org ↔ Org relationship view is displayed without a page navigation
