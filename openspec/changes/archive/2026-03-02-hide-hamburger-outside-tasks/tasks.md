## 1. Hide mobile toggle buttons on non-Tasks routes

- [x] 1.1 Wrap the sidebar hamburger button (☰, `&#9776;`) in `{#if isTasksRoute}` in `frontend/src/routes/+layout.svelte`
- [x] 1.2 Wrap the detail-panel ellipsis button (⋮, `&#8942;`) in `{#if isTasksRoute}` in `frontend/src/routes/+layout.svelte` (already guarded)

## 2. Verify

- [x] 2.1 Confirm buttons render on Tasks route (`/`) at mobile viewport
- [x] 2.2 Confirm buttons are absent on other routes (e.g. `/dashboard`, `/crm/people`) at mobile viewport
