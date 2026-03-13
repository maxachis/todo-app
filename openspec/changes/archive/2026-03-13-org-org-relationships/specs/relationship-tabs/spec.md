## ADDED Requirements

### Requirement: Tabbed layout for the Relationships page
The Relationships page SHALL use a tabbed layout with three tabs: "Person ↔ Person", "Org → Person", and "Org ↔ Org". Only one tab's content SHALL be visible at a time. The active tab SHALL be tracked via a reactive variable (not separate routes). Tab state (form values, filters, lists) SHALL be preserved when switching between tabs.

#### Scenario: Default tab on page load
- **WHEN** the user navigates to the Relationships page
- **THEN** the "Person ↔ Person" tab is active by default

#### Scenario: Switch between tabs
- **WHEN** the user clicks the "Org → Person" tab
- **THEN** the org-person content becomes visible and the person-person content is hidden

#### Scenario: Tab state preservation
- **WHEN** the user partially fills the person-person create form, switches to "Org ↔ Org", then switches back
- **THEN** the person-person form values are preserved

#### Scenario: Each tab has full-width layout
- **WHEN** any tab is active
- **THEN** the tab content uses the full available width (not split into columns)
