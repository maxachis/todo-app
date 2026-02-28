## MODIFIED Requirements

### Requirement: Network navigation in Svelte UI
The system SHALL provide Svelte routes and navigation entries for CRM (People, Organizations, Interactions, Leads) and Network (Relationships, Graph) as nested route groups under `/crm` and `/network` respectively. The former standalone routes (`/people`, `/organizations`, `/interactions`, `/relationships`, `/graph`, `/leads`) SHALL be removed.

#### Scenario: Navigate to People view
- **WHEN** a user selects CRM from the main navigation and then the People sub-tab
- **THEN** the People view loads at `/crm/people` in the Svelte app without full-page reload

#### Scenario: Navigate to Organizations view
- **WHEN** a user selects CRM from the main navigation and then the Orgs sub-tab
- **THEN** the Organizations view loads at `/crm/orgs` without full-page reload

#### Scenario: Navigate to Interactions view
- **WHEN** a user selects CRM from the main navigation and then the Interactions sub-tab
- **THEN** the Interactions view loads at `/crm/interactions` without full-page reload

#### Scenario: Navigate to Leads view
- **WHEN** a user selects CRM from the main navigation and then the Leads sub-tab
- **THEN** the Leads view loads at `/crm/leads` without full-page reload

#### Scenario: Navigate to Relationships view
- **WHEN** a user selects Network from the main navigation and then the Relationships sub-tab
- **THEN** the Relationships view loads at `/network/relationships` without full-page reload

#### Scenario: Navigate to Graph view
- **WHEN** a user selects Network from the main navigation and then the Graph sub-tab
- **THEN** the Graph view loads at `/network/graph` without full-page reload

#### Scenario: Old standalone routes are removed
- **WHEN** a user attempts to navigate to `/people`, `/organizations`, `/interactions`, `/relationships`, `/graph`, or `/leads`
- **THEN** the route does not resolve (SvelteKit 404 or equivalent)
