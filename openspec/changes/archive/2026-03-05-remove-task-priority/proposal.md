## Why

Task priority (None/Low/Medium/High) is never used in practice. It adds visual noise to the dashboard (priority badges) and unnecessary complexity to the task detail form. Removing it simplifies the UI and reduces code surface area.

## What Changes

- **BREAKING**: Remove the `priority` field from the Task model (Django migration)
- Remove priority dropdown from the task detail panel
- Remove priority badges from dashboard task rows
- Remove priority from API schemas (TaskSchema, UpdateTaskInput, UpcomingTaskSchema)
- Remove priority from the frontend UpcomingTask and Task types
- Remove priority from import/export (full backup, TickTick CSV)
- Remove priority-based sorting from dashboard pinned tasks group
- Update tests that reference priority

## Non-goals

- No replacement sorting/ranking mechanism
- No data migration concerns (priority values are simply dropped)

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `django-api`: Remove `priority` from TaskSchema, UpdateTaskInput, UpcomingTaskSchema, and task update endpoint
- `svelte-frontend`: Remove priority from Task type, task detail form, and dashboard badges
- `upcoming-dashboard`: Remove priority badges and priority-based sorting from dashboard
- `full-db-export`: Remove priority from export/import payloads
- `dashboard-task-completion`: Remove priority badge reference (already no functional dependency)

## Impact

- **Backend model**: `tasks/models.py` — remove field + migration
- **Backend API**: `tasks/api/schemas.py`, `tasks/api/tasks.py`, `tasks/api/lists.py`, `tasks/api/upcoming.py`
- **Backend services**: `tasks/services/ticktick_import.py`, `tasks/services/full_export.py`, `tasks/services/full_import.py`
- **Frontend types**: `frontend/src/lib/api/types.ts`
- **Frontend components**: `TaskDetail.svelte`, `dashboard/+page.svelte`
- **Tests**: `test_api_tasks.py`, `test_api_full_backup.py`
