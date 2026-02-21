## Context

The ToDo App currently supports one-off tasks with optional due dates. Users managing recurring obligations (quarterly tax filings, monthly reviews, weekly check-ins) must manually create each occurrence. The Task model has `due_date`, `is_completed`, and `completed_at` fields but no concept of recurrence. The app is single-user with a Django Ninja JSON API backend and SvelteKit frontend.

## Goals / Non-Goals

**Goals:**
- Allow users to attach a recurrence rule to any task
- Automatically create the next occurrence when a recurring task is completed
- Support common patterns: specific annual dates, weekly, monthly, and daily recurrence
- Keep the implementation simple — no full RFC 5545 (iCal) recurrence engine

**Non-Goals:**
- Calendar view or external calendar sync
- Notifications/reminders for upcoming recurrences
- Recurring subtask trees (recurrence applies to individual tasks only)
- Complex recurrence rules (e.g., "third Monday of every month", exclusion dates)
- Time-of-day recurrence — operates on dates only

## Decisions

### 1. Store recurrence as JSON fields on the Task model (not a separate model)

Store recurrence configuration directly on the Task model using two new fields:
- `recurrence_type`: CharField with choices (`none`, `daily`, `weekly`, `monthly`, `yearly`, `custom_dates`)
- `recurrence_rule`: JSONField storing type-specific parameters

**Rationale:** A separate `RecurrenceRule` model adds join complexity for a single-user app with no rule-sharing needs. JSON fields on Task keep queries simple and avoid an extra table. The recurrence data is small and always accessed alongside the task.

**Alternatives considered:**
- Separate `RecurrenceRule` model with FK from Task — adds complexity without benefit for single-user use
- Using python-dateutil rrule strings — powerful but over-engineered for the supported patterns

**`recurrence_rule` JSON structures by type:**
- `daily`: `{}` (no extra params needed)
- `weekly`: `{"days": [0, 2, 4]}` (0=Monday, 6=Sunday, ISO weekday)
- `monthly`: `{"day_of_month": 15}`
- `yearly`: `{"month": 3, "day": 15}`
- `custom_dates`: `{"dates": ["03-15", "06-15", "09-15", "12-15"]}` (MM-DD format, sorted)

### 2. Generate next occurrence on completion, not in advance

When a recurring task is completed, the backend creates a new task in the same section with the same title, notes, priority, tags, and recurrence rule, but with the next computed `due_date` and `is_completed=False`.

**Rationale:** Generating on completion is the simplest model — no background jobs, no scheduler, no concept of "future instances." The user always sees exactly one active instance of each recurring task. This matches how most lightweight task managers (Todoist, TickTick) handle basic recurrence.

**Alternatives considered:**
- Pre-generate N future instances — adds state management complexity, confusing if user edits one instance
- Background job/cron to create tasks — requires scheduler infrastructure not currently in the app

### 3. Next-occurrence date calculation

The next due date is computed relative to the **original due date** (not the completion date), finding the next occurrence that is strictly after today.

- `daily`: due_date + 1 day, repeated until > today
- `weekly`: next matching weekday after today
- `monthly`: same day-of-month in the next applicable month
- `yearly`: same month/day in the next applicable year
- `custom_dates`: next MM-DD from the list that falls after today (wraps to next year if needed)

**Rationale:** Computing from the original due date prevents schedule drift. If a user completes a monthly task late, the next occurrence still lands on the correct day of the month.

### 4. The completion endpoint creates the next occurrence and returns both tasks

The `POST /api/tasks/:id/complete/` endpoint gains new behavior for recurring tasks:
- Completes the current task as normal
- Creates the next occurrence task
- Returns the completed task with a `next_occurrence_id` field

The frontend uses `next_occurrence_id` to show a toast like "Next occurrence: Mar 15" and refreshes the list to show the new task.

### 5. Recurrence UI in the task detail panel

Add a "Repeat" section to `TaskDetail.svelte` below the due date field:
- A dropdown to select recurrence type (None, Daily, Weekly, Monthly, Yearly, Custom Dates)
- Type-specific inputs that appear based on selection (weekday checkboxes, day-of-month picker, month+day picker, or a multi-date list for custom dates)
- A small repeat icon/badge on `TaskRow.svelte` for tasks with active recurrence

### 6. Clearing recurrence

Setting `recurrence_type` to `none` via the task update endpoint removes the recurrence. The next completion will not generate a new occurrence. This is done through the same "Repeat" dropdown by selecting "None."

## Risks / Trade-offs

- **Monthly edge case (day 31 in short months)**: Tasks set to repeat on day 31 would need clamping to the last day of shorter months → Mitigation: clamp to min(day_of_month, last_day_of_month) during calculation
- **Custom dates list could grow large**: No hard limit on the dates list → Mitigation: cap at 52 entries (weekly equivalent) with frontend validation
- **Completed recurring task in "Completed" section while new one appears**: May briefly confuse the user → Mitigation: toast message explaining "Next: [date]" makes this clear
- **Export/import compatibility**: Recurrence fields need inclusion in JSON export → Mitigation: add `recurrence_type` and `recurrence_rule` to export schemas; CSV gets a summary column
- **No recurrence on subtasks**: Subtasks of a recurring task are not carried over to the next occurrence → Document this as expected behavior in the UI
