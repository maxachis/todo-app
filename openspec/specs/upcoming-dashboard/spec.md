### Requirement: API returns upcoming tasks
The system SHALL expose a `GET /api/upcoming/` endpoint that returns all incomplete tasks that either have a non-null due date OR are pinned (`is_pinned=True`). Results SHALL be sorted by `due_date` ascending then `due_time` ascending (nulls last), with pinned tasks without due dates sorted after all dated tasks. Each task object SHALL include `id`, `title`, `due_date` (string or null), `due_time`, `is_pinned`, `list_id`, `list_name`, `list_emoji`, `section_id`, `section_name`, and `tags` (array of tag name strings).

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

### Requirement: Each upcoming task includes list and section context
Each task returned by the upcoming endpoint SHALL include `list_id`, `list_name`, `list_emoji`, `section_id`, and `section_name` so the frontend can display where the task lives without additional API calls.

#### Scenario: Task belongs to a list and section
- **WHEN** the client sends `GET /api/upcoming/`
- **THEN** each task in the response includes `list_id`, `list_name`, `list_emoji` from the task's section's list
- **AND** each task includes `section_id` and `section_name` from the task's section

### Requirement: Dashboard page displays tasks grouped by time horizon
The frontend SHALL render the Upcoming sub-tab within the Dashboard page at `/dashboard`. The sub-tab groups tasks into time-based sections: "Overdue", "Today", "Tomorrow", "This Week", and "Later". Grouping SHALL be based on the client's local date compared to each task's `due_date`. Tasks with `due_date: null` SHALL NOT be placed into any time-horizon group. The Dashboard page SHALL include a sub-tab bar with "Upcoming" and "Trends" tabs, controlled via a `tab` query parameter (defaulting to `upcoming`).

#### Scenario: Tasks span multiple time horizons
- **WHEN** the user navigates to `/dashboard` or `/dashboard?tab=upcoming`
- **AND** there are tasks with due dates in the past, today, tomorrow, this week, and next week
- **THEN** the page displays a sub-tab bar with "Upcoming" active
- **AND** group headers for "Overdue", "Today", "Tomorrow", "This Week", and "Later"
- **AND** each task appears under its correct group

#### Scenario: A group has no tasks
- **WHEN** the user navigates to `/dashboard?tab=upcoming`
- **AND** no tasks are overdue
- **THEN** the "Overdue" group header SHALL NOT be displayed

#### Scenario: No tasks have due dates and no follow-ups due
- **WHEN** the user navigates to `/dashboard?tab=upcoming`
- **AND** the upcoming API returns an empty array
- **AND** no people are overdue for follow-up
- **THEN** the page displays an empty state message

#### Scenario: User switches between sub-tabs
- **WHEN** the user clicks the "Trends" sub-tab
- **THEN** the URL updates to `/dashboard?tab=trends`
- **AND** the Trends content is displayed
- **AND** the browser back button returns to the previous tab

### Requirement: Each dashboard task row shows relevant details
Each task row on the dashboard SHALL display the task title, due date (formatted), due time (if set), and the list name with emoji and section name as context.

#### Scenario: Task with all fields populated
- **WHEN** a task has title "Buy groceries", due_date "2026-02-21", due_time "14:00", list "Personal" with emoji "🏠", section "Errands"
- **THEN** the row displays the title, formatted date, formatted time, and "🏠 Personal / Errands"

#### Scenario: Task with no due time
- **WHEN** a task has a due_date but due_time is null
- **THEN** the row displays the date without a time component

### Requirement: Dashboard task links to its list
Each task on the dashboard SHALL be clickable and navigate the user to the main tasks view with that task's list selected and the task highlighted/selected.

#### Scenario: User clicks a task on the dashboard
- **WHEN** the user clicks a task row on the dashboard
- **THEN** the app navigates to `/?list={list_id}&task={task_id}`
- **AND** the main page selects the corresponding list and task

### Requirement: Upcoming store supports task removal
The upcoming store SHALL provide a `removeUpcomingTask(taskId)` function that removes a task from the store by ID, enabling optimistic UI updates when tasks are completed from the dashboard.

#### Scenario: Remove a task from the upcoming store
- **WHEN** `removeUpcomingTask` is called with a task ID
- **THEN** the task with that ID SHALL be removed from the store's task list
- **THEN** the dashboard view SHALL reactively update to no longer show that task

### Requirement: Navigation includes Upcoming tab
The top navigation bar SHALL include a "Dashboard" tab linking to `/dashboard`, placed between "Tasks" and "Projects" in the tab order. The tab SHALL be highlighted when the user is on the `/dashboard` route.

#### Scenario: User sees Dashboard tab
- **WHEN** the user views any page
- **THEN** the top navigation bar displays a "Dashboard" tab
- **AND** the tab is highlighted when the user is on the `/dashboard` route
