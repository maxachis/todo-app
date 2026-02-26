## 1. Backend: Enrich timesheet API with task details

- [x] 1.1 Add `task_details` to the timesheet GET response in `tasks/api/timesheet.py` — for each entry in `entries_by_date`, include a `task_details` array alongside existing `task_ids`. Each item: `{id, title, parent_titles}` where `parent_titles` is an ordered list of ancestor titles from root to immediate parent. Build a parent lookup dict from prefetched tasks to walk parent chains efficiently.
- [x] 1.2 Update `frontend/src/lib/api/types.ts` — add `task_details` field to the entry type in `TimesheetResponse.entries_by_date` with shape `Array<{id: number, title: string, parent_titles: string[]}>`.
- [x] 1.3 Add API test in `tasks/tests/` verifying `task_details` is returned correctly for entries with tasks at various nesting levels (top-level, subtask, sub-subtask) and for entries with no tasks.

## 2. Frontend: Hierarchical task picker

- [x] 2.1 Add a `flattenTaskTree` helper function in `frontend/src/routes/timesheet/+page.svelte` that takes the nested `Task[]` from the project tasks endpoint and returns a flat array of `{id, title, depth}` objects, capping depth at 3 for visual indentation.
- [x] 2.2 Replace the `<select multiple>` in the entry form with a scrollable checkbox-based task picker. Each row: a checkbox + task title, indented by `depth * 1.25rem` left padding. Bind checkbox state to `newTaskIds`. Container has `max-height: 12rem` with `overflow-y: auto`.
- [x] 2.3 Style the task picker to match existing form styling (border, radius, font-size from `--font-body`, dark mode support via CSS variables). Subtask rows should use slightly smaller/lighter text (`--text-secondary`) to visually distinguish hierarchy levels.
- [x] 2.4 Ensure the picker is hidden when no project is selected or the project has no incomplete tasks (preserving existing conditional logic).

## 3. Frontend: Display task names in entry rows

- [x] 3.1 Update entry row rendering in `+page.svelte` to display task names from `task_details`. Format each task as `"Parent > Task title"` breadcrumb (using `parent_titles`). Show up to 3 tasks comma-separated; if more, append "+N more".
- [x] 3.2 Style the task names display in entry rows — use `--text-secondary` color, `0.8rem` font size, truncate with ellipsis if the line overflows.

## 4. Mobile responsiveness

- [x] 4.1 Ensure the checkbox task picker stacks to full width on phone viewports (640px and below), consistent with existing entry form responsive behavior.
- [x] 4.2 Verify entry rows with task names wrap properly on narrow viewports without horizontal overflow.
