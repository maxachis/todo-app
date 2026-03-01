## Context

The app uses `svelte-dnd-action` (v0.9.69) for all drag-and-drop via a shared `DragContainer.svelte` wrapper. On mobile/touch devices, touching a task immediately begins a drag operation, interfering with scroll gestures and accidental taps. The library already provides a `delayTouchStart` option (boolean or milliseconds) that gates drag initiation behind a touch-hold delay, but it is not currently used anywhere in the app.

All DnD zones flow through `DragContainer.svelte`, which passes configuration to either `dndzone` or `dragHandleZone` directives. The `dragDisabled` prop is already wired up and used by `taskDragLockedStore` to prevent drags during API calls.

## Goals / Non-Goals

**Goals:**
- Prevent accidental drag initiation on touch devices when the user intends to scroll or tap
- Require a deliberate touch-and-hold (~200ms) before drag activates
- Keep desktop mouse drag behavior unchanged (immediate)

**Non-Goals:**
- Adding a visible drag handle icon for mobile
- Changing any drag-and-drop reorder/nest logic
- Adding haptic feedback (browser API support is inconsistent)

## Decisions

### Decision 1: Use `delayTouchStart` from svelte-dnd-action

**Choice:** Pass `delayTouchStart` to the `dndzone`/`dragHandleZone` directives via `DragContainer.svelte`.

**Rationale:** The library natively supports this option — it accepts `true` (80ms default) or a number in ms. This avoids custom touch event handling, keeps the solution minimal, and is the approach recommended by the library maintainer.

**Alternatives considered:**
- *Custom long-press handler toggling `dragDisabled`*: More control and enables visual feedback during the hold, but significantly more complex (touch event listeners, timer management, cleanup, interaction with existing pointer events). Overkill for the core problem.
- *CSS `touch-action: pan-y`*: Would allow vertical scrolling but break horizontal drag — doesn't solve the fundamental "tap vs drag" ambiguity.

### Decision 2: Use 200ms delay

**Choice:** Set `delayTouchStart` to `200` (milliseconds).

**Rationale:** The library default of 80ms is too short to feel deliberate. 200ms is long enough to distinguish scroll flicks from intentional holds, but short enough to feel responsive. This aligns with common mobile UX patterns (iOS uses ~150-200ms for similar gestures). Can be tuned later if needed.

### Decision 3: Single change point in DragContainer.svelte

**Choice:** Add `delayTouchStart` as a prop on `DragContainer.svelte` with a default of `200`, and pass it through to both `dndzone` and `dragHandleZone` directives.

**Rationale:** All DnD zones in the app go through this single wrapper. Changing it once applies the behavior everywhere — task lists, subtask trees, pinned sections, section lists, list sidebar. No per-component changes needed.

## Risks / Trade-offs

- **[Minor UX shift]** Users who were comfortable with instant touch-drag will now need to hold slightly longer. → 200ms is short enough that most users won't notice; those who do will benefit from fewer accidental drags.
- **[No visual hold feedback]** Unlike a custom implementation, `delayTouchStart` doesn't show a visual indicator during the hold period. → Acceptable trade-off for simplicity. The drag shadow appearing after the delay is sufficient feedback. Can add visual feedback later if user testing reveals confusion.
- **[Library reliance]** Depending on svelte-dnd-action's internal touch handling. → The library is mature (v0.9.69) and this feature has been stable since its introduction. Low risk.
