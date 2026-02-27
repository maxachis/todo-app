## 1. Store Layer

- [x] 1.1 Add `refreshTask(taskId: number)` function to `frontend/src/lib/stores/tasks.ts` that fetches the task via `api.tasks.get()`, calls `replaceTaskInList()` to update `listsStore`, and updates `selectedTaskDetail`

## 2. Component Update

- [x] 2.1 Update `addTag()` in `frontend/src/lib/components/tasks/TaskDetail.svelte` to call `refreshTask()` instead of `selectTask()`
- [x] 2.2 Update `removeTag()` in `frontend/src/lib/components/tasks/TaskDetail.svelte` to call `refreshTask()` instead of `selectTask()`

## 3. Verification

- [x] 3.1 Manually verify: add a tag in the detail panel and confirm the tag badge appears immediately in the center-panel task row
- [x] 3.2 Manually verify: remove a tag in the detail panel and confirm the tag badge disappears immediately from the center-panel task row
- [x] 3.3 Run `cd frontend && npm run check` to confirm no TypeScript errors
