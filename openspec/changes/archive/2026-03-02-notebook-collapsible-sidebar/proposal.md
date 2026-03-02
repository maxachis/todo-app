## Why

The notebook view uses a fixed two-panel layout with a 220px sidebar that is always visible. On smaller screens or when focused on writing, the sidebar wastes horizontal space. Users should be able to collapse the sidebar to maximize the editor area, consistent with how modern note-taking apps work.

## What Changes

- Add a toggle button to collapse/expand the notebook sidebar
- When collapsed, the sidebar hides and the editor takes the full width
- Persist the collapsed state in localStorage so it survives page reloads
- Add a keyboard shortcut to toggle the sidebar (e.g., `Cmd/Ctrl+\`)

## Non-goals

- Resizable sidebar width (drag-to-resize) — the sidebar stays at its fixed 220px when expanded
- Mobile-specific responsive behavior — this is a desktop toggle control
- Changing the sidebar content or grouping logic

## Capabilities

### New Capabilities
- `notebook-collapsible-sidebar`: Toggle to collapse/expand the notebook page sidebar, with localStorage persistence and keyboard shortcut

### Modified Capabilities
- `notebook-frontend`: The two-panel layout requirement changes to support a collapsible sidebar state

## Impact

- `frontend/src/routes/notebook/+page.svelte` — layout grid and sidebar rendering
- localStorage — new key for sidebar collapsed state
- No backend/API changes required
