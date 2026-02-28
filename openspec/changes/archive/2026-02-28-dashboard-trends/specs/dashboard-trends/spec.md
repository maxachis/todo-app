## ADDED Requirements

### Requirement: Trends API returns weekly interaction counts
The system SHALL expose a `GET /api/dashboard/trends/` endpoint that returns aggregated trend data. The response SHALL include an `interactions_per_week` array containing objects with `week_start` (ISO date string, Monday) and `count` (integer) for each of the last 12 complete weeks plus the current partial week, sorted chronologically.

#### Scenario: Interactions exist across multiple weeks
- **WHEN** the client sends `GET /api/dashboard/trends/`
- **AND** there are interactions with dates spanning several weeks
- **THEN** the response includes `interactions_per_week` as an array of `{week_start, count}` objects for the last 12 weeks plus the current week
- **AND** weeks with no interactions have `count: 0`

#### Scenario: No interactions exist
- **WHEN** the client sends `GET /api/dashboard/trends/`
- **AND** there are no interactions in the database
- **THEN** the response includes `interactions_per_week` with 13 entries all having `count: 0`

### Requirement: Trends API returns weekly task completion counts
The `GET /api/dashboard/trends/` response SHALL include a `tasks_completed_per_week` array containing objects with `week_start` (ISO date string, Monday) and `count` (integer) for each of the last 12 complete weeks plus the current partial week, based on the `completed_at` timestamp of tasks.

#### Scenario: Tasks completed across multiple weeks
- **WHEN** the client sends `GET /api/dashboard/trends/`
- **AND** there are tasks with `completed_at` timestamps spanning several weeks
- **THEN** the response includes `tasks_completed_per_week` as an array of `{week_start, count}` objects
- **AND** weeks with no completions have `count: 0`

#### Scenario: No tasks have been completed
- **WHEN** the client sends `GET /api/dashboard/trends/`
- **AND** no tasks have a non-null `completed_at`
- **THEN** the response includes `tasks_completed_per_week` with 13 entries all having `count: 0`

### Requirement: Trends API returns follow-up compliance score
The `GET /api/dashboard/trends/` response SHALL include a `follow_up_compliance` object with `on_track` (integer count of people within their cadence), `total` (integer count of people with a `follow_up_cadence_days` set), and `overdue_count` (integer count of people past their cadence).

#### Scenario: Mix of on-track and overdue contacts
- **WHEN** the client sends `GET /api/dashboard/trends/`
- **AND** 10 people have `follow_up_cadence_days` set, 7 have been contacted within cadence, 3 are overdue
- **THEN** the response includes `follow_up_compliance: {on_track: 7, total: 10, overdue_count: 3}`

#### Scenario: Person with cadence but no interactions
- **WHEN** a person has `follow_up_cadence_days` set but no interactions recorded
- **THEN** that person counts as overdue in the compliance score

#### Scenario: No people have cadence set
- **WHEN** no people have `follow_up_cadence_days` set
- **THEN** the response includes `follow_up_compliance: {on_track: 0, total: 0, overdue_count: 0}`

### Requirement: Trends sub-tab renders interactions per week chart
The Dashboard Trends sub-tab SHALL render a bar chart showing interactions per week for the last 12 weeks plus the current week. The x-axis SHALL show week labels, the y-axis SHALL show count. The chart SHALL use the app's theme colors and respond to theme changes.

#### Scenario: Trends tab displays interactions chart
- **WHEN** the user navigates to the Dashboard and selects the Trends tab
- **THEN** a bar chart titled "Interactions per Week" is displayed
- **AND** each bar represents one week's interaction count

#### Scenario: Chart responds to dark mode
- **WHEN** the user switches to dark mode while viewing the Trends tab
- **THEN** the chart colors update to match the dark theme

### Requirement: Trends sub-tab renders tasks completed per week chart
The Dashboard Trends sub-tab SHALL render a bar chart showing tasks completed per week for the last 12 weeks plus the current week, using the same layout and styling conventions as the interactions chart.

#### Scenario: Trends tab displays tasks completed chart
- **WHEN** the user navigates to the Dashboard and selects the Trends tab
- **THEN** a bar chart titled "Tasks Completed per Week" is displayed alongside the interactions chart

### Requirement: Trends sub-tab renders follow-up compliance summary
The Dashboard Trends sub-tab SHALL display a follow-up compliance summary showing "X of Y contacts on track" where X is the on-track count and Y is the total count of people with cadence set. The summary SHALL visually indicate the compliance ratio (e.g., as a progress indicator or colored text).

#### Scenario: Compliance summary with mixed status
- **WHEN** the trends API returns `follow_up_compliance: {on_track: 7, total: 10, overdue_count: 3}`
- **THEN** the summary displays "7 of 10 contacts on track"
- **AND** a visual indicator reflects 70% compliance

#### Scenario: No contacts with cadence
- **WHEN** the trends API returns `follow_up_compliance: {on_track: 0, total: 0, overdue_count: 0}`
- **THEN** the summary displays a message like "No follow-up cadences configured"
