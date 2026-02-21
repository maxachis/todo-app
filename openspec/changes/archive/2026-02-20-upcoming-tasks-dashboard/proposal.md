## Why

There is no way to see upcoming deadlines across all lists and sections in a single view. Users must navigate into each list individually to find tasks with approaching due dates, making it easy to miss deadlines. A dedicated dashboard provides an at-a-glance view of what's coming up.

## What Changes

- Add a new API endpoint that returns incomplete tasks with due dates, sorted chronologically, including their list and section context.
- Add a new `/upcoming` route in the Svelte frontend that renders a grouped dashboard view (e.g., grouped by "Today", "Tomorrow", "This Week", "Later").
- Add an "Upcoming" tab to the top navigation bar alongside the existing Tasks/Projects/Timesheet/Import tabs.
- Each task in the dashboard shows its title, due date/time, list name, section name, and priority — and links back to the task in its list for editing.

## Non-goals

- Notifications or reminders (email, push, browser alerts).
- Calendar view or calendar integrations.
- Recurring/repeating task support.
- Editing tasks inline from the dashboard (navigate to the task's list instead).

## Capabilities

### New Capabilities
- `upcoming-dashboard`: Dashboard page and supporting API for viewing incomplete tasks with due dates, grouped by time horizon, with list/section context.

### Modified Capabilities

_(none — the new API endpoint and frontend route are self-contained within the new capability)_

## Impact

- **Backend**: New Django Ninja router endpoint in `tasks/api/` querying `Task` objects filtered by `due_date IS NOT NULL`, `is_completed=False`, annotated with list/section names.
- **Frontend**: New SvelteKit route at `frontend/src/routes/upcoming/+page.svelte`, new store or loader for upcoming tasks, updated layout navigation tabs.
- **Tests**: New API test file, new E2E test for the dashboard page.
- **No migrations needed** — uses existing `due_date`/`due_time` fields on the Task model.
