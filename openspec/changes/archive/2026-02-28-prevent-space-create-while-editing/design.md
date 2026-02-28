## Context

The `.task-row` div in `TaskRow.svelte` has `role="button"` and an `onkeydown` handler that intercepts `Enter` and `Space` to call `handleClick()` for accessibility. This is standard: ARIA button roles should activate on both Enter and Space.

However, when the user double-clicks a task to inline-edit its title, an `<input>` element appears inside the same `.task-row` div. Keydown events from this input bubble up to the parent div's handler, which catches space, calls `preventDefault()` (blocking the character), and triggers `handleClick()`.

The codebase already solves this pattern elsewhere: `keyboard.ts` uses an `isTextEntryTarget()` function that checks if the event target is inside `input, textarea, select, [contenteditable="true"]` and returns early if so.

## Goals / Non-Goals

**Goals:**
- Allow normal text entry (including spaces) when inline-editing a task title in TaskRow
- Reuse the existing `isTextEntryTarget` pattern for consistency

**Non-Goals:**
- Modifying the global keyboard action in `keyboard.ts` (already correct)
- Changing TaskDetail panel behavior (unaffected — it's outside the keyboard scope)
- Refactoring the accessibility pattern on `.task-row`

## Decisions

**1. Guard the `onkeydown` handler with an `isTextEntryTarget` check**

Add a check at the top of the `.task-row` onkeydown handler: if `event.target` is inside an `input`, `textarea`, `select`, or `[contenteditable]`, return immediately without processing the key.

*Alternative considered*: Use `stopPropagation()` in the inline edit input's own keydown handler. Rejected because stopPropagation can break other listeners and is harder to maintain. The guard-at-parent approach is already the established pattern in this codebase.

**2. Inline the check rather than importing from `keyboard.ts`**

The `isTextEntryTarget` function in `keyboard.ts` is not exported and is a simple one-liner. Rather than exporting it and creating a cross-module dependency for a single check, inline the same logic directly in the `onkeydown` handler.

*Alternative considered*: Export `isTextEntryTarget` from `keyboard.ts` and import it in `TaskRow.svelte`. This would be warranted if more components needed it, but currently only these two locations use it.

## Risks / Trade-offs

- **Duplicated logic**: The `isTextEntryTarget` check exists in two places. Low risk since both are simple and unlikely to diverge. If a third location needs it, consolidate at that point.
