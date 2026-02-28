## 1. Extract Completed Section from TaskList

- [x] 1.1 In `frontend/src/lib/components/tasks/TaskList.svelte`, remove the completed tasks rendering block (toggle button + completed task rows). Export `completedTasks` data or add a new prop/event so the parent can render completed tasks separately.
- [x] 1.2 Ensure TaskList only renders active (incomplete) tasks and the drag-drop container.

## 2. Render Completed Section After TaskCreateForm in SectionList

- [x] 2.1 In `frontend/src/lib/components/sections/SectionList.svelte`, add completed tasks rendering after `TaskCreateForm` for each section. Reuse the same collapsible toggle pattern and completed task row styling.
- [x] 2.2 Verify the completed section retains its border-top separator, collapse/expand toggle, and task count display.

## 3. Verify

- [x] 3.1 Confirm the visual order is: Active Tasks → Create Form → Completed for each section.
- [x] 3.2 Test that collapsing/expanding completed tasks still works correctly in the new position.
- [x] 3.3 Run `cd frontend && npm run check` to verify no type errors.
