## Why

When a user double-clicks a task name to edit it, the input field appears correctly. However, clicking inside the input (e.g., to reposition the cursor) immediately exits edit mode. This makes inline task name editing unusable for anything beyond typing and pressing Enter — the user cannot click to place their cursor within the text.

## What Changes

- Fix the task name inline edit input so that clicks within it do not bubble up to the parent row's click handler, which steals focus from the input and triggers its `onblur` → `commitEdit` → `editing = false` chain.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `svelte-frontend`: Fix event propagation on the inline task title edit input in `TaskRow.svelte` so clicks inside the input stay within the input.

## Impact

- **Code**: `frontend/src/lib/components/tasks/TaskRow.svelte` — the `<input class="title-input">` element (lines 193-202).
- **Root cause**: The parent `.task-row` div's `onclick` handler calls `(event.currentTarget as HTMLElement).focus()`, which moves focus to the div, triggering `onblur` on the input and exiting edit mode.
- **Fix scope**: Add `onclick` with `stopPropagation()` to the title input so parent click/focus handling is not triggered. No API, dependency, or other component changes needed.
