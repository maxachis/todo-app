## Why

The app has a structural mobile framework (1023px breakpoint with bottom tabs, hamburger sidebar, slide-in detail panel) but individual pages and components break or become unusable on phone-sized viewports (375–430px). Fixed-width elements overflow, touch targets are too small for fingers, and several pages (Timesheet, Projects create form) have layouts that assume wide viewports. Users cannot effectively use the app on a phone despite the shell being responsive.

## What Changes

- Add a `@media (max-width: 640px)` breakpoint pass across all pages for phone-specific layout fixes
- Fix SearchBar fixed 220px width to be fluid/responsive in the navbar
- Fix TaskRow `.meta` section `white-space: nowrap` overflow on narrow viewports
- Increase touch targets globally: buttons, checkboxes, tag controls, and form inputs to meet 44px minimum height
- Fix Projects create form 3-column grid to stack on phones
- Fix Timesheet summary bar, entry form, week nav, and entry rows to wrap/stack instead of overflow
- Fix Upcoming task location text overflow (truncation)
- Fix Relationships title overflow for long "Person A ↔ Person B" text
- Increase TaskDetail form element sizes (labels, tag buttons) for touch usability
- Address `100vh` mobile browser viewport issues (URL bar resize)

## Non-goals

- Tablet-specific optimizations (the existing 1023px breakpoint handles tablets adequately)
- Mobile-native UX patterns like swipe gestures, pull-to-refresh, or haptic feedback
- Redesigning any page layout for mobile (all changes are minimal CSS fixes to make existing layouts work)
- Adding additional breakpoints beyond 640px
- JavaScript/Svelte logic changes (this is a CSS-only change)

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `svelte-frontend`: Adding phone-viewport responsive requirements — touch target sizing, overflow handling, and fluid layouts for SearchBar, TaskRow, TaskDetail, Projects, Timesheet, Upcoming, and Relationships pages. Affects scenarios under "Three-panel layout shell" (line 12), "Search across all lists" (line 326), "Task list rendering" (line 113), "Task detail panel" (line 136), "Projects page" (line 383), and "Timesheet page" (line 398).

## Impact

- **Frontend only** — all changes are CSS within SvelteKit components
- **Files affected**: `+layout.svelte`, `SearchBar.svelte`, `TaskRow.svelte`, `TaskDetail.svelte`, `projects/+page.svelte`, `timesheet/+page.svelte`, `upcoming/+page.svelte`, `relationships/+page.svelte`
- **No backend changes**, no API changes, no database changes
- **No new dependencies**
- **Risk**: Low — CSS additions are additive and scoped behind media queries, no existing desktop behavior changes
