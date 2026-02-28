## Why

The completed tasks section currently sits between active tasks and the task creation form, pushing the input further down as completed tasks accumulate. Moving completed tasks below the entry form keeps the creation input closer to active work, improving the task creation workflow.

## What Changes

- Reorder elements within each section so the task creation form appears directly after active tasks, with the completed tasks collapsible section moved below it.
- Visual order changes from: Active Tasks → Completed → Create Form to: Active Tasks → Create Form → Completed.

## Non-goals

- No changes to completed task display styling, collapse behavior, or functionality.
- No changes to the task creation form itself.
- No changes to drag-and-drop behavior.

## Capabilities

### New Capabilities

_None_

### Modified Capabilities

- `svelte-frontend`: Layout ordering of completed tasks section relative to task create form within sections.

## Impact

- `frontend/src/lib/components/tasks/TaskList.svelte` — completed section rendering moves out or is restructured.
- `frontend/src/lib/components/sections/SectionList.svelte` — ordering of TaskList and TaskCreateForm may change, or completed section rendered separately after the form.
