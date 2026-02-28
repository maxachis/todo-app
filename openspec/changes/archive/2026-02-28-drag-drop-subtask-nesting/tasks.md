## 1. Remove svelte-dnd-action from task containers

- [x] 1.1 Update `TaskList.svelte` — remove `DragContainer`/`DragItem` imports and wrappers around task items. Render `TaskRow` and `SubtaskTree` in a plain `{#each}` block. Remove `handleConsider`/`handleFinalize` functions and `sortableActiveTasks` state. Keep the active/completed task filtering and sorting logic. Files: `frontend/src/lib/components/tasks/TaskList.svelte`
- [x] 1.2 Update `SubtaskTree.svelte` — remove `DragContainer`/`DragItem` imports and wrappers around subtask items. Render subtasks in a plain `{#each}` block. Remove `handleConsider`/`handleFinalize` functions and `sortableSubtasks` state. Keep the completed subtask filtering, depth-based indentation, and collapse logic. Files: `frontend/src/lib/components/tasks/SubtaskTree.svelte`
- [x] 1.3 Verify `DragContainer` and `DragItem` components are still used elsewhere (section reordering, list reordering). Do NOT delete the component files — only remove their usage from task containers. Files: `frontend/src/lib/components/dnd/DragContainer.svelte`, `frontend/src/lib/components/dnd/DragItem.svelte`

## 2. Add frontend circular-nesting guard

- [x] 2.1 Add an `isDescendantOf(taskId: number, potentialAncestorId: number): boolean` utility function to `TaskRow.svelte` (or a shared helper). It should traverse the task tree from the store to check if `taskId` appears in the subtree rooted at `potentialAncestorId`. Files: `frontend/src/lib/components/tasks/TaskRow.svelte`
- [x] 2.2 In `handleDropOnTask`, when `midpointDropMode === 'nest'`, call `isDescendantOf(task.id, dragTaskId)` before making the API call. If true, clear `dropMode` and return early without calling `moveTask`. Files: `frontend/src/lib/components/tasks/TaskRow.svelte`

## 3. Improve drop visual indicators

- [x] 3.1 Update `TaskRow.svelte` CSS: enhance the `.drop-nest` style to include a subtle background tint (e.g., `background: var(--accent-light)`) in addition to the existing left accent bar, to differentiate nesting intent from selection state. Files: `frontend/src/lib/components/tasks/TaskRow.svelte`

## 4. Verify and test

- [ ] 4.1 Manual testing: verify that dragging a task above the midpoint of another task reorders it before the target at the same level (top-level, subtask, sub-subtask depths)
- [ ] 4.2 Manual testing: verify that dragging a task below the midpoint of another task nests it as a subtask of the target at any depth
- [ ] 4.3 Manual testing: verify that dragging a task onto its own descendant is silently prevented (no error, no state change)
- [ ] 4.4 Manual testing: verify that section reordering and list reordering (svelte-dnd-action) still work correctly
- [ ] 4.5 Manual testing: verify that the drag lock prevents concurrent drag operations
- [x] 4.6 Run `cd frontend && npm run check` to verify no TypeScript/lint errors after changes
- [x] 4.7 Run existing E2E tests: `uv run python -m pytest e2e -q` to verify no regressions (12/12 drag-drop + pinning tests pass; other failures are pre-existing)
