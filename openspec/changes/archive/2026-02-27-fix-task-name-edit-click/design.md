## Context

The `TaskRow.svelte` component supports double-click-to-edit for task titles. When the user double-clicks, `editing` becomes `true` and an `<input>` replaces the `<span>`. However, the parent `.task-row` div has an `onclick` handler that calls `selectTask()` and then `event.currentTarget.focus()`, stealing focus from the input. This triggers the input's `onblur={commitEdit}`, which sets `editing = false`, immediately exiting edit mode.

The checkbox already handles this correctly — its label wrapper has `onclick={(e) => e.stopPropagation()}` (line 179).

## Goals / Non-Goals

**Goals:**
- Clicks inside the title input stay within the input and do not exit edit mode
- Existing behavior (double-click to enter edit, Enter to commit, Escape to cancel, blur to commit) remains unchanged

**Non-Goals:**
- Changing the edit trigger (e.g., single-click to edit)
- Adding additional inline edit features (selection, undo, etc.)

## Decisions

**Add `stopPropagation` to the title input's click handler**: This prevents the click from bubbling to the `.task-row` div's `onclick`, which would steal focus. This matches the existing pattern used by the checkbox wrapper on line 179.

Alternative considered: Checking `event.target` in `handleClick` to skip focus-stealing when the target is an input. Rejected because `stopPropagation` is simpler, more explicit, and already established as the pattern in this component.

## Risks / Trade-offs

- [Minimal risk] Adding `stopPropagation` means a click inside the title input won't trigger `selectTask()`. This is acceptable because the task is already selected when edit mode is entered (you must click/select the task before double-clicking to edit). → No mitigation needed.
