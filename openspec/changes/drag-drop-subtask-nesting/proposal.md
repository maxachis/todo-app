## Why

Dragging a task onto another task should support two distinct outcomes based on cursor position: dropping above the midpoint places the task as a sibling before the target (same nesting level), while dropping below the midpoint nests it as a subtask of the target. The existing codebase has a `midpointDropMode` helper and native HTML5 drag handlers on `TaskRow`, but these coexist with svelte-dnd-action zones in `DragContainer`/`TaskList`/`SubtaskTree`, leading to event conflicts, inconsistent visual feedback, and unreliable nesting behavior—especially at deeper nesting levels and when dragging across sections.

## What Changes

- Unify the two competing drag-and-drop systems (svelte-dnd-action for reordering and native HTML5 DnD for nesting) into a single cohesive interaction so both reorder-before and nest-as-subtask work reliably from a single drag gesture.
- Refine midpoint hit detection so the "before" vs "nest" zones are visually distinct and behave predictably at every nesting depth—including making a task a sub-subtask by dropping below the midpoint of an existing subtask.
- Add clear visual indicators during drag: a horizontal line above the target for "before" mode; an indented highlight or left-accent bar for "nest" mode.
- Prevent circular nesting on the frontend (skip drop if the target is a descendant of the dragged task) in addition to the existing backend 409 guard.
- Ensure the drag lock mechanism (`taskDragLockedStore`) prevents race conditions across both interaction modes.

## Non-goals

- Drag-and-drop across lists (already handled separately via list move).
- Touch/mobile drag support.
- Changing the keyboard Tab indent/outdent behavior.
- Drag to reorder sections.

## Capabilities

### New Capabilities
- `drag-drop-subtask-nesting`: Midpoint-based drag-and-drop that supports both reordering (place before) and nesting (make subtask/sub-subtask) in a single unified interaction, with clear visual feedback for each mode.

### Modified Capabilities
- `svelte-frontend`: The task DnD interaction model changes from two parallel systems to a unified approach within TaskRow, TaskList, and SubtaskTree components.

## Impact

- **Frontend components**: `TaskRow.svelte`, `TaskList.svelte`, `SubtaskTree.svelte`, `DragContainer.svelte` — DnD event handling and visual feedback.
- **Frontend stores**: `tasks.ts` — drag lock and move helpers.
- **Backend**: No API changes needed; the existing `move_task` endpoint already supports `parent_id`, `section_id`, and `position` in a single call, with circular-nesting protection.
- **Dependencies**: svelte-dnd-action — may need configuration changes or selective disabling during cross-mode drags.
- **Tests**: E2E drag-and-drop tests should cover both reorder and nesting scenarios.
