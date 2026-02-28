## MODIFIED Requirements

### Requirement: Navigation includes Upcoming tab
The top navigation bar SHALL include a "Dashboard" tab linking to `/dashboard`, placed between "Tasks" and "Projects" in the tab order. The tab SHALL be highlighted when the user is on the `/dashboard` route.

#### Scenario: User sees Dashboard tab
- **WHEN** the user views any page
- **THEN** the top navigation bar displays a "Dashboard" tab
- **AND** the tab is highlighted when the user is on the `/dashboard` route

### Requirement: Dashboard page displays tasks grouped by time horizon
The frontend SHALL render the Upcoming sub-tab within the Dashboard page at `/dashboard`. The sub-tab groups tasks into time-based sections: "Overdue", "Today", "Tomorrow", "This Week", and "Later". Grouping SHALL be based on the client's local date compared to each task's `due_date`. The Dashboard page SHALL include a sub-tab bar with "Upcoming" and "Trends" tabs, controlled via a `tab` query parameter (defaulting to `upcoming`).

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
