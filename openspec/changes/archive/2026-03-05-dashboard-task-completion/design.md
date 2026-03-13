## Context

The Dashboard Upcoming tab renders task rows as `<a>` links to the Tasks view. Tasks can be completed from the Tasks view via a checkbox in `TaskRow.svelte`, which calls `completeTask()` from the tasks store. The dashboard uses a separate `upcomingStore` (Svelte writable) populated by `loadUpcoming()`.

## Goals / Non-Goals

**Goals:**
- Add a completion checkbox to each dashboard task row
- Optimistically remove completed tasks from the dashboard
- Show undo toast for recurring tasks (matching Tasks view behavior)

**Non-Goals:**
- Syncing dashboard store with the main tasks store (they serve different views)
- Adding uncomplete functionality beyond the recurring-task undo toast

## Decisions

### 1. Reuse `completeTask` from the tasks store
The existing `completeTask(taskId)` in `stores/tasks.ts` calls `PATCH /api/tasks/{id}` with `{is_completed: true}` and handles recurrence. We'll import and call it directly from the dashboard, then separately remove the task from `upcomingStore`.

**Alternative considered**: Duplicating the API call in the upcoming store. Rejected because it would duplicate completion logic and recurrence handling.

### 2. Optimistic removal from upcomingStore
Add a `removeUpcomingTask(taskId)` helper that filters the task out of the store immediately on checkbox click, before the API call resolves. On failure, reload the full upcoming list.

**Alternative considered**: Waiting for API response before removing. Rejected because it makes the UI feel sluggish.

### 3. Checkbox as a separate click target from the row link
The task row is an `<a>` tag. The checkbox will use `event.preventDefault()` and `event.stopPropagation()` to prevent navigation when clicking the checkbox area.

### 4. Minimal component extraction
The checkbox + completion handler will be inlined in the dashboard page component rather than extracting a shared component. The dashboard checkbox is simpler than TaskRow's (no drag-and-drop, no keyboard nav, no nesting indicators).

## Risks / Trade-offs

- **[Stale tasks store]** → `completeTask` updates the tasks store which may not be loaded on the dashboard. This is fine — the tasks store will reload when the user navigates to the Tasks view.
- **[Race condition on undo]** → If user undoes a recurring task completion, the task should reappear on the dashboard. Mitigation: the undo callback calls `uncompleteTask` then `loadUpcoming()` to refresh.
