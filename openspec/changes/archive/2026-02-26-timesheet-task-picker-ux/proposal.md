## Why

The current timesheet task picker uses a native HTML `<select multiple>` that displays tasks as a flat list of titles with no visual hierarchy. Users cannot distinguish between top-level tasks, subtasks, and sub-subtasks, making it difficult to select the right tasks — especially in projects with deep nesting. Additionally, the time entry display only shows `task_ids` (integers) with no task names, making logged entries hard to review.

## What Changes

- Replace the native `<select multiple>` task picker with a styled, hierarchical task selector that visually indents subtasks and sub-subtasks
- Show task depth/nesting clearly through indentation and/or visual cues (icons, connecting lines, or typography)
- Support selecting multiple tasks via checkboxes rather than Ctrl+Click
- Display selected task names (with hierarchy context) in logged time entries instead of raw IDs
- Enrich the timesheet API response to include task titles alongside IDs

## Non-goals

- Changing the 1-hour-per-entry model (FR-13.1)
- Adding duration tracking or time range input
- Modifying the project selector or date picker
- Changing how tasks are assigned to projects (list-project linking)
- Adding search/filter within the task picker (may be future work)

## Capabilities

### New Capabilities

- `timesheet-task-picker`: Hierarchical, checkbox-based multi-select task picker for timesheet entries, replacing the native `<select multiple>` with indented tree display

### Modified Capabilities

- `svelte-frontend`: Timesheet section updated — task selector UX changes from native multi-select to hierarchical checkbox tree; time entry rows display task names instead of raw IDs

## Impact

- **Frontend**: `frontend/src/routes/timesheet/+page.svelte` — task picker component replacement, entry display changes
- **API**: `tasks/api/timesheet.py` — enrich `GET /timesheet/` response to include task titles (not just IDs); possibly adjust the project tasks endpoint serialization to return a flat list with depth info
- **Stores**: `frontend/src/lib/stores/timesheet.ts` — updated types to handle enriched task data in entries
- **API types**: `frontend/src/lib/api/types.ts` — updated `TimeEntry` type to include task name info
