## Why

When completing a task — especially one near the bottom of a long list — the screen briefly flashes black. The task is synchronously removed from the active DnD zone, the section shrinks instantly, and the scroll container exposes its dark page background (`--bg-page`) before the browser can repaint. The completion check animation plays on the checkbox but the task row is yanked from the DOM in the same frame.

## What Changes

- Delay removal of a completed task from the active task list by ~300ms so the check animation can play and the scroll position adjusts smoothly.
- The task row already has a `.completed` class that sets `opacity: 0.5` — this will be visible during the delay, giving a natural "fading out" feel before the task disappears.

## Non-goals

- Adding a CSS out-transition or slide animation on removal — this would conflict with `svelte-dnd-action`'s DOM management.
- Changing scroll behavior or panel backgrounds — that would be a workaround, not a fix.
- Changing the completed section toggle or DnD container behavior.

## Capabilities

### New Capabilities

_(none — this is a bug fix to existing behavior)_

### Modified Capabilities

_(no spec-level requirement changes — the task completion behavior is the same, just smoother)_

## Impact

- **`frontend/src/lib/components/tasks/TaskList.svelte`**: The `$effect` that filters `sortableActiveTasks` needs to defer removal of newly-completed tasks.
- No backend changes. No new dependencies.
