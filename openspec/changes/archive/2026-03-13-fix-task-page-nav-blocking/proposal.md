## Why

When the task page has a large number of tasks loaded (e.g., 176 tasks with subtasks), clicking navbar links to navigate to other pages sometimes fails — the app does not respond to the click. Navigation works fine from all other pages. This is a data-dependent bug that only manifests with sufficient task volume, pointing to either a performance bottleneck blocking the main thread or an event-handling side effect from the task page's drag-and-drop / keyboard infrastructure.

## What Changes

- Diagnose and fix the root cause of navigation blocking when the task page has many tasks loaded
- Ensure `svelte-dnd-action` event handlers (which call `e.stopPropagation()` and `e.preventDefault()` on `mousedown` for every draggable item) do not interfere with SvelteKit's router click interception on `document.documentElement`
- Optimize the `TaskList` effect that recalculates `sortableActiveTasks` to avoid unnecessary re-renders and DnD zone reconfiguration with large task counts
- Replace `<svelte:window onclick>` handlers in SearchBar and ExportButton with scoped click-outside detection to reduce global event listener overhead
- Add an E2E test that loads a large dataset and verifies navbar navigation from the task page

## Non-goals

- Task virtualization / windowed rendering (future optimization if needed)
- Changing the drag-and-drop library
- Restructuring the three-panel layout

## Capabilities

### New Capabilities
- `nav-reliability`: Ensures navbar navigation works reliably from the task page regardless of data volume

### Modified Capabilities
_None — this is a bug fix, not a requirements change._

## Impact

- **Frontend components**: `+layout.svelte` (navbar), `+page.svelte` (task page), `TaskList.svelte`, `SearchBar.svelte`, `ExportButton.svelte`, `keyboard.ts` action
- **Dependencies**: `svelte-dnd-action@0.9.69` — the library's `handleMouseDown` calls `e.stopPropagation()` on every mousedown within a dndzone; with many draggable items this amplifies event interference
- **E2E tests**: New test using `temp.json` fixture data to reproduce and prevent regression
