## Why

Some tasks recur on a predictable schedule — filing quarterly taxes, renewing subscriptions, monthly reviews — but currently each occurrence must be created manually. Adding recurrence support lets the user define a task once and have it automatically regenerate after completion, reducing the overhead of managing routine obligations.

## What Changes

- Add a recurrence rule model to define repeat schedules (specific dates of the year, weekly, monthly, etc.)
- Extend the Task model with a link to a recurrence rule and a flag indicating it is a recurring instance
- When a recurring task is completed, automatically generate the next occurrence with the appropriate future due date
- Add API endpoints to create, read, update, and delete recurrence rules on tasks
- Add frontend UI in the task detail panel for setting and viewing recurrence rules
- Display a visual indicator on recurring task rows in the task list

## Non-goals

- Calendar view or calendar integration — this change only affects the existing task list UI
- Alarm/notification system for upcoming recurring tasks
- Recurring subtask hierarchies — recurrence applies to individual tasks, not parent-child groups
- Time-of-day recurrence (e.g., "every day at 3pm") — recurrence operates on dates, not times
- Bulk editing of recurrence rules across multiple tasks

## Capabilities

### New Capabilities
- `task-recurrence`: Defines how tasks repeat — recurrence rule storage, supported schedule types (specific annual dates, weekly, monthly, daily), next-occurrence generation on completion, and API endpoints for managing recurrence on tasks

### Modified Capabilities
- `django-api`: Task CRUD and completion endpoints gain recurrence-related fields (recurrence rule data in task create/update, next-occurrence generation in the complete endpoint)
- `svelte-frontend`: Task detail panel adds a recurrence editor; task rows display a repeat indicator badge

## Impact

- **Model layer**: New `RecurrenceRule` model (or fields on `Task`); migration required
- **API**: `tasks/api/tasks.py` and `tasks/api/schemas.py` — extended request/response schemas for recurrence; completion endpoint gains next-occurrence creation logic
- **Frontend stores**: `frontend/src/lib/stores/` — task store needs to handle the new occurrence created on completion
- **Frontend components**: `TaskRow.svelte` gains a repeat indicator; task detail panel gains a recurrence editor section
- **Export/Import**: Recurrence metadata should be included in JSON export; CSV export can include a recurrence summary column
- **Tests**: New API tests for recurrence CRUD and completion-triggered generation; E2E tests for the recurrence UI
