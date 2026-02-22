### Requirement: Follow-up status display in People list
The system SHALL display a follow-up status indicator on each person in the People list who has a `follow_up_cadence_days` value set. The indicator SHALL show the number of days since the last interaction and the cadence value. The status tier SHALL be computed as: overdue (days since > cadence), due soon (days since > 80% of cadence), or on track (days since <= 80% of cadence). People with a cadence but no recorded interactions SHALL be shown as overdue. People without a cadence SHALL show no status indicator.

#### Scenario: Person is overdue for follow-up
- **WHEN** a person has `follow_up_cadence_days` of 14 and their last interaction was 20 days ago
- **THEN** the People list item shows an overdue indicator with "20d / 14d"

#### Scenario: Person is due soon for follow-up
- **WHEN** a person has `follow_up_cadence_days` of 14 and their last interaction was 12 days ago
- **THEN** the People list item shows a due-soon indicator with "12d / 14d"

#### Scenario: Person is on track for follow-up
- **WHEN** a person has `follow_up_cadence_days` of 14 and their last interaction was 5 days ago
- **THEN** the People list item shows an on-track indicator with "5d / 14d"

#### Scenario: Person has cadence but no interactions
- **WHEN** a person has `follow_up_cadence_days` set but no interaction records exist
- **THEN** the People list item shows an overdue indicator with "never / {cadence}d"

#### Scenario: Person has no cadence set
- **WHEN** a person has `follow_up_cadence_days` of null
- **THEN** no follow-up status indicator is shown on the list item

### Requirement: Sort People list by follow-up urgency
The system SHALL provide a "Follow-up status" sort option in the People sort bar. When selected, people SHALL be sorted by overdue ratio (days since last interaction divided by cadence) in descending order, so the most overdue people appear first. People with no cadence SHALL sort to the bottom. People with a cadence but no interactions SHALL sort to the top.

#### Scenario: Sort by follow-up status descending
- **WHEN** the user selects "Follow-up status" from the sort field dropdown
- **THEN** people are ordered by overdue ratio descending, with no-cadence people at the bottom

#### Scenario: Sort by follow-up status ascending
- **WHEN** the user selects "Follow-up status" and toggles sort direction to ascending
- **THEN** people are ordered by overdue ratio ascending, with no-cadence people at the bottom

### Requirement: Last interaction summary in People detail panel
The system SHALL display the most recent interaction date and type in the People detail panel when a person is selected and has at least one interaction recorded.

#### Scenario: Person has interactions
- **WHEN** a person is selected and their last interaction was a "DM" on "2026-01-14"
- **THEN** the detail panel shows "Last interaction: Jan 14 - DM"

#### Scenario: Person has no interactions
- **WHEN** a person is selected and has no interaction records
- **THEN** no last interaction summary is shown (or shows "No interactions recorded")

#### Scenario: Person is overdue with interactions
- **WHEN** a person is selected, has a cadence set, and is overdue
- **THEN** the detail panel shows an overdue warning alongside the last interaction summary

### Requirement: Quick-log interaction from People detail panel
The system SHALL provide an inline form in the People detail panel to log a new interaction for the selected person. The form SHALL include an interaction type selector and a date field (defaulting to today). Submitting the form SHALL create the interaction via the API and refresh the people list to reflect updated follow-up status.

#### Scenario: Log interaction via quick-log form
- **WHEN** the user selects a person, fills in the quick-log form with type "DM" and date "2026-02-22", and submits
- **THEN** an interaction is created for the selected person via `POST /api/interactions/` and the people list reloads with updated status

#### Scenario: Quick-log form defaults to today's date
- **WHEN** the user selects a person and the quick-log form appears
- **THEN** the date field is pre-filled with today's date

#### Scenario: Quick-log form clears after submission
- **WHEN** the user submits the quick-log form successfully
- **THEN** the form fields reset and the person's follow-up status updates in the list
