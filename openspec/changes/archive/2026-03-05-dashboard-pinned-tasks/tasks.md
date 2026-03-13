## 1. Backend API

- [x] 1.1 Update `tasks/api/upcoming.py` query to include pinned tasks without due dates using `Q(due_date__isnull=False) | Q(is_pinned=True)` filter, with pinned-no-date tasks sorted after dated tasks
- [x] 1.2 Update `tasks/api/schemas.py` `UpcomingTaskSchema` to make `due_date` optional (`str | None`)

## 2. Frontend Types

- [x] 2.1 Update `frontend/src/lib/api/types.ts` `UpcomingTask.due_date` from `string` to `string | null`

## 3. Dashboard Frontend

- [x] 3.1 Add "Pinned" group to `frontend/src/routes/dashboard/+page.svelte` grouping logic — extract pinned tasks into a separate bucket, rendered above time-horizon groups but below Follow-ups Due
- [x] 3.2 Handle `null` due dates in `groupTasks()` — route tasks with `due_date === null` to the Pinned group only (skip time-horizon bucketing)
- [x] 3.3 Sort Pinned group by priority descending, then tasks with due dates before those without, then title alphabetically
- [x] 3.4 Add pin icon indicator on pinned task rows in time-horizon groups

## 4. Testing

- [x] 4.1 Add API test in `tasks/tests/test_api_misc.py` verifying pinned tasks without due dates are returned by `GET /api/upcoming/`
- [x] 4.2 Add API test verifying completed pinned tasks are excluded from `GET /api/upcoming/`
- [x] 4.3 Run `cd frontend && npm run check` to verify TypeScript types are consistent
