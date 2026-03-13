## ADDED Requirements

### Requirement: Dashboard task rows display a completion checkbox
Each task row on the Dashboard Upcoming tab SHALL display a checkbox to the left of the task title. The checkbox SHALL be unchecked for all displayed tasks (completed tasks are not shown on the dashboard).

#### Scenario: Checkbox is visible on task rows
- **WHEN** the Dashboard Upcoming tab is displayed with tasks
- **THEN** each task row SHALL display an unchecked checkbox before the task title

### Requirement: Clicking the checkbox completes the task
Clicking the checkbox on a dashboard task row SHALL mark the task as completed via the API and remove it from the dashboard view.

#### Scenario: Complete a non-recurring task
- **WHEN** user clicks the checkbox on a non-recurring task
- **THEN** the task SHALL be immediately removed from the dashboard list
- **THEN** the task SHALL be marked as completed via the API

#### Scenario: Complete a recurring task
- **WHEN** user clicks the checkbox on a recurring task
- **THEN** the task SHALL be immediately removed from the dashboard list
- **THEN** the task SHALL be marked as completed via the API
- **THEN** an undo toast SHALL appear allowing the user to reverse the completion

#### Scenario: API failure on completion
- **WHEN** user clicks the checkbox and the API call fails
- **THEN** the dashboard SHALL reload the upcoming tasks list to restore the task

### Requirement: Checkbox click does not navigate away
Clicking the checkbox area SHALL NOT trigger navigation to the Tasks view. Only clicking the task title or other row content SHALL navigate.

#### Scenario: Click checkbox without navigation
- **WHEN** user clicks the checkbox on a task row
- **THEN** the browser SHALL NOT navigate to the Tasks view
- **THEN** the task SHALL be completed as described above

### Requirement: Undo restores task to dashboard
When a recurring task completion is undone via the toast action, the task SHALL reappear on the dashboard.

#### Scenario: Undo recurring task completion
- **WHEN** user completes a recurring task and clicks undo on the toast
- **THEN** the original task SHALL be uncompleted via the API
- **THEN** the dashboard upcoming list SHALL refresh to show the restored task
