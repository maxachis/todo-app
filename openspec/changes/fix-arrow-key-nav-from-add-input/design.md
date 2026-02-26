## Context

The keyboard action (`frontend/src/lib/actions/keyboard.ts`) uses an `isTextEntryTarget()` guard at the top of its `handleKeydown` handler (line 39). This guard checks whether `event.target` is inside an `input`, `textarea`, `select`, or `[contenteditable]` element — if so, the entire handler returns early and no keyboard shortcut is processed.

This is correct for most text fields (task title editing, notes, search) where arrow keys should move the cursor within the text. However, for the task-add input (`TaskCreateForm.svelte`), the user expectation is different: pressing Arrow Up/Down should exit the input and navigate to nearby tasks, since the add-task input sits inline within the task list.

## Goals / Non-Goals

**Goals:**
- Arrow Up/Down in the task-add input navigates to the nearest task (blurring the input)
- Other text-entry fields (task detail title, notes textarea, search bar) continue to suppress arrow-key navigation as they do today
- Escape in the task-add input clears any typed text and blurs the field

**Non-Goals:**
- Changing keyboard behavior in any text field other than the task-add input
- Adding new keyboard shortcuts to TaskCreateForm beyond arrow navigation and Escape
- Modifying the `isTextEntryTarget` guard itself — the guard is correct for the general case

## Decisions

### Handle arrow keys in TaskCreateForm directly

**Decision**: Add an `onkeydown` handler to the task-add `<input>` in `TaskCreateForm.svelte` that intercepts Arrow Up, Arrow Down, and Escape, then blurs the input.

**Rationale**: This keeps the fix self-contained in `TaskCreateForm.svelte` without modifying the shared keyboard action. The keyboard action's `isTextEntryTarget` guard remains intact for all other inputs. Once the input is blurred, the keyboard action's event listener on the parent node will naturally handle navigation on subsequent keypresses.

**How it works**:
1. TaskCreateForm's `<input>` gets an `onkeydown` handler
2. On Arrow Up/Down: call `event.preventDefault()`, blur the input, then dispatch a new `keydown` event on the keyboard-scope container so navigation happens immediately (not requiring a second keypress)
3. On Escape: clear the input value, blur the input

**Alternative considered**: Modifying `isTextEntryTarget` to whitelist certain inputs (e.g., by class or data attribute). Rejected because it couples the generic keyboard action to specific component knowledge, and the guard's broad suppression is the correct default.

**Alternative considered**: Dispatching the event on `document` instead of the keyboard-scope node. Rejected because the keyboard action listens on a specific node (`use:keyboard` container), not on `document`.

### Find the keyboard-scope node via DOM traversal

**Decision**: Use `inputElement.closest('[data-keyboard-scope]')` (or equivalent selector for the keyboard action's container) to find the right dispatch target.

**Rationale**: The keyboard action is applied to a `<div>` wrapping the task area in `+page.svelte`. Rather than importing store references or passing callbacks, the simplest approach is to find this ancestor via DOM and dispatch the synthetic event there.

**Refinement**: Looking at `+page.svelte`, the keyboard action is applied via `use:keyboard` on a div. We can add a `data-keyboard-scope` attribute to that div, or simply use the existing structure — the `TaskCreateForm` is always a descendant of the keyboard-scoped node, so `event.currentTarget.closest()` from the input's perspective or `inputElement.parentElement` traversal will work. The most robust approach: `inputElement.closest('.task-area')` or dispatch on `document.body` — but since the keyboard handler listens on a specific node, we should use `closest` with an identifiable selector.

## Risks / Trade-offs

- **Synthetic event dispatch**: Dispatching a new `KeyboardEvent` after blur is slightly unusual, but it's a well-supported browser API and keeps the keyboard action completely unaware of this fix. Risk is minimal.
- **Focus state after navigation**: After blur + dispatch, the keyboard action will select a task via `onSelectTask`. The task row itself doesn't receive DOM focus (selection is store-driven), so there's no focus conflict. Low risk.
- **Escape behavior overlap**: Escape already has meaning in the keyboard action (clear task selection). Since we handle Escape in the input's own handler and the input will be blurred, the keyboard action may also fire Escape on the next keypress. This is acceptable — clearing selection when no input is focused is fine. We should `stopPropagation()` on Escape in the input handler to prevent double-firing.
