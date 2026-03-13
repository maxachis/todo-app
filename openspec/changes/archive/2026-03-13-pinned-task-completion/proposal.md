## Why

Pinned tasks on the Tasks page are high-priority items the user wants quick access to, but completing them requires scrolling to find the task in its section and clicking its checkbox. Adding a completion checkbox directly in the pinned section removes this friction and lets users check off their most important tasks without leaving the pinned area.

## What Changes

- Add a completion checkbox to each pinned task row in the PinnedSection component
- Clicking the checkbox completes the task via the existing `completeTask` store function
- Completed tasks are automatically removed from the pinned section (existing filter: `task.is_pinned && !task.is_completed`)
- Checkbox click does not trigger the "jump to task" navigation behavior

## Non-goals

- No undo toast for pinned task completion (the task detail panel and uncomplete flow already exist)
- No changes to the Dashboard pinned group (already has its own completion checkbox via `dashboard-task-completion`)
- No changes to the pin/unpin mechanism itself

## Capabilities

### New Capabilities
- `pinned-task-checkbox`: Completion checkbox on pinned task rows in the Tasks page PinnedSection

### Modified Capabilities

## Impact

- `frontend/src/lib/components/tasks/PinnedSection.svelte` — add checkbox element and completion handler
- Relies on existing `completeTask` from `$lib/stores/tasks`
