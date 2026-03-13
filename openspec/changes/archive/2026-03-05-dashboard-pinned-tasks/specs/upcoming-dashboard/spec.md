## MODIFIED Requirements

### Requirement: API returns upcoming tasks
The system SHALL expose a `GET /api/upcoming/` endpoint that returns all incomplete tasks that either have a non-null due date OR are pinned (`is_pinned=True`). Results SHALL be sorted by `due_date` ascending then `due_time` ascending (nulls last), with pinned tasks without due dates sorted after all dated tasks. Each task object SHALL include `id`, `title`, `due_date` (string or null), `due_time`, `priority`, `is_pinned`, `list_id`, `list_name`, `list_emoji`, `section_id`, `section_name`, and `tags` (array of tag name strings).

#### Scenario: Tasks with due dates exist
- **WHEN** the client sends `GET /api/upcoming/`
- **AND** there are incomplete tasks with due dates
- **THEN** the response status is 200
- **AND** the response body is a JSON array of task objects sorted by `due_date` ascending, then `due_time` ascending (null times sort after non-null times)

#### Scenario: Pinned tasks without due dates are included
- **WHEN** the client sends `GET /api/upcoming/`
- **AND** there are incomplete pinned tasks without due dates
- **THEN** those tasks are included in the response with `due_date: null`
- **AND** they appear after all tasks that have due dates

#### Scenario: No tasks with due dates and no pinned tasks
- **WHEN** the client sends `GET /api/upcoming/`
- **AND** no incomplete tasks have a due date set
- **AND** no incomplete tasks are pinned
- **THEN** the response status is 200
- **AND** the response body is an empty JSON array `[]`

#### Scenario: Completed tasks are excluded
- **WHEN** the client sends `GET /api/upcoming/`
- **AND** a task has `is_completed=True` and a non-null due date
- **THEN** that task SHALL NOT appear in the response

#### Scenario: Completed pinned tasks are excluded
- **WHEN** the client sends `GET /api/upcoming/`
- **AND** a task has `is_completed=True` and `is_pinned=True`
- **THEN** that task SHALL NOT appear in the response

#### Scenario: Tasks without due dates and not pinned are excluded
- **WHEN** the client sends `GET /api/upcoming/`
- **AND** a task has `due_date=null` and `is_pinned=False`
- **THEN** that task SHALL NOT appear in the response

### Requirement: Dashboard page displays tasks grouped by time horizon
The frontend SHALL render the Upcoming sub-tab within the Dashboard page at `/dashboard`. The sub-tab groups tasks into time-based sections: "Overdue", "Today", "Tomorrow", "This Week", and "Later". Grouping SHALL be based on the client's local date compared to each task's `due_date`. Tasks with `due_date: null` SHALL NOT be placed into any time-horizon group. The Dashboard page SHALL include a sub-tab bar with "Upcoming" and "Trends" tabs, controlled via a `tab` query parameter (defaulting to `upcoming`).

#### Scenario: Tasks span multiple time horizons
- **WHEN** the user navigates to `/dashboard` or `/dashboard?tab=upcoming`
- **AND** there are tasks with due dates in the past, today, tomorrow, this week, and next week
- **THEN** the page displays a sub-tab bar with "Upcoming" active
- **AND** tasks are grouped under the correct time-horizon headers
