## 1. Backend: Position next occurrence in-place

- [x] 1.1 In `tasks/models.py` `Task.complete()`, change `position=max_pos + 10` to `position=self.position` so the next occurrence inherits the completed task's position

## 2. Backend: Return full next occurrence in complete response

- [x] 2.1 In `tasks/api/tasks.py` `complete_task()`, serialize the next occurrence task (if created) and attach it as `next_occurrence` on the response alongside the existing `next_occurrence_id`
- [x] 2.2 In `tasks/api/schemas.py`, add `next_occurrence: TaskSchema | None = None` field to `TaskSchema` (or confirm it can be set dynamically)
- [x] 2.3 In `frontend/src/lib/api/types.ts`, add `next_occurrence: Task | null` to the `Task` interface

## 3. Frontend: Optimistic store update on completion

- [x] 3.1 In `frontend/src/lib/stores/tasks.ts` `completeTask()`, replace `await refreshListDetail()` with targeted store mutations: call `replaceTaskInList()` to update the completed task in-place, then if `next_occurrence` exists call `addTaskToSection()` to insert it
- [x] 3.2 Verify the "Next: {date}" info toast still works using `updated.next_occurrence` data directly (no separate `api.tasks.get()` call needed)

## 4. Frontend: Fix undo for recurring tasks

- [x] 4.1 In `frontend/src/lib/components/tasks/TaskRow.svelte` `handleCheck()`, capture `next_occurrence_id` from the completion result and pass it into the undo closure
- [x] 4.2 In `frontend/src/lib/stores/tasks.ts`, update `uncompleteTask()` to accept an optional `deleteNextOccurrenceId` parameter; if provided, call `api.tasks.remove(deleteNextOccurrenceId)` and `removeTaskFromList()` before un-completing the original
- [x] 4.3 Update the undo toast `onAction` in `TaskRow.svelte` to call `uncompleteTask(task.id, result.next_occurrence_id)` when the completed task was recurring

## 5. Testing

- [x] 5.1 Add/update backend API test in `tasks/tests/test_api_tasks.py`: completing a recurring task returns `next_occurrence` with full task data and correct position (same as original)
- [x] 5.2 Add backend API test: completing a non-recurring task returns `next_occurrence: null`
- [x] 5.3 Add backend API test: the next occurrence's position matches the completed task's position
