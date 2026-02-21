## 1. Backend API

- [x] 1.1 Create `UpcomingTaskSchema` in `tasks/api/schemas.py` with fields: `id`, `title`, `due_date`, `due_time`, `priority`, `is_pinned`, `list_id`, `list_name`, `list_emoji`, `section_id`, `section_name`, `tags` (list of strings)
- [x] 1.2 Create `tasks/api/upcoming.py` with `GET /upcoming/` endpoint: query `Task.objects.filter(is_completed=False, due_date__isnull=False)`, use `select_related("section__list")` and `prefetch_related("tags")`, order by `due_date`, `due_time` (nulls last), serialize with `UpcomingTaskSchema`
- [x] 1.3 Register the upcoming router in `tasks/api/__init__.py`

## 2. Backend Tests

- [x] 2.1 Create `tasks/tests/test_api_upcoming.py` with tests: returns tasks with due dates sorted chronologically, excludes completed tasks, excludes tasks without due dates, returns empty array when no matches, includes list/section context fields, null due_time sorts after non-null

## 3. Frontend Types and API Client

- [x] 3.1 Add `UpcomingTask` interface to `frontend/src/lib/api/types.ts` matching the API schema
- [x] 3.2 Add `api.upcoming.get()` method to `frontend/src/lib/api/index.ts` calling `GET /upcoming/`

## 4. Frontend Store

- [x] 4.1 Create `frontend/src/lib/stores/upcoming.ts` with a `loadUpcoming()` function and a writable store holding `UpcomingTask[]`

## 5. Frontend Dashboard Page

- [x] 5.1 Create `frontend/src/routes/upcoming/+page.svelte` that calls `loadUpcoming()` on mount, groups tasks into Overdue/Today/Tomorrow/This Week/Later buckets based on client local date, renders group headers and task rows
- [x] 5.2 Each task row displays: title, formatted due date/time, priority indicator (if non-zero), list emoji + name / section name
- [x] 5.3 Each task row links to `/?list={list_id}&task={task_id}` on click

## 6. Navigation

- [x] 6.1 Add `{ href: '/upcoming', label: 'Upcoming' }` to the `tabs` array in `frontend/src/routes/+layout.svelte`, positioned after "Tasks"

## 7. Deep Link Support

- [x] 7.1 Update `frontend/src/routes/+page.svelte` to read `list` and `task` query params on mount and auto-select the corresponding list and task

## 8. E2E Tests

- [x] 8.1 Add `e2e/test_upcoming.py` with tests: dashboard page loads, tasks grouped correctly, clicking a task navigates to its list, empty state shown when no upcoming tasks
