## 1. Store Update

- [x] 1.1 Add `removeUpcomingTask(taskId: number)` function to `frontend/src/lib/stores/upcoming.ts` that filters the given task ID out of the store

## 2. Dashboard UI

- [x] 2.1 Add checkbox markup to each task row in `frontend/src/routes/dashboard/+page.svelte` (inside `.task-main`, before the task title)
- [x] 2.2 Add `handleComplete(task)` function that calls `completeTask(taskId)`, optimistically removes the task via `removeUpcomingTask`, and shows undo toast for recurring tasks (calling `uncompleteTask` + `loadUpcoming` on undo)
- [x] 2.3 Wire checkbox click with `event.preventDefault()` and `event.stopPropagation()` to prevent navigation
- [x] 2.4 Add checkbox styles (`.dashboard-checkbox`, `.checkbox-custom`) matching existing TaskRow checkbox appearance

## 3. Verification

- [ ] 3.1 Manual test: complete a non-recurring task from dashboard — verify it disappears and stays completed in Tasks view
- [ ] 3.2 Manual test: complete a recurring task from dashboard — verify undo toast appears and undo restores the task
- [x] 3.3 Run `cd frontend && npm run check` to verify no type errors
