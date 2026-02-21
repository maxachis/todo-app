## 1. Database Model & Migration

- [x] 1.1 Add `recurrence_type` CharField (choices: none/daily/weekly/monthly/yearly/custom_dates, default "none") and `recurrence_rule` JSONField (default={}) to the Task model in `tasks/models.py`
- [x] 1.2 Create and run the migration (`python manage.py makemigrations && python manage.py migrate`)

## 2. Recurrence Logic

- [x] 2.1 Create `tasks/services/recurrence.py` with `compute_next_due_date(recurrence_type, recurrence_rule, current_due_date)` function implementing all recurrence types (daily, weekly, monthly with day clamping, yearly, custom_dates with year wrapping)
- [x] 2.2 Create `tasks/services/recurrence.py` validation function `validate_recurrence_rule(recurrence_type, recurrence_rule)` that raises on invalid input (bad weekdays, day_of_month > 31, wrong date format, empty days list, >52 custom dates)
- [x] 2.3 Update `Task.complete()` in `tasks/models.py` to create the next occurrence task (copy title, notes, priority, tags, section, recurrence fields; set new due_date) when `recurrence_type != "none"`, returning the new task ID

## 3. API Schema Changes

- [x] 3.1 Add `recurrence_type: str` (default "none") and `recurrence_rule: dict` (default {}) to `TaskSchema` in `tasks/api/schemas.py`
- [x] 3.2 Add `next_occurrence_id: int | None` (default None) to `TaskSchema`
- [x] 3.3 Add `recurrence_type: str | None` and `recurrence_rule: dict | None` to `TaskUpdateInput`

## 4. API Endpoint Changes

- [x] 4.1 Update `update_task` in `tasks/api/tasks.py` to handle `recurrence_type` and `recurrence_rule` fields, calling the validation function before saving
- [x] 4.2 Update `complete_task` in `tasks/api/tasks.py` to call the recurrence-aware `Task.complete()` and include `next_occurrence_id` in the response
- [x] 4.3 Update `_serialize_task` in `tasks/api/lists.py` to include `recurrence_type`, `recurrence_rule`, and `next_occurrence_id` fields

## 5. Frontend TypeScript Types

- [x] 5.1 Add `recurrence_type: string`, `recurrence_rule: Record<string, unknown>`, and `next_occurrence_id: number | null` to the `Task` interface in `frontend/src/lib/api/types.ts`
- [x] 5.2 Add optional `recurrence_type?: string` and `recurrence_rule?: Record<string, unknown>` to `UpdateTaskInput` in `frontend/src/lib/api/types.ts`

## 6. Frontend Task Store

- [x] 6.1 Update `completeTask` in `frontend/src/lib/stores/tasks.ts` to handle the `next_occurrence_id` in the response and show a toast with the next occurrence's due date

## 7. Frontend Recurrence Editor

- [x] 7.1 Create `frontend/src/lib/components/tasks/RecurrenceEditor.svelte` with a dropdown for recurrence type selection (None/Daily/Weekly/Monthly/Yearly/Custom Dates) and type-specific inputs (weekday toggles, day-of-month number input, month+day selectors, MM-DD date list editor)
- [x] 7.2 Integrate `RecurrenceEditor` into `TaskDetail.svelte` below the due date field, wiring auto-save on blur to `updateTask`

## 8. Frontend Task Row Indicator

- [x] 8.1 Add a repeat icon (circular arrows SVG) to `TaskRow.svelte` that displays when `recurrence_type !== "none"`, positioned near the due date badge

## 9. Export/Import Updates

- [x] 9.1 Add `recurrence_type` and `recurrence_rule` fields to the JSON export in `tasks/api/export.py`
- [x] 9.2 Add a `recurrence` summary column to the CSV export in `tasks/api/export.py`

## 10. Backend Tests

- [x] 10.1 Add tests for `compute_next_due_date` covering all recurrence types, edge cases (month clamping, year wrapping, late completion) in `tasks/tests/test_recurrence.py`
- [x] 10.2 Add tests for `validate_recurrence_rule` covering valid and invalid inputs in `tasks/tests/test_recurrence.py`
- [x] 10.3 Add API tests for task update with recurrence fields (set, clear, validation errors) in `tasks/tests/test_api_tasks.py`
- [x] 10.4 Add API tests for completing a recurring task (next occurrence creation, response includes next_occurrence_id) in `tasks/tests/test_api_tasks.py`

## 11. E2E Tests

- [x] 11.1 Add E2E test: set recurrence on a task via the detail panel, verify the repeat icon appears on the task row
- [x] 11.2 Add E2E test: complete a recurring task, verify the next occurrence appears in the section with the correct due date
