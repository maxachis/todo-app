## 1. App Shell Layout Lock

- [x] 1.1 In `frontend/src/routes/+layout.svelte`, change `.app-shell` from `min-height: 100vh` to `height: 100vh` and add `overflow: hidden` (desktop only, wrap in media query or keep mobile override)
- [x] 1.2 Add `min-height: 0` and `overflow-y: auto` to `aside`, `.center-panel`, and `.detail-panel` rules so each panel scrolls independently
- [x] 1.3 Ensure `.panels` grid has `height: 100%` or equivalent so it fills the available `1fr` row

## 2. Network Page Panels

- [x] 2.1 In `frontend/src/routes/people/+page.svelte`, make `.network-page` fill its container height and add `overflow-y: auto` + `min-height: 0` to each `.panel` in `.network-grid`
- [x] 2.2 In `frontend/src/routes/organizations/+page.svelte`, apply the same overflow and height-fill changes to `.network-page` and `.panel`
- [x] 2.3 In `frontend/src/routes/interactions/+page.svelte`, apply the same overflow and height-fill changes to `.network-page` and `.panel`

## 3. Relationships Page

- [x] 3.1 In `frontend/src/routes/relationships/+page.svelte`, make `.network-page` fill its container height and add `overflow-y: auto` + `min-height: 0` to each `.panel` column

## 4. Mobile Preservation

- [x] 4.1 Ensure the `@media (max-width: 1023px)` block in `+layout.svelte` reverts `.app-shell` to `min-height: 100vh` / `overflow: visible` so mobile retains normal document scroll
- [x] 4.2 Verify network page panels stack and scroll normally on narrow viewports (no height lock)

## 5. Verification

- [x] 5.1 Manually test Tasks page: confirm sidebar, center, and detail panels scroll independently
- [x] 5.2 Manually test People, Orgs, Interactions pages: confirm list and detail panels scroll independently
- [x] 5.3 Manually test Relationships page: confirm both columns scroll independently
- [x] 5.4 Verify drag-and-drop still works correctly within scrollable panels on the Tasks page
- [x] 5.5 Run `cd frontend && npm run check` to confirm no type/lint regressions
