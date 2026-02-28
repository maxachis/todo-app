## Context

The Tasks route uses a three-panel layout: sidebar, center task list, and right detail panel. Keyboard shortcuts are managed by a Svelte action (`keyboard.ts`) attached to a `.keyboard-scope` div wrapping the center panel content. The detail panel (TaskDetail) is rendered as a sibling in the layout, outside the keyboard scope.

When a user clicks a task row, the row receives focus and `selectedTaskStore` is set. The detail panel then shows that task's editable fields (title, due date, priority, notes, tags, linked entities). The problem: if focus remains on (or returns to) the task row in the center panel while the user is mentally "in" the detail panel, pressing "x" triggers the complete-task shortcut.

Current guard logic in `keyboard.ts`:
- `isTextEntryTarget(event.target)` — returns early if focus is on `input`, `textarea`, `select`, or `[contenteditable]`
- This correctly prevents shortcuts while typing in form fields, but does NOT prevent shortcuts when focus is on a task row element while the detail panel is open

## Goals / Non-Goals

**Goals:**
- Prevent "x" and "Delete" single-key shortcuts from firing unless focus is explicitly on a task row element (`[data-task-id]`)
- Maintain all other keyboard shortcuts (j/k, arrow keys, Tab/Shift+Tab, Ctrl+arrows, Escape) unchanged

**Non-Goals:**
- Changing the keybinding from "x" to a modifier combo
- Adding auto-focus behavior to the detail panel on task selection
- Modifying navigation shortcuts (they're non-destructive and should keep working broadly)

## Decisions

### Decision 1: Guard destructive shortcuts by checking the event target is a task row

**Choice**: For "x" (complete) and "Delete" (delete), add an additional check that the event originated from a `[data-task-id]` element (or a descendant of one).

**Rationale**: These are destructive single-key shortcuts. Requiring that the event target be a task row element ensures they only fire when the user is clearly interacting with a task in the center panel list, not when focus has drifted to other elements inside the keyboard scope (e.g., section headers, create-form buttons).

**Alternative considered**: Check `document.activeElement` against the detail panel — rejected because the detail panel is already outside the keyboard scope. The real issue is non-task-row elements *inside* the keyboard scope (like section create forms after blurring, header buttons, etc.) that can receive focus.

**Alternative considered**: Use `event.target.closest('[data-task-id]')` — this is the chosen approach and is already computed as `eventElement` in the handler.

### Decision 2: Use existing `eventElement` variable

The keyboard handler already computes `eventElement = event.target.closest('[data-task-id]')`. For "x" and "Delete", guard with `if (eventElement === null) return;` so the shortcut only fires when the event target is within a task row.

## Risks / Trade-offs

- **[Minor behavior change]** If a user somehow focuses a non-task-row element inside the keyboard scope (e.g., a section header or "Add section" button) and presses "x", it will now be silently ignored instead of completing the selected task. This is the desired behavior. → No mitigation needed.
- **[Consistency]** Navigation shortcuts (j/k, arrows) still work from any element in the keyboard scope, while destructive shortcuts require task-row focus. This asymmetry is intentional — navigation is non-destructive. → Document the behavior difference in code comments.
