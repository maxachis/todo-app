## Context

The app currently organizes tasks into Lists > Sections > Tasks. Tasks already have `due_date` (DateField) and `due_time` (TimeField) fields, and the API exposes them in `TaskSchema`. However, there is no cross-list view for tasks by due date. The search endpoint (`/search/`) demonstrates the pattern for querying across all lists using `select_related("section__list")`.

The frontend is a SvelteKit SPA with typed API client, Svelte stores, and route-based pages. Existing non-task pages (Projects, Timesheet, Import) follow a simple pattern: a dedicated route, a store or inline fetch, and a full-width center panel (no sidebar/detail panel).

## Goals / Non-Goals

**Goals:**
- Provide a single API endpoint that returns incomplete tasks with due dates, enriched with list/section names.
- Render a dashboard page grouped by time horizon (Overdue, Today, Tomorrow, This Week, Later).
- Allow navigating from a dashboard task to its list and selecting it.

**Non-Goals:**
- No inline editing, completion toggling, or drag-drop on the dashboard.
- No filtering/sorting controls in v1 (the grouping is fixed).
- No server-side grouping — the API returns a flat list sorted by date; the frontend groups.

## Decisions

### 1. Flat API response with client-side grouping

The API returns a flat array of upcoming tasks sorted by `due_date`, `due_time`. The frontend groups into time buckets (Overdue / Today / Tomorrow / This Week / Later) based on the user's local date.

**Why**: Keeps the API simple and stateless. Time-horizon grouping depends on the client's current date, so it belongs on the frontend. The search endpoint follows a similar pattern (flat results, client groups by list).

**Alternative considered**: Server-side grouping with a `group` field per task — rejected because the server would need to know "today" relative to the user's timezone, adding unnecessary complexity for a single-user app.

### 2. New dedicated API router (`tasks/api/upcoming.py`)

A new `GET /upcoming/` endpoint with its own router, registered alongside existing routers in `tasks/api/__init__.py`.

**Why**: Follows the existing pattern (search, export, timesheet each have their own router file). Keeps the tasks router focused on CRUD operations.

### 3. New response schema (`UpcomingTaskSchema`)

A lightweight schema containing: `id`, `title`, `due_date`, `due_time`, `priority`, `is_pinned`, `list_id`, `list_name`, `list_emoji`, `section_id`, `section_name`, `tags`. This is flatter than `TaskSchema` — no nested subtasks, no notes, no position.

**Why**: The dashboard only needs display-relevant fields. Including list/section names avoids extra client-side lookups. Keeping it flat is simpler to consume.

### 4. Frontend route at `/upcoming` with store

A new `frontend/src/routes/upcoming/+page.svelte` page with a companion `frontend/src/lib/stores/upcoming.ts` store. The store fetches from the API on mount and exposes a derived grouping. The layout tabs array gains an "Upcoming" entry.

**Why**: Follows the same pattern as Projects and Timesheet pages. A store allows potential future reactivity (e.g., refreshing after completing a task elsewhere).

### 5. Navigate-to-task linking

Each task row in the dashboard links to `/?list={list_id}&task={task_id}`. The main page reads these query params to auto-select the list and task.

**Why**: This is the simplest deep-linking approach. The main `+page.svelte` already has list selection logic — adding query param support is minimal.

**Alternative considered**: SvelteKit `goto()` with store manipulation — rejected as more coupled and harder to share as a URL.

## Risks / Trade-offs

- **Performance on large datasets**: The endpoint fetches all incomplete tasks with due dates. For a single-user app this is unlikely to be an issue. → Mitigation: No pagination in v1; can add `?limit=` later if needed.
- **Stale data**: The dashboard fetches once on mount and doesn't auto-refresh. → Mitigation: Acceptable for v1; user can navigate away and back. A future enhancement could add polling or store invalidation.
- **Query param deep-linking**: The main page doesn't currently read query params. → Mitigation: Small addition to `+page.svelte`'s `$effect` to read `list` and `task` params on mount.
