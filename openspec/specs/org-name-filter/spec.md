### Requirement: Organization list name filter input
The system SHALL display a text input above the Organizations list that filters the displayed organizations by name.

#### Scenario: Filter input is present and empty by default
- **WHEN** the Organizations page loads
- **THEN** a text input with placeholder text is visible above the list, and the full organizations list is displayed

#### Scenario: Typing filters the list by organization name
- **WHEN** the user types "acme" into the filter input
- **THEN** only organizations whose name contains "acme" (case-insensitive) are displayed

#### Scenario: No matches shows empty list
- **WHEN** the user types a query that matches no organization name
- **THEN** no organizations are displayed in the list

### Requirement: Filter persists through organization selection
The system SHALL NOT clear the filter input when the user selects an organization from the filtered list.

#### Scenario: Selecting an organization keeps the filter active
- **WHEN** the user has filtered the list and clicks on an organization
- **THEN** the organization's detail panel loads, and the filter input retains its value and the list remains filtered

### Requirement: Clearing the filter restores the full list
The system SHALL restore the full (unfiltered) organizations list when the filter input is cleared.

#### Scenario: Clearing filter text shows all organizations
- **WHEN** the user clears the filter input
- **THEN** all organizations are displayed in their default sorted order
