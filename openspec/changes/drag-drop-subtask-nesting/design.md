## Context

The task drag-and-drop system currently uses two competing mechanisms:

1. **svelte-dnd-action** (library) in `TaskList.svelte` and `SubtaskTree.svelte` — handles flat reordering within a parent via consider/finalize events
2. **Native HTML5 DnD** handlers on `TaskRow.svelte` — handles midpoint-based nesting (`ondragstart`, `ondragover`, `ondrop`)

Both systems share `type="task-dnd"` zones and the `taskDragLockedStore` lock, but they fire concurrently during a drag. When a user drops a task, svelte-dnd-action's `onfinalize` may trigger a flat reorder at the same time as `TaskRow.handleDropOnTask` attempts a nest or positional insert. This race condition leads to unpredictable results, especially at deeper nesting levels.

The `midpointDropMode()` function already implements the core detection logic (above midpoint = "before", below midpoint = "nest"), and the backend `move_task` endpoint already supports `parent_id` changes with circular-nesting protection. The infrastructure for both reordering and nesting is in place — the problem is the conflicting event handling.

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

### 1. Remove svelte-dnd-action from task containers; use only native HTML5 DnD

**Decision:** Remove `DragContainer`/`DragItem` wrappers from `TaskList.svelte` and `SubtaskTree.svelte` for task items. Rely entirely on native HTML5 drag-and-drop handlers already on `TaskRow.svelte`.

**Rationale:** svelte-dnd-action operates on flat arrays and has no concept of hierarchical nesting. Its `onfinalize` callback receives a reordered array and always interprets drops as positional reorders. It cannot express "this drop means nest task A under task B." Trying to intercept or override its behavior creates fragile coordination code. Removing it eliminates the root cause of the dual-system conflict.

**Alternatives considered:**
- *Keep svelte-dnd-action, override finalize*: Would require hooking into internal drag state to read cursor position at drop time — svelte-dnd-action doesn't expose this. Fragile.
- *Keep svelte-dnd-action for "before" only, disable for "nest"*: Would need to dynamically toggle `dropFromOthersDisabled` based on real-time midpoint detection during `ondragover`, which still creates timing conflicts.

**Trade-off:** We lose svelte-dnd-action's animated placeholder (FLIP animation during consider). Tasks won't visually "shuffle" during drag. Instead, the static CSS indicators (`drop-before` line, `drop-nest` accent) provide clear feedback. This is acceptable for a task management tool where precision matters more than animation.

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
