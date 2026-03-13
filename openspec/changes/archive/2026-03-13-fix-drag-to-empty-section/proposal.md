## Why

Dragging a task into an empty section doesn't work. The `dndzone` (from svelte-dnd-action) renders inside a `<div>` that has zero height when the section has no tasks, so there's no droppable area for the library to detect.

## What Changes

- Add a `min-height` to the `.task-dnd-zone` container so empty sections have a visible drop target area
- The min-height should only apply when the zone is empty (during a drag operation, the library needs space to detect the zone)

## Non-goals

- No changes to the drag-and-drop library or task reordering logic
- No changes to the backend API

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `drag-drop-subtask-nesting`: The dndzone container needs a minimum height so empty sections are valid drop targets

## Impact

- **Frontend**: `frontend/src/lib/components/tasks/TaskList.svelte` — add min-height to `.task-dnd-zone` or the wrapping `.task-list` when empty
