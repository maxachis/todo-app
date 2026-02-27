## Context

The `TypeaheadSelect` component has two code paths when the user types text that matches no options:

1. **With `onCreate`**: Dropdown stays open, shows a "Create [text]" item — good UX.
2. **Without `onCreate`**: Dropdown closes silently, typed text is discarded on blur — bad UX.

This affects all consumers that don't provide `onCreate`, including LinkedEntities (people/org selectors on tasks) and the people page quick-log interaction type field.

## Goals / Non-Goals

**Goals:**
- Show a non-selectable "not found" message in the dropdown when no options match and no `onCreate` is provided
- Keep the dropdown open so the user sees feedback
- Preserve typed text while the message is visible

**Non-Goals:**
- Adding `onCreate` callbacks to existing consumers
- Changing behavior for TypeaheadSelects that already have `onCreate`
- Making the "not found" item selectable or interactive

## Decisions

### 1. Add a `showNoMatch` derived state alongside `showCreateOption`

**Decision**: Introduce a new derived boolean `showNoMatch` that is true when `inputText` is non-empty, `filtered` is empty, and `onCreate` is not provided. This mirrors the existing `showCreateOption` pattern.

**Why**: Keeps the two empty-state paths clearly separated. `showCreateOption` handles the "can create" case, `showNoMatch` handles the "can't create" case. Both feed into dropdown visibility logic the same way.

**Alternative considered**: A single `emptyStateMode` enum — rejected because it adds indirection for only two mutually exclusive states that are already cleanly expressed as booleans.

### 2. Render a non-selectable `<li>` with `role="status"` for the message

**Decision**: Add a `<li>` with muted styling (similar to `.typeahead-create` but non-interactive) and `role="status"` instead of `role="option"`. No `onmousedown`, no hover highlight, not included in `totalItems` count.

**Why**: The item is informational, not actionable. Excluding it from keyboard navigation and the option count avoids confusing both sighted users and screen reader users. Using `role="status"` signals it's a live status message.

### 3. Update `handleInput` dropdown-open logic

**Decision**: Change the condition at line 99 from `filtered.length > 0 || showCreateOption` to `filtered.length > 0 || showCreateOption || showNoMatch`. Same change in the `{#if}` guard on line 205.

**Why**: Minimal change — extends the existing pattern rather than restructuring it.

### 4. Message text: "No match found — add it first"

**Decision**: Use static text "No match found — add it first" rather than interpolating the typed text.

**Why**: The user can already see what they typed in the input. Repeating it in the dropdown adds clutter. The message focuses on what to do next (add the item via its dedicated page).

## Risks / Trade-offs

- **Dropdown stays open with no selectable items**: Minor visual change, but the muted non-interactive styling makes it clear nothing can be selected. Low risk.
- **All consumers without `onCreate` get this behavior**: This is intentional and desirable — the proposal explicitly states it. No consumer-specific opt-out is needed.
