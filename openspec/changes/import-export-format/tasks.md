## 1. Native JSON Import Service

- [x] 1.1 Create `tasks/services/native_import.py` with `import_native_json(file)` function that parses a JSON file (single list object or array of list objects) and creates lists, sections, tasks, subtasks, and tags. Returns the standard stats dict (`lists_created`, `sections_created`, `tasks_created`, `tasks_skipped`, `tags_created`, `parents_linked`, `errors`, `error_details`).
- [x] 1.2 Implement title-based duplicate detection within (list, section) scope — skip tasks whose title already exists in the same list and section.
- [x] 1.3 Implement recursive subtask creation from nested `subtasks` arrays, setting correct `parent` references and positions.

## 2. Native CSV Import Service

- [x] 2.1 Add `import_native_csv(file)` function to `tasks/services/native_import.py` that parses a CSV with columns `list`, `section`, `task`, `parent_task`, `depth`, `notes`, `due_date`, `tags`, `is_completed`. Creates lists, sections, and tasks. Returns the standard stats dict.
- [x] 2.2 Implement parent-child linking using `parent_task` column and `depth` — within a section, match parent by title at `depth - 1`.
- [x] 2.3 Parse comma-separated `tags` column and create/link Tag records.
- [x] 2.4 Parse `due_date` (YYYY-MM-DD format) and `is_completed` (True/False) fields.

## 3. API Format Detection and Routing

- [x] 3.1 Update `tasks/api/import_tasks.py` to accept `.json` files in addition to `.csv`. Route `.json` files to `import_native_json`.
- [x] 3.2 For `.csv` files, read the header row and detect format: if header contains `taskId` and `Title`, route to `import_ticktick_csv`; if header contains `list`, `section`, `task`, route to `import_native_csv`; otherwise return 400 with descriptive error.
- [x] 3.3 Wrap all import paths in `transaction.atomic()` to ensure consistency.

## 4. Frontend Import Page Update

- [x] 4.1 Update `frontend/src/routes/import/+page.svelte`: change file input `accept` from `.csv` to `.csv,.json`. Update description text to list all supported formats (app JSON export, app CSV export, TickTick CSV).
- [x] 4.2 Update `frontend/src/lib/api/index.ts`: change the import upload method to send the file with a generic field name (or keep `csv_file` and also accept it for JSON — verify backend handles both).

## 5. Backend Tests

- [x] 5.1 Add tests in `tasks/tests/test_api_import_native.py` for native JSON import: single-list, multi-list, subtask hierarchy, tags, duplicate detection, summary stats.
- [x] 5.2 Add tests for native CSV import: flat tasks, subtasks via depth/parent_task, tags, due_date, is_completed, duplicate detection, summary stats.
- [x] 5.3 Add tests for format auto-detection: `.json` routes to native JSON importer, `.csv` with native header routes to native CSV, `.csv` with TickTick header routes to TickTick, unrecognized CSV returns 400.
- [x] 5.4 Verify existing TickTick import tests still pass (no regressions).
