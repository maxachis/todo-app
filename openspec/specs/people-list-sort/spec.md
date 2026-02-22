### Requirement: People list sort field selection
The system SHALL provide a sort control on the People list panel that allows the user to select a sort field from: Last Name, First Name, and Follow Up Days.

#### Scenario: Default sort is Last Name ascending
- **WHEN** the People page loads
- **THEN** the people list is sorted by Last Name in ascending (A-Z) order and the sort control indicates Last Name as the active field

#### Scenario: Sort by First Name
- **WHEN** the user selects "First Name" from the sort field selector
- **THEN** the people list re-sorts by first name in the current sort direction

#### Scenario: Sort by Follow Up Days
- **WHEN** the user selects "Follow Up Days" from the sort field selector
- **THEN** the people list re-sorts by follow_up_cadence_days in the current sort direction, with people who have no follow-up cadence appearing at the end of the list

### Requirement: People list sort direction toggle
The system SHALL provide a toggle button that switches the sort direction between ascending and descending, with a visual indicator showing the current direction.

#### Scenario: Toggle from ascending to descending
- **WHEN** the sort direction is ascending and the user clicks the direction toggle
- **THEN** the people list reverses to descending order and the toggle visually indicates descending

#### Scenario: Toggle from descending to ascending
- **WHEN** the sort direction is descending and the user clicks the direction toggle
- **THEN** the people list reverses to ascending order and the toggle visually indicates ascending

### Requirement: Sort applies to newly created people
The system SHALL apply the active sort field and direction when a new person is added to the list.

#### Scenario: New person inserted in sorted position
- **WHEN** a new person is created while the list is sorted by First Name descending
- **THEN** the new person appears in the correct position according to the active sort field and direction

### Requirement: Null follow-up cadence sorts to end
The system SHALL sort people with a null follow_up_cadence_days value to the end of the list when sorting by Follow Up Days, regardless of sort direction.

#### Scenario: Null cadence at end in ascending order
- **WHEN** the sort field is Follow Up Days and direction is ascending
- **THEN** people with a set cadence appear first (smallest to largest) and people with no cadence appear at the end

#### Scenario: Null cadence at end in descending order
- **WHEN** the sort field is Follow Up Days and direction is descending
- **THEN** people with a set cadence appear first (largest to smallest) and people with no cadence appear at the end
