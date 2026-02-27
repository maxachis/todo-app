## ADDED Requirements

### Requirement: Auto-detect full database JSON format
The system SHALL detect the full-database export format by checking for `"format": "nexus-full-backup"` in the top-level JSON object when a `.json` file is uploaded to `/api/import/`. If detected, the system SHALL route to the full-database import logic instead of the existing per-list import.

#### Scenario: Full-backup JSON is detected and routed
- **WHEN** a `.json` file containing `"format": "nexus-full-backup"` is uploaded to `/api/import/`
- **THEN** the system SHALL invoke the full-database import service

#### Scenario: Regular list JSON falls through
- **WHEN** a `.json` file without `"format": "nexus-full-backup"` is uploaded to `/api/import/`
- **THEN** the system SHALL use the existing `import_native_json` logic

### Requirement: Import all entity types in dependency order
The system SHALL create records in foreign-key dependency order, maintaining an old-ID-to-new-ID mapping per entity type so that FK references from the export file resolve to newly created records.

#### Scenario: Import creates entities in correct order
- **WHEN** a full-backup JSON is imported
- **THEN** independent entities (tags, org_types, interaction_types, projects, people) SHALL be created before dependent entities (organizations, lists, sections, tasks, interactions, leads) and join tables (task_persons, interaction_tasks, lead_tasks, relationships) SHALL be created last

#### Scenario: Foreign keys resolve via ID mapping
- **WHEN** a task in the export has `section_id: 5` and the imported section with old ID 5 received new ID 12
- **THEN** the imported task SHALL be created with `section_id: 12`

### Requirement: Task tree reconstruction
The system SHALL import tasks with correct parent-child relationships by processing root tasks (parent_id null) before child tasks, using the old-to-new ID mapping for parent_id resolution.

#### Scenario: Subtask parent is linked correctly
- **WHEN** a task in the export has `parent_id: 10` and the imported task with old ID 10 received new ID 25
- **THEN** the imported subtask SHALL be created with `parent_id: 25`

#### Scenario: Root tasks are created before children
- **WHEN** the export contains tasks at multiple nesting depths
- **THEN** tasks with `parent_id: null` SHALL be created first, then depth-1 tasks, and so on

### Requirement: Duplicate detection per entity type
The system SHALL detect duplicates using each entity type's natural key and skip creation for duplicates, reusing the existing record's ID in the mapping.

#### Scenario: Duplicate tag is skipped
- **WHEN** a tag with name "urgent" already exists in the database
- **THEN** the import SHALL skip creating it, map the old ID to the existing record's ID, and increment `tags_skipped` in the stats

#### Scenario: Duplicate person is skipped
- **WHEN** a person with the same first_name and last_name already exists
- **THEN** the import SHALL skip creating it and reuse the existing record's ID

### Requirement: Atomic import with rollback
The system SHALL wrap the entire full-database import in a database transaction. If any error occurs, all changes SHALL be rolled back.

#### Scenario: Error during import rolls back all changes
- **WHEN** an error occurs while importing interactions (after tasks and people were already created)
- **THEN** all previously created records in the transaction SHALL be rolled back and no partial data remains

### Requirement: Import returns statistics
The system SHALL return a statistics object summarizing what was created, skipped, and any errors encountered, with counts per entity type.

#### Scenario: Successful import returns counts
- **WHEN** a full-backup JSON is imported successfully
- **THEN** the response SHALL include counts such as `tasks_created`, `tasks_skipped`, `people_created`, `people_skipped`, `organizations_created`, etc., plus an `errors` count and `error_details` array
