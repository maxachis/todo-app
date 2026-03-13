## 1. Fix focus restoration after Tab indent/outdent

- [x] 1.1 In `frontend/src/lib/actions/keyboard.ts`, add a helper function `restoreFocus(node, taskId)` that queries for `[data-task-id="${taskId}"]` within the keyboard scope node and calls `.focus()` on it
- [x] 1.2 In the Tab handler (lines 118-142), after `await options.onIndentTask()` and `await options.onOutdentTask()` return, call `tick()` then `restoreFocus()` to re-focus the moved task's row element
- [x] 1.3 Add `requestAnimationFrame` fallback in `restoreFocus()` — if the element isn't found after `tick()`, retry once in the next animation frame

## 2. Verify

- [x] 2.1 Manual test: select a task, press Tab to indent, then press ArrowDown — next task should be selected
- [x] 2.2 Manual test: select a nested task, press Shift+Tab to outdent, then press ArrowUp — previous task should be selected
- [x] 2.3 Manual test: press Tab on a task with no valid sibling (no-op) — keyboard navigation still works
