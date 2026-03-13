## MODIFIED Requirements

### Requirement: Task CRUD operations
The API SHALL support creating, reading, updating, and deleting tasks.

#### Scenario: Get task detail
- **WHEN** a client sends GET to `/api/tasks/:id/`
- **THEN** the server responds with the full task object including `title`, `notes`, `due_date`, `due_time`, `is_completed`, `completed_at`, `is_pinned`, `tags`, `parent`, `section`, nested `subtasks`, `recurrence_type`, and `recurrence_rule`

#### Scenario: Create a task
- **WHEN** a client sends POST to `/api/sections/:section_id/tasks/` with `{"title": "Buy milk"}`
- **THEN** the server creates the task in that section with default values

#### Scenario: Create a subtask
- **WHEN** a client sends POST to `/api/sections/:section_id/tasks/` with `{"title": "Buy milk", "parent_id": 5}`
- **THEN** the server creates the task as a child of task 5

#### Scenario: Update task fields
- **WHEN** a client sends PUT to `/api/tasks/:id/` with `{"title": "Updated", "notes": "# Heading", "due_date": "2026-03-15"}`
- **THEN** the server updates only the provided fields and responds with the full updated task object
