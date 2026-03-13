## Why

The Dashboard shows upcoming tasks grouped by time horizon, but completing a task requires navigating away to the Tasks view. This adds friction for quick triage workflows — users should be able to check off tasks directly from the dashboard.

## What Changes

- Add a checkbox to each task row on the Dashboard's Upcoming tab
- Clicking the checkbox completes the task via the existing API, with optimistic removal from the dashboard list
- If the completed task has recurrence, show an undo toast (consistent with Tasks view behavior)
- Completed tasks are removed from the dashboard view (they no longer have a relevant due date)

## Non-goals

- No inline editing of task fields from the dashboard
- No drag-and-drop reordering on the dashboard
- No uncomplete action beyond the undo toast for recurring tasks

## Capabilities

### New Capabilities

- `dashboard-task-completion`: Checkbox UI on dashboard task rows to mark tasks as done, with optimistic store updates and undo support for recurring tasks

### Modified Capabilities

- `upcoming-dashboard`: Dashboard task rows gain a completion checkbox; the upcoming store needs a removal function

## Impact

- **Frontend**: `frontend/src/routes/dashboard/+page.svelte` — add checkbox to task rows
- **Frontend**: `frontend/src/lib/stores/upcoming.ts` — add function to remove a task from the store
- **Backend**: No changes needed — uses existing `PATCH /api/tasks/{id}` completion endpoint
