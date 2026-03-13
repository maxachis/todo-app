## 1. Backend Model

- [x] 1.1 Remove `PRIORITY_NONE`, `PRIORITY_LOW`, `PRIORITY_MEDIUM`, `PRIORITY_HIGH`, `PRIORITY_CHOICES` constants and the `priority` field from `Task` model in `tasks/models.py`
- [x] 1.2 Remove `priority` from `Task.create_next_occurrence()` method in `tasks/models.py`
- [x] 1.3 Run `python manage.py makemigrations` to generate migration removing the `priority` column

## 2. Backend API

- [x] 2.1 Remove `priority` from `TaskSchema` in `tasks/api/schemas.py`
- [x] 2.2 Remove `priority` from `UpdateTaskInput` in `tasks/api/schemas.py`
- [x] 2.3 Remove `priority` from `UpcomingTaskSchema` in `tasks/api/schemas.py`
- [x] 2.4 Remove `priority` assignment from the task update handler in `tasks/api/tasks.py`
- [x] 2.5 Remove `priority` from task serialization in `tasks/api/lists.py`
- [x] 2.6 Remove `priority` from upcoming task dict in `tasks/api/upcoming.py`

## 3. Backend Services

- [x] 3.1 Remove `priority` from `tasks/services/full_export.py` export serialization
- [x] 3.2 Remove `priority` from `tasks/services/full_import.py` import deserialization (keep silently ignoring old exports)
- [x] 3.3 Remove `priority` parsing from `tasks/services/ticktick_import.py`

## 4. Frontend Types

- [x] 4.1 Remove `priority` from `Task` interface in `frontend/src/lib/api/types.ts`
- [x] 4.2 Remove `priority` from `UpcomingTask` interface in `frontend/src/lib/api/types.ts`
- [x] 4.3 Remove `priority` from `UpdateTaskInput` interface in `frontend/src/lib/api/types.ts`

## 5. Frontend Components

- [x] 5.1 Remove priority dropdown from `frontend/src/lib/components/tasks/TaskDetail.svelte`
- [x] 5.2 Remove `PRIORITY_LABELS`, `PRIORITY_CLASSES`, priority badges, and priority-based sorting from `frontend/src/routes/dashboard/+page.svelte`
- [x] 5.3 Remove priority badge CSS styles from `frontend/src/routes/dashboard/+page.svelte`

## 6. Tests

- [x] 6.1 Remove `priority` from test payloads/assertions in `tasks/tests/test_api_tasks.py`
- [x] 6.2 Remove `priority` from test fixtures/assertions in `tasks/tests/test_api_full_backup.py`

## 7. Verification

- [x] 7.1 Run `uv run python -m pytest tasks/tests/ -q` to verify backend tests pass
- [x] 7.2 Run `cd frontend && npm run check` to verify no type errors
- [x] 7.3 Run `uv run python manage.py migrate` to apply the migration
