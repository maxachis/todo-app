## Context

The task drag-and-drop system uses two complementary mechanisms:

1. **svelte-dnd-action** (library) in `TaskList.svelte` and `SubtaskTree.svelte` — handles flat reordering within a parent via pointer-event-based drag with consider/finalize events and FLIP animations
2. **Native HTML5 DnD** handlers on `TaskRow.svelte` — handles midpoint-based nesting (`ondragstart`, `ondragover`, `ondrop`)

svelte-dnd-action provides the drag gesture (pointer events, visual feedback, animated placeholders) while the native DnD handlers on TaskRow provide midpoint-based nesting. Both systems coexist: svelte-dnd-action handles same-level reordering, and the TaskRow drop handlers handle parent-id changes for nesting.

The `midpointDropMode()` function implements the core detection logic (above midpoint = "before", below midpoint = "nest"), and the backend `move_task` endpoint already supports `parent_id` changes with circular-nesting protection. The infrastructure is in place — the improvements needed are a frontend circular-nesting guard and clearer visual feedback for nesting intent.

## Goals / Non-Goals

**Goals:**
- Single, predictable drag-and-drop interaction for tasks that supports both reordering (place before) and nesting (make subtask) based on cursor position relative to the drop target's midpoint
- Clear visual feedback showing whether a drop will reorder or nest
- Works at any nesting depth (subtask, sub-subtask, etc.)
- Frontend guard against circular nesting (don't wait for a 409 from the backend)
- Maintains the existing drag lock mechanism to prevent concurrent operations

**Non-Goals:**
- Changing section or list drag-and-drop (those keep svelte-dnd-action)
- Touch/mobile drag support
- Animated placeholder repositioning during drag (FLIP-style) — the static visual indicators (top-line for "before", left-accent for "nest") are sufficient
- Cross-list task dragging via the center panel

## Decisions

### 1. Keep svelte-dnd-action for drag gesture; enhance native DnD for nesting

**Decision:** Keep `DragContainer`/`DragItem` wrappers in `TaskList.svelte` and `SubtaskTree.svelte`. svelte-dnd-action handles the drag gesture (pointer-event-based, works across browsers including Firefox/Linux) and same-level reordering. The native HTML5 DnD handlers on `TaskRow.svelte` handle midpoint-based nesting when the user drops below a task's midpoint.

**Rationale:** Native HTML5 DnD is unreliable across browser/OS combinations (particularly Firefox on Linux). svelte-dnd-action uses pointer events which work universally. The two systems coexist: svelte-dnd-action handles the drag initiation and reorder finalization, while TaskRow's ondragover/ondrop handlers handle nesting with midpoint detection.

**Enhancements over the original:**
- Explicit `draggable` attribute with string values (`'true'`/`'false'`) for correct HTML semantics
- `effectAllowed = 'move'` and `dropEffect = 'move'` set on dataTransfer for proper browser feedback
- Frontend circular-nesting guard (see Decision 3)

### 2. Midpoint detection determines reorder vs nest

**Decision:** Keep the existing `midpointDropMode()` function on `TaskRow`. Above the midpoint = "before" (insert at target's level, before the target). Below the midpoint = "nest" (make child of target at position 0).

**Rationale:** This is the most intuitive gesture — the top half of the task row represents "insert above me at my level," the bottom half represents "put it inside me." It already exists and works well.

### 3. Add frontend circular-nesting guard

**Decision:** Before calling `moveTask` in `handleDropOnTask`, check whether the drop target is a descendant of the dragged task. If so, abort the drop silently (clear dropMode, return early).

**Rationale:** The backend already returns a 409 for circular nesting, but the frontend should catch this before making the API call to avoid a flash of incorrect state and an error toast. The check is simple: walk up the target's parent chain and verify the dragged task's ID doesn't appear.

**Implementation:** Add a `isDescendantOf(taskId: number, potentialAncestorId: number)` utility that traverses the task tree from the store. Call it in `handleDropOnTask` when `midpointDropMode === 'nest'`.

### 4. Render task items directly without DragContainer/DragItem wrappers

**Decision:** In `TaskList.svelte` and `SubtaskTree.svelte`, render `TaskRow` components in a plain `{#each}` block. Task reordering is handled by `TaskRow`'s `handleDropOnTask` (the "before" branch already computes the correct sibling index).

**Rationale:** The `DragContainer` and `DragItem` components are svelte-dnd-action wrappers. Without svelte-dnd-action for tasks, they add no value. Removing them simplifies the component tree and reduces wrapper divs.

### 5. Keep svelte-dnd-action for sections and lists

**Decision:** `DragContainer`/`DragItem` remain for section reordering and list reordering in the sidebar. These are flat lists without nesting concerns.

**Rationale:** Section and list reordering is purely positional (no nesting). svelte-dnd-action works perfectly for this use case and provides nice FLIP animations.

### 6. Improve drop visual indicators

**Decision:** Enhance the existing CSS indicators for clarity:
- **"before" mode**: Horizontal accent line above the task row (existing `box-shadow: inset 0 2px 0`)
- **"nest" mode**: Left accent bar plus a subtle background tint to clearly indicate "this task will become a child"

**Rationale:** The current `drop-nest` style uses the same `inset 3px 0 0` as the selected state, which can be confusing. Adding a background tint differentiates nesting intent from selection.

## Risks / Trade-offs

- **[Loss of FLIP animations]** → Acceptable trade-off. Static indicators are clear and predictable. Could add CSS transitions on position changes via `animate:flip` in Svelte's `{#each}` blocks later if desired.
- **[svelte-dnd-action removal scope]** → Only affects task containers. Section and list DnD remain unchanged. Mitigated by keeping the DragContainer/DragItem components for non-task uses.
- **[Deep nesting performance]** → The `isDescendantOf` check walks the task tree. With typical nesting depths (2-4 levels), this is negligible. Tasks with 10+ nesting levels are rare.
- **[Regression risk in existing reorder behavior]** → The "before" branch of `handleDropOnTask` already handles reordering correctly. It computes sibling index and calls `moveTask` with the same parameters that svelte-dnd-action's finalize was using. Risk is low since the logic already exists and works.

## Open Questions

- None. The approach builds directly on existing, tested code paths. The main change is removing the competing DnD system.
