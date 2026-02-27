## Why

When a tag is added to or removed from a task via the detail panel, the task list (center panel) does not reflect the change until the list is reloaded. This breaks the optimistic-UI pattern used by every other task mutation and makes tagging feel unresponsive.

## What Changes

- After a tag is added or removed, update the task object inside `listsStore` so that `TaskRow` components immediately render the new tag set.
- Align the tag mutation flow with the existing `updateTask()` pattern, which already calls `replaceTaskInList()` to keep both stores in sync.

## Non-goals

- Changing the tag API response shape or backend logic.
- Adding tag management UI (create/rename/delete tags outside of tasks).
- Modifying how `selectTask()` works globally — the fix is scoped to tag operations.

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `svelte-frontend`: Tag add/remove operations must propagate to the list store, not just the detail store.

## Impact

- **Frontend store layer** (`frontend/src/lib/stores/tasks.ts`): New or updated helper to refresh a task in `listsStore` after tag mutation.
- **Task detail component** (`frontend/src/lib/components/tasks/TaskDetail.svelte`): `addTag()` and `removeTag()` handlers updated to trigger the list-store refresh.
- No backend, API, or database changes required.
