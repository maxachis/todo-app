## MODIFIED Requirements

### Requirement: Drag-and-drop with svelte-dnd-action
The system SHALL use svelte-dnd-action for section and list drag-and-drop interactions. Task drag-and-drop SHALL use native HTML5 drag-and-drop with midpoint-based drop detection instead of svelte-dnd-action, to support both reordering (place before) and nesting (make subtask) from a single drag gesture. Drop events SHALL update the Svelte store optimistically, then persist via API.

#### Scenario: Reorder task within section
- **WHEN** the user drags a task and drops it above the midpoint of another task in the same section
- **THEN** the task is placed before the drop target at the same nesting level and the new position persists via API

#### Scenario: Task drag lock during finalize
- **WHEN** a task drag finalize/persist cycle is in progress
- **THEN** initiating another task drag is disabled until the first cycle completes

#### Scenario: Drag visual tracks cursor
- **WHEN** the user drags a task
- **THEN** the browser's native drag ghost follows the cursor

#### Scenario: Move task to different section
- **WHEN** the user drags a task and drops it above the midpoint of a task in a different section
- **THEN** the task appears in the new section at the drop target's level and the section/position change persists

#### Scenario: Nest task as subtask
- **WHEN** the user drags a task and drops it below the midpoint of another task
- **THEN** the dragged task becomes a subtask of the drop target, updating visually and persisting via API

#### Scenario: Midpoint controls drop intent on task rows
- **WHEN** the user drags task A over task B
- **THEN** dropping above task B's midpoint inserts task A before task B at task B's current hierarchy level, and dropping below task B's midpoint nests task A under task B

#### Scenario: Promote subtask
- **WHEN** the user drags a subtask and drops it above the midpoint of a top-level task
- **THEN** the subtask becomes a top-level task in the section

#### Scenario: Move task to different list via sidebar
- **WHEN** the user drags a task onto a list in the sidebar
- **THEN** the task moves to the first section of that list, with all subtasks following

#### Scenario: API failure rolls back
- **WHEN** a drag operation succeeds visually but the API call fails
- **THEN** the store reverts to the pre-drag state and a toast shows an error message

#### Scenario: Reorder sections within list
- **WHEN** the user drags a section to a new position within the list
- **THEN** the section order updates immediately via svelte-dnd-action and persists via API

#### Scenario: Reorder lists in sidebar
- **WHEN** the user drags a list to a new position in the sidebar
- **THEN** the list order updates immediately via svelte-dnd-action and persists via API
