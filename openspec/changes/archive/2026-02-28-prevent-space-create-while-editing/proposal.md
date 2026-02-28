## Why

When inline-editing a task title in the task list (via double-click), pressing the space bar does not insert a space character. Instead, the space keydown event bubbles from the `<input>` up to the parent `.task-row` div, where the accessibility keydown handler intercepts `' '`, calls `preventDefault()`, and re-triggers `handleClick()`. This makes it impossible to type multi-word task titles during inline editing.

## What Changes

- **Fix space/Enter key handler on `.task-row`**: Guard the `onkeydown` handler in `TaskRow.svelte` so it ignores key events originating from text-entry elements (`input`, `textarea`, `select`, `[contenteditable]`), matching the same `isTextEntryTarget` pattern already used in the global `keyboard.ts` action.

## Non-goals

- Changing the global keyboard action in `keyboard.ts` (it already correctly guards with `isTextEntryTarget`).
- Modifying TaskDetail panel editing behavior (TaskDetail is outside the keyboard scope and unaffected).

## Capabilities

### New Capabilities
- `task-row-edit-guard`: Guard the TaskRow accessibility keydown handler to allow normal text input during inline editing.

### Modified Capabilities

## Impact

- **`frontend/src/lib/components/tasks/TaskRow.svelte`**: The `onkeydown` handler on the `.task-row` div (lines 148–153) needs a guard check before processing space/Enter keys.
