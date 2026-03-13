## Why

The Dashboard's Upcoming tab currently only shows tasks that have due dates. Pinned tasks represent high-priority items the user has explicitly flagged for attention, but if they lack a due date, they're invisible on the dashboard. Showing pinned tasks on the dashboard ensures the user's most important items are always surfaced in their daily overview, regardless of whether a due date is set.

## Non-goals

- Changing how pinning works in the task list view
- Adding a separate "Pinned" tab to the dashboard
- Modifying the Trends tab
- Changing the follow-ups due section

## Capabilities

### New Capabilities

- `dashboard-pinned-tasks`: A "Pinned" group displayed on the Dashboard Upcoming tab, showing all incomplete pinned tasks (including those without due dates). Pinned tasks with due dates that already appear in time-horizon groups should also appear in the Pinned group for visibility. The Pinned group renders above the time-horizon groups but below Follow-ups Due.

### Modified Capabilities

- `upcoming-dashboard`: The API and frontend need to also return/display pinned tasks that have no due date. The grouping logic on the frontend gains a new "Pinned" bucket.

## Impact

- **Backend**: `GET /api/upcoming/` endpoint needs to also return pinned tasks without due dates (currently filtered to `due_date__isnull=False`). The `due_date` field in `UpcomingTaskSchema` must become optional.
- **Frontend types**: `UpcomingTask.due_date` changes from `string` to `string | null` to accommodate pinned tasks without dates.
- **Frontend store/page**: `upcoming.ts` store unchanged. Dashboard `+page.svelte` grouping logic adds a "Pinned" group and handles null due dates.
- **No migration needed**: `is_pinned` already exists on the Task model.
