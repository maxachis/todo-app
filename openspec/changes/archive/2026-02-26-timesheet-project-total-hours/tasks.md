## 1. Backend API

- [x] 1.1 Add overall hours aggregation query to `get_timesheet` in `tasks/api/timesheet.py` — query all `TimeEntry` rows grouped by project to get all-time per-project counts, and a total count across all entries
- [x] 1.2 Merge overall hours into `per_project` array: add `overall_hours` field to each project entry, include projects with zero weekly hours but nonzero overall hours, sort by descending weekly hours then descending overall hours
- [x] 1.3 Add `overall_total_hours` field to the summary response object

## 2. Frontend Types

- [x] 2.1 Add `overall_hours` field to `TimesheetSummaryItem` in `frontend/src/lib/api/types.ts`
- [x] 2.2 Add `overall_total_hours` field to `TimesheetResponse.summary` in `frontend/src/lib/api/types.ts`

## 3. Frontend UI

- [x] 3.1 Update summary bar total display in `frontend/src/routes/timesheet/+page.svelte` to show "Total: Xh (Yh total)" format
- [x] 3.2 Update per-project display in the summary bar to show "ProjectName: Xh (Yh total)" format
- [x] 3.3 Ensure projects with 0 weekly hours but nonzero overall hours render correctly in the summary bar

## 4. Testing

- [x] 4.1 Add API test in `tasks/tests/test_api_projects.py` (or new test file) verifying `overall_total_hours` and `overall_hours` fields in timesheet summary response
- [x] 4.2 Add API test verifying projects with zero weekly hours but nonzero overall hours appear in `per_project`
