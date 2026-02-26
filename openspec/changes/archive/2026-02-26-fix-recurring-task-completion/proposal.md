## Why

Completing a recurring task causes three bugs: (1) the page briefly goes blank due to a full list re-fetch that forces all svelte-dnd-action DND zones to tear down and rebuild, (2) the new occurrence is positioned at the bottom of the section instead of replacing the completed task in-place, and (3) clicking "Undo" on the completion toast un-completes the original task but leaves the newly created next occurrence orphaned, resulting in duplicate tasks.

## What Changes

- **Backend: Position next occurrence in-place** — When creating the next occurrence of a recurring task, use the completed task's position (not `max_pos + 10`) so the new task appears in the same spot.
- **Backend: Return next occurrence data in complete response** — Include the full serialized next occurrence task in the `/tasks/{id}/complete/` API response so the frontend can update optimistically without a full list re-fetch.
- **Frontend: Optimistic store update on completion** — Replace the full `refreshListDetail()` call with targeted store mutations: remove the completed task from the active list and insert the new occurrence at the same position.
- **Frontend: Fix undo for recurring tasks** — When undoing completion of a recurring task, delete the next occurrence before un-completing the original task. Add a new `DELETE /tasks/{id}/` call for the next occurrence in the undo handler.
- **Backend: Add uncomplete-with-cleanup endpoint** — Extend the uncomplete endpoint (or add a parameter) to accept an optional `delete_next_occurrence_id` that deletes the orphaned next occurrence atomically with un-completing the original.

## Non-goals

- Changing the recurrence date calculation logic (that works correctly).
- Adding new recurrence types.
- Modifying the task detail panel behavior during completion.
- Addressing Upcoming page completion (it doesn't have a completion checkbox).

## Capabilities

### New Capabilities

_None — this is a bug fix within existing capabilities._

### Modified Capabilities

- `task-recurrence`: Next occurrence positioning changes from end-of-section to in-place. Completion API response now includes full next occurrence data. Undo behavior for recurring task completion now cleans up the next occurrence.

## Impact

- **Backend**: `tasks/models.py` (Task.complete position logic), `tasks/api/tasks.py` (complete_task response, uncomplete_task cleanup)
- **Frontend**: `frontend/src/lib/stores/tasks.ts` (completeTask, uncompleteTask optimistic updates), `frontend/src/lib/components/tasks/TaskRow.svelte` (undo handler), `frontend/src/lib/api/index.ts` (updated complete response type)
- **API contract**: `/tasks/{id}/complete/` response gains a `next_occurrence` field (full task object). `/tasks/{id}/uncomplete/` gains optional `delete_next_occurrence_id` query param.
