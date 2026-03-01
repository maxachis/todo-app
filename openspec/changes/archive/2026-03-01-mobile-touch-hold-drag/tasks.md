## 1. Add delayTouchStart to DragContainer

- [x] 1.1 Add `delayTouchStart` prop to `DragContainer.svelte` with default value `200`, typed as `boolean | number` — pass it through to both `dndzone` and `dragHandleZone` directive option objects (`frontend/src/lib/components/dnd/DragContainer.svelte`)

## 2. Verify all DnD zone consumers

- [x] 2.1 Confirm `TaskList.svelte`, `SubtaskTree.svelte`, `PinnedSection.svelte` use `DragContainer` and inherit the new default without per-component changes (`frontend/src/lib/components/tasks/`)
- [x] 2.2 Confirm `SectionList.svelte` (uses `dragHandleZone` via `DragContainer`) inherits the delay (`frontend/src/lib/components/sections/SectionList.svelte`)
- [x] 2.3 Confirm `ListSidebar.svelte` inherits the delay (`frontend/src/lib/components/lists/ListSidebar.svelte`)

## 3. Manual testing

- [x] 3.1 Test on mobile/touch: short tap does not start drag, scroll gesture works normally, touch-and-hold (~200ms) activates drag
- [x] 3.2 Test on desktop: mouse drag still starts immediately with no delay
- [x] 3.3 Test all DnD zones (task list, subtask tree, pinned section, section reorder, list sidebar) on touch device
