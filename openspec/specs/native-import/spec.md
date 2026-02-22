### Requirement: Native JSON import service
The system SHALL provide a service function that accepts the app's own JSON export format and creates corresponding database records (lists, sections, tasks, subtasks, tags).

#### Scenario: Import single-list JSON export
- **WHEN** the service receives a JSON object with `name`, `sections` (each containing `tasks`)
- **THEN** it creates the list, its sections, and all tasks/subtasks with correct positions and parent relationships

#### Scenario: Import multi-list JSON export
- **WHEN** the service receives a JSON array of list objects
- **THEN** it creates all lists, sections, tasks, and subtasks preserving the full hierarchy

#### Scenario: JSON import preserves task fields
- **WHEN** a JSON import contains tasks with `title`, `notes`, `due_date`, `is_completed`, `completed_at`, `position`, and `tags`
- **THEN** all fields are stored on the created task records

#### Scenario: JSON import creates tags
- **WHEN** a JSON import contains tasks with tag names that do not yet exist in the database
- **THEN** the tags are created and associated with the tasks

#### Scenario: JSON import reconstructs subtask hierarchy
- **WHEN** a JSON import contains tasks with nested `subtasks` arrays
- **THEN** child tasks are created with correct `parent` references and positions

#### Scenario: JSON import duplicate detection by title
- **WHEN** a JSON import contains a task whose title already exists in the same list and section
- **THEN** the task is skipped and counted in `tasks_skipped`

#### Scenario: JSON import returns summary statistics
- **WHEN** a JSON import completes
- **THEN** the service returns a dict with `lists_created`, `sections_created`, `tasks_created`, `tasks_skipped`, `tags_created`, `parents_linked`, `errors`, and `error_details`

### Requirement: Native CSV import service
The system SHALL provide a service function that accepts the app's own CSV export format (columns: `list`, `section`, `task`, `parent_task`, `depth`, `notes`, `due_date`, `tags`, `is_completed`) and creates corresponding database records.

#### Scenario: Import native CSV with flat tasks
- **WHEN** the service receives a CSV file with rows containing `list`, `section`, `task` and `depth` of 0
- **THEN** it creates lists, sections, and top-level tasks

#### Scenario: Import native CSV with subtasks
- **WHEN** the service receives a CSV file with rows where `depth` > 0 and `parent_task` is set
- **THEN** it creates subtasks linked to the correct parent task within the same section

#### Scenario: Native CSV import parses tags
- **WHEN** a CSV row has a comma-separated `tags` value
- **THEN** each tag is created (if needed) and associated with the task

#### Scenario: Native CSV import parses due_date
- **WHEN** a CSV row has a `due_date` value in `YYYY-MM-DD` format
- **THEN** the task's `due_date` field is set accordingly

#### Scenario: Native CSV import parses is_completed
- **WHEN** a CSV row has `is_completed` set to `True`
- **THEN** the task's `is_completed` field is set to `True`

#### Scenario: Native CSV import duplicate detection by title
- **WHEN** a CSV row's `task` title already exists in the same list and section
- **THEN** the task is skipped and counted in `tasks_skipped`

#### Scenario: Native CSV import returns summary statistics
- **WHEN** a native CSV import completes
- **THEN** the service returns a dict with `lists_created`, `sections_created`, `tasks_created`, `tasks_skipped`, `tags_created`, `parents_linked`, `errors`, and `error_details`

### Requirement: Format auto-detection
The system SHALL auto-detect the import format based on file extension and content structure, without requiring the user to specify it.

#### Scenario: JSON file detected by extension
- **WHEN** the uploaded file has a `.json` extension
- **THEN** the system parses it as JSON and routes to the native JSON importer

#### Scenario: Native CSV detected by header columns
- **WHEN** the uploaded file has a `.csv` extension and the header row contains `list`, `section`, `task`
- **THEN** the system routes to the native CSV importer

#### Scenario: TickTick CSV detected by header columns
- **WHEN** the uploaded file has a `.csv` extension and the header row contains `taskId` and `Title`
- **THEN** the system routes to the existing TickTick CSV importer

#### Scenario: Unrecognized CSV format returns error
- **WHEN** the uploaded file has a `.csv` extension but the header matches neither native nor TickTick format
- **THEN** the system responds with status 400 and a descriptive error message
