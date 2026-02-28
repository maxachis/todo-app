# Dashboard Follow-ups

## Purpose

Surface overdue CRM follow-ups on the Dashboard Upcoming sub-tab, enabling users to see which contacts need attention alongside their upcoming tasks.

## Requirements

### Requirement: Follow-ups due API endpoint
The system SHALL expose a `GET /api/dashboard/follow-ups-due/` endpoint that returns people who are past their `follow_up_cadence_days` threshold. Each entry SHALL include `person_id`, `first_name`, `last_name`, `follow_up_cadence_days`, `last_interaction_date` (ISO date string or null), and `days_overdue` (integer, how many days past cadence). Results SHALL be sorted by `days_overdue` descending (most overdue first).

#### Scenario: People overdue for follow-up
- **WHEN** the client sends `GET /api/dashboard/follow-ups-due/`
- **AND** a person has `follow_up_cadence_days` of 14 and their last interaction was 20 days ago
- **THEN** that person appears in the response with `days_overdue: 6` and `last_interaction_date` set to the interaction date

#### Scenario: Person with cadence but no interactions
- **WHEN** the client sends `GET /api/dashboard/follow-ups-due/`
- **AND** a person has `follow_up_cadence_days` set but no interactions recorded
- **THEN** that person appears in the response with `last_interaction_date: null` and `days_overdue` computed from their `created_at` date

#### Scenario: All contacts are on track
- **WHEN** the client sends `GET /api/dashboard/follow-ups-due/`
- **AND** all people with cadence set have been contacted within their window
- **THEN** the response is an empty array

#### Scenario: People without cadence are excluded
- **WHEN** the client sends `GET /api/dashboard/follow-ups-due/`
- **AND** a person has `follow_up_cadence_days` of null
- **THEN** that person does not appear in the response

### Requirement: Follow-ups due group in Upcoming sub-tab
The Dashboard Upcoming sub-tab SHALL display a "Follow-ups Due" group above the task time-horizon groups when there are people overdue for follow-up. Each row SHALL show the person's name, days since last interaction, cadence, and days overdue. The group SHALL be visually distinct from task groups to differentiate CRM items from tasks.

#### Scenario: Overdue follow-ups exist
- **WHEN** the user views the Dashboard Upcoming sub-tab
- **AND** 3 people are overdue for follow-up
- **THEN** a "Follow-ups Due" group appears above Overdue/Today/Tomorrow task groups
- **AND** each row shows the person's name and overdue status (e.g., "20d / 14d cadence -- 6d overdue")

#### Scenario: No overdue follow-ups
- **WHEN** the user views the Dashboard Upcoming sub-tab
- **AND** no people are overdue for follow-up
- **THEN** the "Follow-ups Due" group is not displayed

### Requirement: Follow-up row links to person
Each follow-up row in the "Follow-ups Due" group SHALL be clickable and navigate to the People page filtered or scrolled to that person.

#### Scenario: User clicks a follow-up row
- **WHEN** the user clicks a follow-up row for "Jane Smith"
- **THEN** the app navigates to `/people?person={person_id}`
