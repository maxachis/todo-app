## Why

The hamburger (☰) and detail-panel (⋮) toggle buttons in the top navbar are rendered on all routes at mobile breakpoints, but the sidebar and detail panel they control only exist on the Tasks route (`/`). Tapping them on other pages does nothing, creating a confusing dead control.

## What Changes

- Conditionally render the two mobile-only toggle buttons (sidebar hamburger and detail-panel ellipsis) only when the user is on the Tasks route.
- No layout, styling, or desktop behavior changes.

## Non-goals

- Changing the sidebar or detail panel behavior on the Tasks route.
- Adding mobile navigation drawers to other routes.
- Modifying desktop breakpoint behavior (buttons are already hidden on desktop).

## Capabilities

### New Capabilities

(none — this is a visibility fix for existing controls)

### Modified Capabilities

(none — no spec-level behavior changes)

## Impact

- `frontend/src/routes/+layout.svelte` — wrap the two `.mobile-only` buttons in an `{#if isTasksRoute}` guard.
