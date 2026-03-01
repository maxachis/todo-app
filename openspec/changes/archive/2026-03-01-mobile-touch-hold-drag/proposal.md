## Why

On mobile devices, touching a task to scroll the list or tap a checkbox/link accidentally initiates a drag-and-drop operation. Users need a deliberate gesture — a touch-and-hold (long press) — before dragging begins, so that normal scrolling and tapping remain unaffected.

## What Changes

- Add a touch-hold delay before drag-and-drop activates on mobile/touch devices
- Normal taps and scroll gestures remain unaffected — only a sustained touch (~200-300ms) triggers drag mode
- Desktop mouse-based drag remains unchanged (immediate on mousedown)
- Visual feedback on the held task to indicate drag mode is activating (e.g., subtle scale or highlight)

### Non-goals

- Changing the existing drag-and-drop reorder/nest logic or API persistence
- Adding a dedicated drag handle for mobile (the hold gesture replaces the need for handles)
- Changing desktop drag behavior in any way

## Capabilities

### New Capabilities
- `mobile-touch-hold-drag`: Touch-and-hold gesture gate for drag-and-drop on mobile/touch devices, including hold detection, visual feedback, and scroll preservation

### Modified Capabilities
- `drag-drop-subtask-nesting`: The drag initiation path changes on touch devices (hold-to-drag gate added before existing DnD logic kicks in), but the reorder/nest behavior itself is unchanged

## Impact

- **Frontend components**: `DragContainer.svelte`, `TaskList.svelte`, `SubtaskTree.svelte`, `PinnedSection.svelte`, `ListSidebar.svelte`, `SectionList.svelte` — anywhere `dndzone` or `dragHandleZone` is used
- **Library**: svelte-dnd-action configuration — likely uses the `dragDisabled` prop toggled by touch state, or a custom touch event layer
- **No backend changes**: purely a frontend UX improvement
- **No dependency additions expected**: svelte-dnd-action already handles pointer events; this adds a gesture gate on top
