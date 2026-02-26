## Why

The timesheet summary bar only shows hours logged for the current week. When reviewing a week's time entries, there's no way to see how many total hours have been invested in each project overall. This context is useful for understanding cumulative effort alongside the weekly snapshot.

## What Changes

- Add all-time total hours per project to the timesheet API summary (`per_project` entries gain an `overall_hours` field)
- Add all-time total hours across all projects to the timesheet API summary (`overall_total_hours` field)
- Display overall project hours alongside weekly hours in the timesheet summary bar on the frontend

## Non-goals

- Changing the projects page or its existing `total_hours` metric
- Adding date-range filtering or custom period summaries
- Changing how time entries are created or deleted

## Capabilities

### New Capabilities

- `timesheet-summary`: Requirements for the timesheet summary bar — weekly totals, per-project breakdown, and overall (all-time) hours display

### Modified Capabilities

_(none — no existing spec covers the timesheet summary; `timesheet-task-picker` only covers the task picker UI)_

## Impact

- **Backend**: `tasks/api/timesheet.py` — additional aggregation query for all-time hours in `get_timesheet`
- **Frontend**: `frontend/src/routes/timesheet/+page.svelte` — summary bar UI updates to show overall hours
- **Frontend**: `frontend/src/lib/api/types.ts` — updated `TimesheetResponse` type for new summary fields
