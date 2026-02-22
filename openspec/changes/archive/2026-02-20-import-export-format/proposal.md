## Why

The import page currently only supports TickTick CSV files, which is a third-party format with specific column names (`taskId`, `parentId`, `List Name`, `Column Name`, etc.) and a metadata preamble. The app's own "Export All" button produces JSON, CSV, and Markdown files in the app's native format — but there is no way to re-import these files. A user who exports their data cannot restore it into a fresh instance or merge it back. Supporting import of the app's own export formats closes this round-trip gap.

## What Changes

- Add a new backend import service that parses the app's native JSON export format (nested lists > sections > tasks > subtasks) and creates the corresponding database records.
- Add a new backend import service that parses the app's native CSV export format (flat rows with `list`, `section`, `task`, `parent_task`, `depth`, `notes`, `due_date`, `tags`, `is_completed` columns) and creates the corresponding database records.
- Extend the `/api/import/` endpoint to accept `.json` and `.csv` files in the app's native format, in addition to the existing TickTick CSV support. The endpoint will auto-detect the format based on file extension and content structure.
- Update the frontend import page to accept `.json` files in addition to `.csv`, and update the UI copy to reflect that both app-native and TickTick formats are supported.

## Non-goals

- Importing Markdown (`.md`) export files. The markdown format is lossy (no structured metadata for tags, due dates in a parseable form, etc.) and is intended for human reading, not round-tripping.
- Changing the existing export format or structure.
- Adding import for any other third-party formats beyond TickTick.

## Capabilities

### New Capabilities

- `native-import`: Backend service and API support for importing the app's own JSON and CSV export formats, including list/section/task/subtask creation and duplicate handling.

### Modified Capabilities

- `django-api`: The import endpoint requirement expands from TickTick CSV only to also accept the app's native JSON and CSV export formats, with auto-detection.
- `svelte-frontend`: The import page UI expands to accept `.json` files and updates copy to describe supported formats.

## Impact

- **Backend**: New import service module(s) in `tasks/services/`. Modified `tasks/api/import_tasks.py` to route by detected format. Existing TickTick import path is unchanged.
- **Frontend**: Modified `frontend/src/routes/import/+page.svelte` (file accept attribute, UI text). Possibly updated API types if the import summary shape changes.
- **API**: The `POST /api/import/` endpoint accepts additional file types. Response shape (ImportSummary) remains the same.
- **Tests**: New API tests for native JSON/CSV import. Existing TickTick import tests remain unchanged.
