## 1. Shared Infrastructure

- [x] 1.1 Create shared linked-tasks module at `frontend/src/lib/components/shared/linkedTasks.svelte.ts` — export `createLinkedTasksManager(entityType)` factory returning `loadAllTasks`, `loadLinkedTasks`, `addTaskLink`, `removeTaskLink`, `taskName` functions. Entity type determines which `api.taskLinks.*` methods are called.
- [x] 1.2 Create shared CRM CSS at `frontend/src/lib/styles/crm.css` — extract the ~200 lines of duplicated styles from existing pages. Rename `.network-page` → `.crm-page`, `.network-grid` → `.crm-grid`. Include: page shell, grid, panel, create-form, list, list-item (with active state), detail-header, detail-form, label, primary/danger buttons, linked-tasks-section, empty-state, and 1024px responsive breakpoint.

## 2. CRM Route Group

- [x] 2.1 Create `/crm/+layout.svelte` — sub-tab bar (People, Orgs, Interactions, Leads) with active state via `$page.url.pathname` exact matching. Import shared CRM CSS. Render `<slot>` for nested pages.
- [x] 2.2 Create `/crm/+page.svelte` — redirect to `/crm/people` via `goto()` in `onMount`.
- [x] 2.3 Move `frontend/src/routes/people/+page.svelte` → `frontend/src/routes/crm/people/+page.svelte`. Replace duplicated linked-tasks logic with `createLinkedTasksManager('people')`. Replace duplicated CSS classes with shared CRM CSS classes. Keep all entity-specific logic (follow-up tracking, tags, quick-log, sort/filter).
- [x] 2.4 Move `frontend/src/routes/organizations/+page.svelte` → `frontend/src/routes/crm/orgs/+page.svelte`. Replace duplicated linked-tasks logic with shared module. Replace duplicated CSS with shared classes. Keep org-type TypeaheadSelect and inline creation.
- [x] 2.5 Move `frontend/src/routes/interactions/+page.svelte` → `frontend/src/routes/crm/interactions/+page.svelte`. Replace duplicated linked-tasks logic with shared module. Replace duplicated CSS with shared classes. Keep multi-person chips, medium field, date handling.
- [x] 2.6 Move `frontend/src/routes/leads/+page.svelte` → `frontend/src/routes/crm/leads/+page.svelte`. Replace duplicated linked-tasks logic with shared module. Replace duplicated CSS with shared classes. Keep status pipeline, autosave-on-blur behavior.
- [x] 2.7 Delete old route directories: `frontend/src/routes/people/`, `frontend/src/routes/organizations/`, `frontend/src/routes/interactions/`, `frontend/src/routes/leads/`.

## 3. Network Route Group

- [x] 3.1 Create `/network/+layout.svelte` — sub-tab bar (Relationships, Graph) with active state via `$page.url.pathname`. Render `<slot>` for nested pages.
- [x] 3.2 Create `/network/+page.svelte` — redirect to `/network/relationships` via `goto()` in `onMount`.
- [x] 3.3 Move `frontend/src/routes/relationships/+page.svelte` → `frontend/src/routes/network/relationships/+page.svelte`. No logic changes needed — page is self-contained.
- [x] 3.4 Move `frontend/src/routes/graph/+page.svelte` → `frontend/src/routes/network/graph/+page.svelte`. No logic changes needed — page is self-contained.
- [x] 3.5 Delete old route directories: `frontend/src/routes/relationships/`, `frontend/src/routes/graph/`.

## 4. Navigation Updates

- [x] 4.1 Update `frontend/src/routes/+layout.svelte` top navbar — replace individual tabs (People, Orgs, Interactions, Relationships, Graph, Leads) with CRM (`/crm`) and Network (`/network`). Active state uses `pathname.startsWith('/crm')` and `pathname.startsWith('/network')`.
- [x] 4.2 Update `frontend/src/routes/+layout.svelte` mobile bottom nav — replace 10 items with 6: Tasks, Dashboard, Projects, Timesheet, CRM, Network. Same prefix-based active state.
- [x] 4.3 Update `frontend/src/routes/+layout.svelte` route detection — update any `$page.url.pathname` checks that reference old routes (e.g., for showing/hiding task panels, search bar visibility).

## 5. Cross-Cutting Updates

- [x] 5.1 Search all frontend code for hardcoded references to old routes (`/people`, `/organizations`, `/interactions`, `/relationships`, `/graph`, `/leads`) and update to new paths. Check: API client, stores, components, any `goto()` or `<a href>` calls.
- [x] 5.2 Update E2E tests in `e2e/` — change any route paths from old standalone routes to new nested routes.
- [x] 5.3 Update `frontend/src/routes/dashboard/+page.svelte` — if it links to people or interactions (e.g., follow-up links), update those hrefs to `/crm/people` and `/crm/interactions`.

## 6. Verification

- [x] 6.1 Run `cd frontend && npm run check` — ensure no TypeScript errors from the restructuring.
- [x] 6.2 Run `cd frontend && npm run build` — ensure static build succeeds with new route structure.
- [x] 6.3 Run `uv run python -m pytest e2e -q` — all pre-existing failures, zero new regressions from restructuring.
- [x] 6.4 Manual smoke test — verified via screenshots that CRM sub-pages load correctly, sub-tab navigation works, and navbar active states are correct.
