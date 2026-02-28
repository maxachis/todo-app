## ADDED Requirements

### Requirement: People list name filter input
The system SHALL display a text input in the People list panel's sort bar that filters the displayed people by name.

#### Scenario: Filter input is present and empty by default
- **WHEN** the People page loads
- **THEN** a text input with placeholder text is visible in the sort bar, and the full people list is displayed

#### Scenario: Typing filters the list by first or last name
- **WHEN** the user types "chen" into the filter input
- **THEN** only people whose first name or last name contains "chen" (case-insensitive) are displayed

#### Scenario: Filter matches on first name
- **WHEN** the user types "sarah" into the filter input
- **THEN** people whose first name contains "sarah" (case-insensitive) are displayed, regardless of last name

#### Scenario: Filter matches on last name
- **WHEN** the user types "adams" into the filter input
- **THEN** people whose last name contains "adams" (case-insensitive) are displayed, regardless of first name

#### Scenario: No matches shows empty list
- **WHEN** the user types a query that matches no person's first or last name
- **THEN** no people are displayed in the list

### Requirement: Filter composes with sort
The system SHALL apply the active sort field and direction to the filtered subset of people.

#### Scenario: Filtered results respect active sort
- **WHEN** the user has typed a filter query and the sort field is Last Name ascending
- **THEN** only matching people are displayed, sorted by last name in ascending order

#### Scenario: Changing sort while filtered
- **WHEN** the user changes the sort field or direction while a filter is active
- **THEN** the filtered results re-sort according to the new sort settings

### Requirement: Filter persists through person selection
The system SHALL NOT clear the filter input when the user selects a person from the filtered list.

#### Scenario: Selecting a person keeps the filter active
- **WHEN** the user has filtered the list and clicks on a person
- **THEN** the person's detail panel loads, and the filter input retains its value and the list remains filtered

### Requirement: Clearing the filter restores the full list
The system SHALL restore the full (unfiltered) people list when the filter input is cleared.

#### Scenario: Clearing filter text shows all people
- **WHEN** the user clears the filter input (backspace or select-all + delete)
- **THEN** all people are displayed, sorted by the active sort settings
