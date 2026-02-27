## MODIFIED Requirements

### Requirement: Svelte store state management
The system SHALL manage application state using Svelte writable stores, one per resource type, with co-located async mutation functions. Tag add and remove operations SHALL update the task in both `selectedTaskDetail` and `listsStore` so that all subscribed components (detail panel and task list rows) re-render with current tag data.

#### Scenario: Store updates propagate to all subscribers
- **WHEN** a task is completed via the store's `completeTask()` function
- **THEN** all components subscribed to the tasks store re-render with the updated state

#### Scenario: Optimistic updates with rollback
- **WHEN** a mutation function updates the store optimistically and the API call fails
- **THEN** the store reverts to the previous state and a toast shows the error

#### Scenario: Tag add updates task in list store
- **WHEN** a user adds a tag to a task via the detail panel
- **THEN** the task object in `listsStore` SHALL be replaced with the refreshed task, causing `TaskRow` to display the new tag immediately

#### Scenario: Tag remove updates task in list store
- **WHEN** a user removes a tag from a task via the detail panel
- **THEN** the task object in `listsStore` SHALL be replaced with the refreshed task, causing `TaskRow` to remove the tag immediately
