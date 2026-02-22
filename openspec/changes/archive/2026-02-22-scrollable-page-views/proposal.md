## Why

All page views (Tasks, People, Orgs, Interactions, Relationships) currently scroll as a single document — when content overflows, the entire page scrolls, pushing the header and sibling panels out of view. Each panel within a page should scroll independently so users can reference one panel (e.g., a list of people) while scrolling another (e.g., the detail form) without losing context.

## What Changes

- Make the layout viewport-filling: the app shell, header, and main content area should consume exactly the viewport height with no document-level scroll.
- On the **Tasks page** (three-panel layout), the sidebar, center task list, and detail panel each scroll independently.
- On **People, Orgs, and Interactions pages** (two-panel `network-grid` layout), the list panel and detail panel each scroll independently.
- On the **Relationships page** (two-column grid), each column scrolls independently.
- The top navigation header remains fixed/pinned at all viewport sizes.

## Non-goals

- Mobile layout changes — the existing stacked single-column mobile behavior is fine; independent scroll is primarily a desktop concern.
- Adding virtual/infinite scroll or lazy loading — this is purely a CSS layout change.
- Changing the content or functionality of any page.

## Capabilities

### New Capabilities

- `scrollable-panels`: CSS layout changes to make each panel/column within a page independently scrollable, keeping the header pinned and the layout viewport-constrained.

### Modified Capabilities

_(none — this is a pure CSS/layout change with no requirement-level behavior changes to existing specs)_

## Impact

- **Layout**: `frontend/src/routes/+layout.svelte` — app shell grid and panel styles need height constraints and overflow rules.
- **Tasks page**: `frontend/src/routes/+page.svelte` — task view may need overflow adjustments.
- **Network pages**: `frontend/src/routes/people/+page.svelte`, `frontend/src/routes/organizations/+page.svelte`, `frontend/src/routes/interactions/+page.svelte`, `frontend/src/routes/relationships/+page.svelte` — panel and grid styles need overflow/height changes.
- No backend or API changes required.
- No new dependencies.
