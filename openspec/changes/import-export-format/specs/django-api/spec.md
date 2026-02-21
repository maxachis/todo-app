## MODIFIED Requirements

### Requirement: Import endpoint
The system SHALL provide an endpoint to import tasks from TickTick CSV files, the app's native JSON export format, and the app's native CSV export format. The endpoint SHALL auto-detect the format based on file extension and CSV header structure.

#### Scenario: Successful TickTick CSV import
- **WHEN** a client sends POST to `/api/import/` with a CSV file whose header contains `taskId` and `Title`
- **THEN** the server routes to the TickTick importer, creates lists, sections, tasks, and tags as needed, and responds with a summary JSON including counts of created/skipped entities

#### Scenario: Successful native JSON import
- **WHEN** a client sends POST to `/api/import/` with a `.json` file containing the app's export format
- **THEN** the server routes to the native JSON importer, creates lists, sections, tasks, subtasks, and tags, and responds with a summary JSON including counts of created/skipped entities

#### Scenario: Successful native CSV import
- **WHEN** a client sends POST to `/api/import/` with a `.csv` file whose header contains `list`, `section`, `task`
- **THEN** the server routes to the native CSV importer, creates lists, sections, tasks, subtasks, and tags, and responds with a summary JSON including counts of created/skipped entities

#### Scenario: Duplicate detection for TickTick import
- **WHEN** a client re-imports a CSV containing tasks with `external_id` values that already exist
- **THEN** the server skips those tasks and reports them as skipped in the summary

#### Scenario: Duplicate detection for native import
- **WHEN** a client re-imports a native JSON or CSV file containing tasks whose titles already exist in the same list and section
- **THEN** the server skips those tasks and reports them as skipped in the summary

#### Scenario: Unsupported file type
- **WHEN** a client sends POST to `/api/import/` with a file that is not `.csv` or `.json`
- **THEN** the server responds with status 400

#### Scenario: Unrecognized CSV format
- **WHEN** a client sends POST to `/api/import/` with a `.csv` file whose header matches neither native nor TickTick format
- **THEN** the server responds with status 400 and a descriptive error message
