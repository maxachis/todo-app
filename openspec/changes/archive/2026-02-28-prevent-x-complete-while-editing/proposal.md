## Why

Pressing "x" while a task is selected completes it via keyboard shortcut, even when the user is actively working in the task detail panel (editing title, notes, tags, etc.). If focus remains on the task row in the center panel after selecting a task — or returns there after blurring a detail-panel input — an accidental "x" keystroke triggers task completion. This is a data-integrity issue: the user intends to interact with detail fields, not mark the task done.

## What Changes

- Guard the "x" (complete) and "Delete" keyboard shortcuts so they only fire when the focused element is an actual task row (`[data-task-id]`), not just any non-text-entry element inside the keyboard scope.
- This prevents accidental completion when focus drifts back to the keyboard scope while the user is working in the detail panel.

## Non-goals

- Changing the "x" keybinding to a different key or requiring a modifier (Ctrl+X). The shortcut remains "x" — it just becomes context-aware.
- Adding focus management to the detail panel (auto-focusing inputs on task selection). That would be a separate UX improvement.

## Capabilities

### New Capabilities

_(none — this is a bug fix to existing keyboard navigation behavior)_

### Modified Capabilities

- `svelte-frontend`: Keyboard shortcut guard logic in the keyboard action is tightened to require focus on a task row element for destructive single-key shortcuts.

## Impact

- **Code**: `frontend/src/lib/actions/keyboard.ts` — modify the "x" and "Delete" key handlers to check `document.activeElement` or `event.target` against `[data-task-id]`.
- **Risk**: Low. Only affects single-key destructive shortcuts; modifier-key and navigation shortcuts are unaffected.
- **Tests**: Existing E2E keyboard tests should still pass; may add a targeted test confirming "x" does not fire when focus is not on a task row.
