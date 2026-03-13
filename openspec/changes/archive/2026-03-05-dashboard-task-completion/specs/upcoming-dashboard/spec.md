## MODIFIED Requirements

### Requirement: Upcoming store supports task removal
The upcoming store SHALL provide a `removeUpcomingTask(taskId)` function that removes a task from the store by ID, enabling optimistic UI updates when tasks are completed from the dashboard.

#### Scenario: Remove a task from the upcoming store
- **WHEN** `removeUpcomingTask` is called with a task ID
- **THEN** the task with that ID SHALL be removed from the store's task list
- **THEN** the dashboard view SHALL reactively update to no longer show that task
