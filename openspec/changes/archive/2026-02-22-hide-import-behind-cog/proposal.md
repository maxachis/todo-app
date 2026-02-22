## Why

The Import tab occupies space in the primary navigation alongside frequently-used tabs (Tasks, Upcoming, Projects, Timesheet, etc.). Import is an infrequent utility action, not a daily workflow destination. Moving it behind a settings/cog icon declutters the navbar and keeps primary navigation focused on core workflows.

## What Changes

- Remove "Import" from the primary tab list in the top navigation bar and mobile bottom tabs.
- Add a cog/settings icon button next to the existing dark/light theme toggle in the navbar.
- Clicking the cog icon opens a dropdown or popover menu containing an "Import" link (and potentially other utility actions in the future).
- The `/import` route and import page remain unchanged — only the navigation entry point moves.

## Capabilities

### New Capabilities

- `settings-menu`: A cog icon button in the navbar that opens a dropdown menu for utility/settings actions (starting with Import).

### Modified Capabilities

- `svelte-frontend`: Navigation tab list changes — Import tab removed from primary tabs. Cog icon with dropdown added next to theme toggle.

## Impact

- **Frontend only**: Changes are limited to `frontend/src/routes/+layout.svelte` (navbar tabs and new cog menu) and potentially a new small dropdown component.
- **No backend changes**: The `/import` route and API remain unchanged.
- **No breaking changes**: The import page URL (`/import`) stays the same; only the navigation path to reach it changes.
