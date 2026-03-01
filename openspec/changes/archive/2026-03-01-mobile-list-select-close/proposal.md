## Why

On mobile, tapping a list in the sidebar selects it but leaves the sidebar overlay open, forcing the user to manually close it before seeing the task list. This adds unnecessary friction — selecting a list should immediately dismiss the sidebar so the user can see their tasks.

## What Changes

- When a list is selected on mobile (viewport ≤ 1023px), the sidebar overlay automatically closes
- Desktop behavior is unchanged (sidebar is always visible as part of the grid layout)

## Non-goals

- Changing the sidebar open/close animation
- Adding swipe-to-dismiss gestures
- Modifying the detail panel behavior

## Capabilities

### New Capabilities

- `mobile-sidebar-auto-close`: Auto-close the mobile sidebar overlay when a list is selected

### Modified Capabilities

_(none — no existing spec-level requirements change)_

## Impact

- **Code**: `frontend/src/routes/+layout.svelte` — the `sidebarOpen` state needs to react to list selection changes on mobile viewports
- **APIs**: None
- **Dependencies**: None
