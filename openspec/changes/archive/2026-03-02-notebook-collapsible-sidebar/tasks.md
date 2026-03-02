## 1. Sidebar Collapse State & localStorage

- [x] 1.1 Add `sidebarCollapsed` reactive state (`$state`) initialized from `localStorage.getItem('notebook-sidebar-collapsed')`, defaulting to `false` — in `frontend/src/routes/notebook/+page.svelte`
- [x] 1.2 Add `$effect` to sync `sidebarCollapsed` to localStorage on change — in `frontend/src/routes/notebook/+page.svelte`

## 2. Layout & CSS Changes

- [x] 2.1 Update `.notebook-layout` grid to use dynamic `grid-template-columns` based on `sidebarCollapsed` state: `32px 1fr` when collapsed, `220px 1fr` when expanded — in `frontend/src/routes/notebook/+page.svelte`
- [x] 2.2 Add CSS transition on `.notebook-layout` for `grid-template-columns` (~200ms ease) — in `frontend/src/routes/notebook/+page.svelte`
- [x] 2.3 Add `overflow: hidden` on the sidebar container when collapsed to hide content during/after transition — in `frontend/src/routes/notebook/+page.svelte`

## 3. Toggle Button UI

- [x] 3.1 Add a collapse toggle button in the sidebar header area showing a left-pointing chevron (when expanded) — in `frontend/src/routes/notebook/+page.svelte`
- [x] 3.2 When collapsed, render a slim vertical strip with a right-pointing chevron expand button — in `frontend/src/routes/notebook/+page.svelte`
- [x] 3.3 Style the toggle button to match existing app button patterns (subtle, icon-only) — in `frontend/src/routes/notebook/+page.svelte`

## 4. Keyboard Shortcut

- [x] 4.1 Add `keydown` event listener for `Cmd+\` (Mac) / `Ctrl+\` (other) that toggles `sidebarCollapsed` — in `frontend/src/routes/notebook/+page.svelte`
- [x] 4.2 Call `preventDefault()` on the shortcut to avoid browser default behavior — in `frontend/src/routes/notebook/+page.svelte`

## 5. Verification

- [x] 5.1 Verify sidebar collapses/expands with smooth animation on button click
- [x] 5.2 Verify collapsed state persists after page reload
- [x] 5.3 Verify keyboard shortcut toggles sidebar on both Mac and non-Mac
- [x] 5.4 Verify editor fills full width when sidebar is collapsed
- [x] 5.5 Run `cd frontend && npm run check` to ensure no type errors
