## Context

The keyboard action (`frontend/src/lib/actions/keyboard.ts`) handles Tab to indent/outdent tasks. The Tab handler calls `options.onIndentTask()` or `options.onOutdentTask()`, which call `moveTask()` in the tasks store. `moveTask()` calls `refreshListDetail()`, which reloads the entire list from the API and replaces the Svelte store value. This causes all task row DOM elements to be destroyed and recreated. The previously-focused task row element no longer exists, so `document.activeElement` falls to `document.body`, and subsequent arrow key / j/k presses have no effect because `resolvedCurrentId` resolves to `null`.

## Goals / Non-Goals

**Goals:**
- After Tab indent/outdent, the moved task's row element retains focus so keyboard navigation continues immediately
- No visible flicker or delay for the user

**Non-Goals:**
- Changing how `refreshListDetail()` works (full list reload is the established pattern)
- Focus restoration for other async operations (complete, delete, drag-drop)

## Decisions

### Decision 1: Restore focus in the keyboard action's Tab handler after the async operation

**Approach**: After `await options.onIndentTask()`/`onOutdentTask()` returns, use `tick()` (Svelte's microtask flush) then query the DOM for the task element with the same `data-task-id` and call `.focus()` on it.

**Why this over alternatives**:
- *Alternative: Restore focus inside `moveTask()`* — The store layer shouldn't know about DOM focus; that's a UI concern.
- *Alternative: Use `afterUpdate` lifecycle* — More complex and would fire on every update, not just Tab operations.
- *Alternative: Restore focus in `+page.svelte` callbacks* — The keyboard action already owns the Tab handler and has the task ID; keeping focus logic co-located is simpler.

### Decision 2: Use `requestAnimationFrame` as fallback timing

After `tick()`, if the element isn't found yet (possible if the store update triggers an async re-render), retry once with `requestAnimationFrame`. This handles edge cases where Svelte's microtask flush completes before the DOM is fully painted.

## Risks / Trade-offs

- [Risk] The task row element may briefly not exist between store update and re-render → Mitigation: `tick()` + `requestAnimationFrame` fallback covers both sync and async render paths.
- [Risk] If the task ID changes during indent (it shouldn't — only parent/position change) → Mitigation: The API returns the same task ID; only hierarchy changes.
