### Requirement: Full database export endpoint
The system SHALL expose a GET endpoint at `/api/export/full/` that returns a JSON file containing all records from every model in both the `tasks` and `network` Django apps.

#### Scenario: Export returns valid JSON with envelope
- **WHEN** a GET request is made to `/api/export/full/`
- **THEN** the response content-type is `application/json` and the body is a JSON object containing `"format": "nexus-full-backup"`, `"version": 1`, and an `"exported_at"` ISO-8601 timestamp

#### Scenario: Export includes all entity collections
- **WHEN** a GET request is made to `/api/export/full/`
- **THEN** the JSON object SHALL contain keys for every entity type: `tags`, `org_types`, `interaction_types`, `projects`, `project_links`, `people`, `organizations`, `lists`, `sections`, `tasks`, `time_entries`, `interactions`, `leads`, `lead_tasks`, `relationships_person_person`, `relationships_organization_person`, `task_persons`, `task_organizations`, `interaction_tasks`

#### Scenario: Export serves as file download
- **WHEN** a GET request is made to `/api/export/full/`
- **THEN** the response SHALL include a `Content-Disposition: attachment` header with filename `nexus-backup.json`

### Requirement: Entity serialization preserves all fields
The system SHALL serialize each entity with its database `id` and all model fields, so that foreign-key references between collections resolve correctly.

#### Scenario: Task serialization includes all fields
- **WHEN** a task exists with title, notes, due_date, due_time, priority, is_completed, completed_at, created_at, position, external_id, is_pinned, recurrence_type, recurrence_rule, section FK, and parent FK
- **THEN** the exported task object SHALL include all of those fields, with `section_id`, `parent_id`, and a `tag_ids` array

#### Scenario: Person serialization includes all fields
- **WHEN** a person exists with first_name, middle_name, last_name, email, linkedin_url, notes, follow_up_cadence_days, created_at, updated_at
- **THEN** the exported person object SHALL include all of those fields and the database `id`

#### Scenario: M2M relationships are serialized as ID arrays
- **WHEN** a time entry has linked tasks via M2M
- **THEN** the exported time entry object SHALL include a `task_ids` array containing the database IDs of linked tasks

### Requirement: Empty collections are included
The system SHALL include entity collection keys even when no records exist for that type, using empty arrays.

#### Scenario: No people exist
- **WHEN** the database has no Person records
- **THEN** the export JSON SHALL contain `"people": []`
