## Why

Timesheet entries currently can only be created and deleted — there's no way to update the description after creation. If a user makes a typo or wants to add detail later, they must delete and re-create the entry. Adding inline edit for the description field fixes this.

## What Changes

- Add a PUT endpoint for updating timesheet entry description
- Add `UpdateTimeEntryInput` schema
- Add frontend API client method and store function for updating entries
- Make the description text in entry rows editable inline (click to edit, save on blur)

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `timesheet-summary`: Add update endpoint and inline description editing in entry rows

## Impact

- Backend: `tasks/api/schemas.py` — add `TimeEntryUpdateInput`
- Backend: `tasks/api/timesheet.py` — add PUT endpoint
- Frontend: `frontend/src/lib/api/types.ts` — add `UpdateTimeEntryInput` interface
- Frontend: `frontend/src/lib/api/index.ts` — add `update` method to timesheet API
- Frontend: `frontend/src/lib/stores/timesheet.ts` — add `updateTimeEntry` function
- Frontend: `frontend/src/routes/timesheet/+page.svelte` — make description editable inline

## Non-goals

- Editing other entry fields (project, date, tasks) inline
- Undo/redo support
