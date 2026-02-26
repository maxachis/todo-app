## Context

The timesheet page lets users log 1-hour time entries against a project, optionally associating tasks from that project's linked lists. Currently, the task picker is a native `<select multiple>` showing a flat list of task titles. The API returns only `task_ids` (integers) in time entry responses, so logged entries display no task information at all. Task hierarchy (parent→child nesting) is available in the data model (`Task.parent` FK) and returned by the project tasks endpoint (nested `subtasks` arrays), but the frontend doesn't use it.

## Goals / Non-Goals

**Goals:**
- Replace the native multi-select with a checkbox-based tree picker that shows task hierarchy via indentation
- Display task names (with hierarchy breadcrumbs) in logged time entry rows
- Enrich the timesheet API to return task titles alongside IDs
- Keep the implementation simple — reuse existing data and patterns rather than introducing new libraries

**Non-Goals:**
- Changing the 1-hour-per-entry model
- Adding search/filter/typeahead to the task picker
- Modifying the project tasks endpoint structure
- Adding duration or time-range input

## Decisions

### 1. Flatten task tree with depth for the picker

**Decision:** Transform the nested `subtasks` array from the project tasks API into a flat list with a `depth` property, then render each row with `padding-left: depth * indent`.

**Rationale:** The project tasks endpoint already returns `TaskSchema` with nested `subtasks`. Rather than changing the API, we flatten client-side. This avoids backend changes for the picker and reuses the existing data shape.

**Alternative considered:** Add a `GET /projects/{id}/tasks/?flat=true&include_depth=true` endpoint. Rejected — adds backend complexity for a purely presentational concern.

### 2. Checkbox-based multi-select in a scrollable container

**Decision:** Replace `<select multiple>` with a styled `<div>` containing checkbox rows, one per task. Checking a parent does NOT auto-check children (each task is independently selectable). The container is scrollable with a max-height.

**Rationale:** Checkboxes are more discoverable than Ctrl+Click. Independent selection (no cascading) keeps the model simple — users may want to log time against a parent task without its children, or vice versa. This matches the existing M2M semantics where any combination of tasks can be selected.

**Alternative considered:** Cascading parent-child selection. Rejected — adds complexity and the use cases don't clearly require it. The current M2M model treats each task independently.

### 3. Enrich timesheet API with task details

**Decision:** Add `task_details: [{id, title, parent_titles}]` to the timesheet GET response (in the `entries_by_date` grouped entries). `parent_titles` is an ordered list from root to immediate parent, providing hierarchy context.

**Rationale:** The frontend needs task names for entry display. Including `parent_titles` lets the UI show breadcrumb context (e.g., "Feature A > Design > Mock up screens") without additional API calls. The data is already loaded via `prefetch_related("tasks")` — we just need to walk each task's parent chain.

**Alternative considered:** Return only `task_titles` (flat list of strings). Rejected — loses hierarchy context which is the main UX problem we're solving.

### 4. Display tasks in entry rows as comma-separated with hierarchy

**Decision:** Show associated tasks in entry rows as a comma-separated list. Each task shows its title with a truncated breadcrumb prefix if it has parents (e.g., "Feature A > Mock up screens"). Limit display to first 2-3 tasks with a "+N more" overflow indicator.

**Rationale:** Entry rows are compact — full breadcrumbs for many tasks would overflow. The truncated prefix gives just enough context to distinguish same-named tasks at different nesting levels.

### 5. No new components — inline in timesheet page

**Decision:** Build the checkbox tree picker directly in `+page.svelte` rather than extracting a reusable component.

**Rationale:** This is a single-use picker specific to timesheet task selection. The existing TypeaheadSelect component serves a different pattern (single-select with search). If a reusable tree-select is needed later, it can be extracted then.

## Risks / Trade-offs

- **Deep nesting visual limits** — Tasks nested 4+ levels deep may push content too far right. Mitigation: cap visual indent at 3 levels (tasks deeper than that still show but don't indent further).
- **Parent chain query performance** — Walking parent chains for `parent_titles` could be slow with many tasks. Mitigation: the M2M relation is already prefetched, and we only need parents for linked tasks (typically 1-5 per entry). We can use `select_related` on the task's parent chain or build a lookup dict.
- **No backward-compatible API change** — Adding `task_details` to the response is additive (existing `task_ids` stays). No migration needed. Frontend types need updating.
