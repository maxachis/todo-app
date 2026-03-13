## MODIFIED Requirements

### Requirement: Network navigation in Svelte UI
The system SHALL provide Svelte routes and navigation entries for CRM (People, Organizations, Interactions, Leads, Relationships) and Network (Graph) as nested route groups under `/crm` and `/network` respectively. The former standalone routes (`/people`, `/organizations`, `/interactions`, `/relationships`, `/graph`, `/leads`) SHALL be removed. The `/network/relationships` route SHALL be removed; relationships are managed at `/crm/relationships`.

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
- **WHEN** a user selects CRM from the main navigation and then the Relationships sub-tab
- **THEN** the Relationships view loads at `/crm/relationships` without full-page reload

#### Scenario: Navigate to Graph view
- **WHEN** a user selects Network from the main navigation
- **THEN** the Graph view loads at `/network/graph` without full-page reload

#### Scenario: Old standalone routes are removed
- **WHEN** a user attempts to navigate to `/people`, `/organizations`, `/interactions`, `/relationships`, `/graph`, or `/leads`
- **THEN** the route does not resolve (SvelteKit 404 or equivalent)

#### Scenario: Network relationships route is removed
- **WHEN** a user attempts to navigate to `/network/relationships`
- **THEN** the route does not resolve (SvelteKit 404 or equivalent)

## MODIFIED Requirements

### Requirement: Editable relationship notes on the Relationships page
The system SHALL allow users to edit the notes field on existing person-to-person, organization-to-person, and organization-to-organization relationships directly from the Relationships page at `/crm/relationships`.

#### Scenario: Edit person-to-person relationship notes via inline edit
- **WHEN** the user clicks on a person-to-person relationship's notes area (or edit button)
- **THEN** the notes area switches to an editable textarea pre-filled with the current notes text

#### Scenario: Save edited notes on blur
- **WHEN** the user edits relationship notes and blurs the textarea
- **THEN** the updated notes are saved via PUT to the appropriate relationship endpoint and the display updates immediately

#### Scenario: Cancel edit with Escape
- **WHEN** the user presses Escape while editing relationship notes
- **THEN** the edit is cancelled, the textarea reverts to the display view, and no API call is made

#### Scenario: Edit organization-to-person relationship notes
- **WHEN** the user clicks on an organization-to-person relationship's notes area (or edit button)
- **THEN** the notes area switches to an editable textarea, and saving works the same as for person-to-person relationships

#### Scenario: Edit organization-to-organization relationship notes
- **WHEN** the user clicks on an organization-to-organization relationship's notes area (or edit button)
- **THEN** the notes area switches to an editable textarea, and saving works the same as for other relationship types

#### Scenario: Add notes to a relationship with no existing notes
- **WHEN** a relationship has no notes and the user clicks the edit affordance
- **THEN** an empty textarea appears for entering notes, and saving persists the new notes
