## Why

There is no way to delete a task from the detail panel. The only way to delete is via the keyboard shortcut (Backspace/Delete), which is not discoverable. Users need a visible, clickable delete action in the task detail view.

## What Changes

- Add a "Delete" button to the bottom of the task detail panel
- Clicking it shows a confirmation prompt, then deletes the task and clears the detail selection
- Reuses the existing `deleteTask` store function and `api.tasks.remove` endpoint — no backend changes needed

## Non-goals

- Bulk delete (multi-select)
- Undo/trash/soft-delete — deletion remains permanent as it is today
- Changing the existing keyboard shortcut behavior

## Capabilities

### New Capabilities

- `task-detail-delete`: Delete button in the task detail panel with confirmation dialog

### Modified Capabilities

## Impact

- `frontend/src/lib/components/tasks/TaskDetail.svelte` — add delete button and handler
- No backend, API, or data model changes
