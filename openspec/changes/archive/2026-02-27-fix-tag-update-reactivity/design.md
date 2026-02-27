## Context

The app uses a dual-store pattern for tasks: `listsStore` holds the full list/section/task tree (driving `TaskRow` components in the center panel), while `selectedTaskDetail` holds the currently selected task (driving the detail panel). Every mutation function (`updateTask`, `completeTask`, `uncompleteTask`, `deleteTask`) updates both stores. However, `addTag()` and `removeTag()` in `TaskDetail.svelte` only call `selectTask()`, which fetches the fresh task and writes to `selectedTaskDetail` — it never touches `listsStore`. This means tag changes appear in the detail panel but not in the task list.

## Goals / Non-Goals

**Goals:**
- Tag add/remove operations update the task in `listsStore` so `TaskRow` renders new tags immediately.
- Follow the existing pattern used by `updateTask()`: call `replaceTaskInList()` to sync the list store after mutation.

**Non-Goals:**
- Changing the tag API endpoints or response shapes.
- Adding an optimistic-update pattern for tags (the current approach waits for API confirmation, which is fine for this operation).
- Modifying `selectTask()` globally — the fix is scoped to tag operations.

## Decisions

**Re-fetch the full task after tag mutation, then update both stores.**

After `api.tasks.addTag()` or `api.tasks.removeTag()`, fetch the updated task via `api.tasks.get()` and call `replaceTaskInList()` with the result. This reuses the existing `selectTask()` fetch but adds the missing list-store update.

The alternative — constructing a patched task object locally from the tag API response — was rejected because:
1. The add-tag endpoint returns `Tag[]` (just the tags), not a full `Task` object.
2. The remove-tag endpoint returns `204 No Content`.
3. Constructing a partial update risks drift between the local object and backend state.

**Implementation approach: create a `refreshTask` helper in the tasks store.**

A new exported function `refreshTask(taskId)` will fetch the task, update `selectedTaskDetail`, and call `replaceTaskInList()`. This consolidates the pattern so `TaskDetail.svelte` can call one function instead of managing both stores. This helper is also useful for any future operations that need to re-sync a single task across both stores.

## Risks / Trade-offs

**Extra API call** — Each tag add/remove already calls the tag endpoint; the refresh adds one more `GET /tasks/{id}/` call. This matches the existing behavior (the current code already calls `selectTask()` which does this fetch). The only change is that the fetched result now also updates `listsStore`. No additional network cost.

**Race condition on rapid tag changes** — If the user adds tags very quickly, sequential fetches could arrive out of order. Mitigation: this is the same pattern used by all other mutations and hasn't been a problem in practice. The last fetch wins, and tags are additive, so transient inconsistency self-corrects.
