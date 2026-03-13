## MODIFIED Requirements

### Requirement: Full backup serializes all entities
The system SHALL serialize each entity with its database `id` and all model fields, so that foreign-key references between collections resolve correctly.

#### Scenario: Task serialization includes all fields
- **WHEN** a task exists with title, notes, due_date, due_time, is_completed, completed_at, created_at, position, external_id, is_pinned, recurrence_type, recurrence_rule, section FK, and parent FK
- **THEN** the export JSON includes all of these fields for the task
