## Why

Creating a task with a due date currently requires two steps: create the task (title only), then open the detail panel to set the date. This friction discourages setting due dates upfront, especially when quickly adding multiple tasks. Adding an inline date picker next to the "+" button lets users set a due date at creation time in a single step.

## What Changes

- Add a date input to the `TaskCreateForm` component, positioned next to the existing "+" submit button
- Extend the `TaskCreateInput` API schema to accept an optional `due_date` field
- Update the `create_task` API endpoint to persist `due_date` when provided
- Update the frontend `CreateTaskInput` type to include `due_date`
- The date field is optional — users can still create tasks without a date (current behavior preserved)

## Capabilities

### New Capabilities

- `inline-task-date`: Add an optional date picker to the task creation form, allowing users to set a due date at task creation time without opening the detail panel

### Modified Capabilities

_(none — the existing due date capability in the detail panel is unchanged)_

## Impact

- **Frontend**: `TaskCreateForm.svelte` gains a date input; `types.ts` `CreateTaskInput` interface adds optional `due_date`
- **Backend**: `TaskCreateInput` schema adds optional `due_date`; `create_task` endpoint passes it through to `Task.objects.create()`
- **No breaking changes**: The date field is optional with no default, preserving all existing behavior
- **No new dependencies**: Uses native HTML `<input type="date">`, consistent with the existing detail panel
