## Context

The ToDo App has a fully integrated network module with Svelte pages for People, Organizations, Interactions, Relationships, and Graph, plus a Django API backend with CRUD endpoints for all entities. Bridge models (TaskPerson, TaskOrganization, InteractionTask) and their API endpoints already exist. However, the network pages are unreachable from the navigation bar, and no frontend UI uses the task-link endpoints. The existing network pages each use a consistent two-panel layout (list + inline detail) with CRUD support.

## Goals / Non-Goals

**Goals:**
- Make all network pages discoverable via the main navigation
- Let users link/unlink people and organizations to tasks from the task detail panel
- Let users link/unlink tasks from person, organization, and interaction detail views
- Add TypeScript types and API client methods for the existing task-link endpoints

**Non-Goals:**
- Backend API or model changes (all endpoints already exist and are tested)
- Changes to graph visualization or relationship pages
- Changes to network CRUD functionality (create/edit/delete already works)
- Bulk linking operations or drag-to-link gestures
- Search/filter within link dropdowns (simple select is sufficient for single-user scale)

## Decisions

### 1. Add network pages as flat entries in the tabs array

Add People, Organizations, Interactions, Relationships, and Graph as individual entries in the `tabs` array in `+layout.svelte`. They render alongside the existing tabs (Tasks, Upcoming, Projects, Timesheet, Import) with the same link/active-state pattern.

**Rationale:** The existing tab system is a simple flat array of `{ href, label }` objects. Adding entries follows the established pattern with zero abstraction overhead. At 10 total tabs, the navbar is still manageable — on mobile, the bottom tab bar scrolls horizontally if needed.

**Alternatives considered:**
- Dropdown/grouped "Network" menu — adds interaction complexity (hover/click to expand) for marginal space savings; not worth it at this tab count
- Separate sidebar section — breaks the established single-nav pattern

### 2. Extend the `isTasksRoute` guard for network routes

The layout uses `isTasksRoute` to conditionally show the sidebar and detail panel. Network routes should behave like other non-task routes (Projects, Timesheet) — showing only the center panel. No changes needed to this logic since the derived check `$page.url.pathname === '/'` already excludes all non-root routes.

### 3. Add `api.taskLinks` namespace to the API client

Group all task-link methods under a new `taskLinks` namespace in `frontend/src/lib/api/index.ts` with sub-objects for `people`, `organizations`, and `interactions`. Each sub-object has `list`, `add`, and `remove` methods.

**Rationale:** Follows the existing namespacing pattern (e.g., `api.people`, `api.organizations`). Keeps task-link operations grouped and discoverable.

### 4. Fetch links on task selection, not eagerly

When a task is selected in the task detail panel, fetch its linked people and organizations from the API at that point. Do not pre-fetch links for all tasks — that would be N+1 requests on list load for a feature only used when viewing task detail.

**Rationale:** Links are only visible in the detail panel. Lazy-loading on selection keeps the initial list load fast. The link endpoints return small payloads so per-selection fetch latency is negligible.

### 5. Use inline `<select>` dropdowns for adding links

For linking entities, use a simple `<select>` dropdown populated with all available people/organizations/tasks (minus already-linked ones). No autocomplete, search, or modal — the single-user dataset is small enough for a flat dropdown.

**Rationale:** Keeps the UI minimal and consistent with existing patterns (e.g., the interaction form's person/type dropdowns). Autocomplete would be over-engineering for a personal task manager.

### 6. Resolve link display names client-side from already-loaded entity lists

When displaying linked people/organizations on a task, the API returns link objects with IDs (e.g., `person_id`). Resolve display names by looking up the ID in the already-fetched people/organizations lists (which each page loads on mount). For task detail, fetch the people and organizations lists if not already loaded.

**Rationale:** Avoids adding display-name fields to the link API response (which would require backend changes, a non-goal). The entity lists are small and already cached in the existing page stores.

### 7. Create a shared `LinkedEntities.svelte` component

Build one reusable component that handles the list-add-remove pattern for linked entities. It accepts props for the entity list, linked IDs, display name resolver, and add/remove callbacks. Used in both TaskDetail (for people/orgs) and network detail pages (for tasks).

**Rationale:** The link management UI is identical across all three contexts (task→people, task→orgs, person→tasks, org→tasks, interaction→tasks) — a shared component avoids duplicating the dropdown + list + remove button pattern five times.

## Risks / Trade-offs

- **Navbar width on mobile with 10 tabs**: The bottom tab bar may overflow → Mitigation: make the mobile tab bar horizontally scrollable with `overflow-x: auto`
- **Fetching entity lists for name resolution in TaskDetail**: If the user hasn't visited the People or Organizations pages, those lists aren't cached → Mitigation: fetch people and organizations lists on demand when the linked-entities section mounts
- **No optimistic UI for link operations**: Link add/remove will wait for the API response before updating the UI → Acceptable trade-off: link operations are fast (single row insert/delete) and the lack of rollback complexity keeps the code simple
- **Dropdown may grow long with many people/organizations**: No search/filter in the select → Acceptable for single-user scale; can add autocomplete later if needed
