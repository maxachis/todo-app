## 1. Fix the $effect in TaskDetail

- [x] 1.1 Add a `prevTaskId` state variable to track the currently-loaded task ID (`frontend/src/lib/components/tasks/TaskDetail.svelte`)
- [x] 1.2 Change the `$effect` to compare `task.id` against `prevTaskId` and only reset local form values + call side-effect functions when the ID differs; update `prevTaskId` after resetting (`frontend/src/lib/components/tasks/TaskDetail.svelte`)

## 2. Fix backend: allow clearing due_date via API

- [x] 2.1 In `update_task`, use `model_fields_set` to distinguish "field not sent" from "field set to null" for `due_date` and `due_time` (`tasks/api/tasks.py`)

## 3. Verify

- [x] 3.1 Run backend API tests — 18 passed, 1 pre-existing failure (unrelated priority attribute)
- [ ] 3.2 Manual verification: set a due date on a task, then clear it, confirm it stays cleared after reload
