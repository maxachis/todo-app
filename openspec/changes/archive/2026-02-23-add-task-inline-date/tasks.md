## 1. Backend API

- [x] 1.1 Add optional `due_date: date | None = None` field to `TaskCreateInput` schema in `tasks/api/schemas.py`
- [x] 1.2 Update `create_task` endpoint in `tasks/api/tasks.py` to pass `due_date` through to `Task.objects.create()` when provided
- [x] 1.3 Add API test cases for creating a task with and without `due_date` in `tasks/tests/test_api_tasks.py`

## 2. Frontend Types & API Client

- [x] 2.1 Add optional `due_date?: string | null` to `CreateTaskInput` interface in `frontend/src/lib/api/types.ts`

## 3. Frontend UI

- [x] 3.1 Add date input (`<input type="date">`) to `TaskCreateForm.svelte` between the title input and submit button
- [x] 3.2 Bind date value to a `dueDate` variable and include it in the `createTask` payload when set
- [x] 3.3 Clear the date input on form submission (alongside existing title reset)
- [x] 3.4 Style the date input to be compact and visually secondary (constrained width, flex layout so title input takes remaining space)
- [x] 3.5 Ensure the form layout works on mobile viewports without overflow or wrapping issues
