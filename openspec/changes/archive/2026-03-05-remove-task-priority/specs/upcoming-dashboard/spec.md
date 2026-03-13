## MODIFIED Requirements

### Requirement: API returns upcoming tasks
The system SHALL expose a `GET /api/upcoming/` endpoint that returns all incomplete tasks with a non-null due date, sorted by `due_date` ascending then `due_time` ascending (nulls last). Each task object SHALL include `id`, `title`, `due_date`, `due_time`, `is_pinned`, `list_id`, `list_name`, `list_emoji`, `section_id`, `section_name`, and `tags` (array of tag name strings).

#### Scenario: Tasks with due dates exist
- **WHEN** the client sends `GET /api/upcoming/`
- **AND** there are incomplete tasks with due dates
- **THEN** the response status is 200
- **AND** the response body is a JSON array of task objects sorted by `due_date` ascending, then `due_time` ascending (null times sort after non-null times)

#### Scenario: No tasks with due dates
- **WHEN** the client sends `GET /api/upcoming/`
- **AND** no incomplete tasks have a due date set
- **THEN** the response status is 200
- **AND** the response body is an empty JSON array `[]`

#### Scenario: Completed tasks are excluded
- **WHEN** the client sends `GET /api/upcoming/`
- **AND** a task has `is_completed=True` and a non-null due date
- **THEN** that task SHALL NOT appear in the response

#### Scenario: Tasks without due dates are excluded
- **WHEN** the client sends `GET /api/upcoming/`
- **AND** a task has `due_date=null`
- **THEN** that task SHALL NOT appear in the response

### Requirement: Each dashboard task row shows relevant details
Each task row on the dashboard SHALL display the task title, due date (formatted), due time (if set), and the list name with emoji and section name as context.

#### Scenario: Task with all fields populated
- **WHEN** a task has title "Buy groceries", due_date "2026-02-21", due_time "14:00", list "Personal" with emoji "🏠", section "Errands"
- **THEN** the row displays the title, formatted date, formatted time, and "🏠 Personal / Errands"

#### Scenario: Task with no due time
- **WHEN** a task has a due_date but due_time is null
- **THEN** the row displays the date without a time component
