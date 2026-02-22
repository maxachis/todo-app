## 1. App Shell & Viewport

- [x] 1.1 Replace `100vh` with `100dvh` (with `vh` fallback) in `+layout.svelte` app shell height
- [x] 1.2 Add `@media (max-width: 640px)` block in `+layout.svelte` for navbar touch targets — set `min-height: 44px` on hamburger, settings cog, theme toggle, and detail panel toggle buttons

## 2. SearchBar

- [x] 2.1 Change SearchBar input from `width: 220px` to `width: 100%; max-width: 220px` in `SearchBar.svelte`
- [x] 2.2 Add `@media (max-width: 640px)` rule in `SearchBar.svelte` to reduce `max-width` so the input fits within the navbar alongside other controls

## 3. TaskRow

- [x] 3.1 Add `@media (max-width: 640px)` block in `TaskRow.svelte` to remove `white-space: nowrap` from `.meta` and allow wrapping
- [x] 3.2 Add `min-height: 44px` to task row checkboxes and pin buttons at the 640px breakpoint in `TaskRow.svelte`

## 4. TaskDetail

- [x] 4.1 Add `@media (max-width: 640px)` block in `TaskDetail.svelte` to increase tag button touch targets to `min-height: 44px`
- [x] 4.2 Increase form input padding and action button sizes at the 640px breakpoint in `TaskDetail.svelte`

## 5. Upcoming Dashboard

- [x] 5.1 Add `@media (max-width: 640px)` block in `upcoming/+page.svelte` with `overflow: hidden; text-overflow: ellipsis` on `.task-location`
- [x] 5.2 Allow task row metadata to stack (flex-wrap) at the 640px breakpoint in `upcoming/+page.svelte`

## 6. Projects Page

- [x] 6.1 Add `@media (max-width: 640px)` block in `projects/+page.svelte` to change `.create-form` grid to `grid-template-columns: 1fr` (single column)
- [x] 6.2 Add `min-height: 44px` to `.card-actions` buttons at the 640px breakpoint in `projects/+page.svelte`

## 7. Timesheet Page

- [x] 7.1 Add `flex-wrap: wrap` to `.summary-bar` at the 640px breakpoint in `timesheet/+page.svelte`
- [x] 7.2 Stack `.entry-form` fields vertically at the 640px breakpoint in `timesheet/+page.svelte` (change flex direction to column or set `flex-basis: 100%` on children)
- [x] 7.3 Fix `.week-nav` date range text overflow at the 640px breakpoint in `timesheet/+page.svelte` (allow wrapping or reduce font size)
- [x] 7.4 Add `flex-wrap: wrap` to `.entry-row` at the 640px breakpoint in `timesheet/+page.svelte`

## 8. Relationships Page

- [x] 8.1 Add `overflow: hidden; text-overflow: ellipsis; white-space: nowrap` to relationship `.title` at the 640px breakpoint in `relationships/+page.svelte`
- [x] 8.2 Add `min-height: 44px` to relationship card action buttons at the 640px breakpoint in `relationships/+page.svelte`

## 9. Verification

- [x] 9.1 Run `npm run check` in `frontend/` to verify no TypeScript or Svelte compilation errors
- [x] 9.2 Run `npm run build` in `frontend/` to verify production build succeeds
