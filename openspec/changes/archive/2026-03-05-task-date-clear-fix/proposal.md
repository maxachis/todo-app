## Why

Clearing a task's due date in TaskDetail doesn't work — the date resets to its previous value. The root cause is a `$effect` that syncs local form state from the reactive `task` prop: it resets `dueDateValue` whenever the task object changes, overwriting the user's in-progress edit before the save can complete. This affects any field edited via the detail panel, but is most visible with dates because clearing produces a visually obvious snap-back.

## What Changes

- Fix the `$effect` in TaskDetail to only reset local form values when the **task ID** changes (i.e., the user selects a different task), not on every task object mutation
- This prevents the effect from overwriting in-progress edits when the store updates after a save

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

_(none — this is a bug fix in component logic, not a spec-level behavior change; the existing behavior spec already implies that clearing a date should persist)_

## Non-goals

- Changing how other fields (title, priority, notes) save — though they benefit from the same fix
- Adding a dedicated "clear date" button
- Changing the save-on-blur pattern

## Impact

- **Frontend**: `frontend/src/lib/components/tasks/TaskDetail.svelte` — modify the `$effect` to track task ID changes instead of full task object changes
- **No backend changes**
