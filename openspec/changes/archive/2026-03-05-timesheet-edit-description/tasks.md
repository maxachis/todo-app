## 1. Backend: Add update endpoint

- [x] 1.1 Add `TimeEntryUpdateInput` schema to `tasks/api/schemas.py` with optional `description` field
- [x] 1.2 Add PUT `/timesheet/{entry_id}/` endpoint to `tasks/api/timesheet.py` that updates description and returns the entry

## 2. Frontend: API client and store

- [x] 2.1 Add `UpdateTimeEntryInput` interface to `frontend/src/lib/api/types.ts`
- [x] 2.2 Add `update` method to the timesheet API client in `frontend/src/lib/api/index.ts`
- [x] 2.3 Add `updateTimeEntry` function to `frontend/src/lib/stores/timesheet.ts`

## 3. Frontend: Inline editing UI

- [x] 3.1 Replace static description text in entry rows with a click-to-edit input that saves on blur
