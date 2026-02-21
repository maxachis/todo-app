## MODIFIED Requirements

### Requirement: Task CRUD endpoints
The system SHALL provide endpoints for task creation, reading, updating, and deletion.

#### Scenario: Create a task in a section
- **WHEN** a client sends POST to `/api/sections/:section_id/tasks/` with `{"title": "Buy groceries"}`
- **THEN** the server creates the task in the section and responds with status 201 and the serialized task

#### Scenario: Create a subtask
- **WHEN** a client sends POST to `/api/sections/:section_id/tasks/` with `{"title": "Buy milk", "parent_id": 5}`
- **THEN** the server creates the task as a child of task 5

#### Scenario: Get task detail
- **WHEN** a client sends GET to `/api/tasks/:id/`
- **THEN** the server responds with the full task object including `title`, `notes`, `priority`, `due_date`, `due_time`, `is_completed`, `completed_at`, `is_pinned`, `tags`, `parent`, `section`, nested `subtasks`, `recurrence_type`, and `recurrence_rule`

#### Scenario: Update task fields
- **WHEN** a client sends PUT to `/api/tasks/:id/` with `{"title": "Updated", "notes": "# Heading", "due_date": "2026-03-15", "priority": 3}`
- **THEN** the server updates the specified fields and responds with the updated task

#### Scenario: Update task recurrence
- **WHEN** a client sends PUT to `/api/tasks/:id/` with `{"recurrence_type": "weekly", "recurrence_rule": {"days": [0, 2, 4]}}`
- **THEN** the server updates the task's recurrence fields and responds with the updated task including the new recurrence settings

#### Scenario: Clear task recurrence
- **WHEN** a client sends PUT to `/api/tasks/:id/` with `{"recurrence_type": "none"}`
- **THEN** the server sets `recurrence_type` to `none` and `recurrence_rule` to `{}`, and responds with the updated task

#### Scenario: Delete a task
- **WHEN** a client sends DELETE to `/api/tasks/:id/`
- **THEN** the server deletes the task and all its subtasks, responding with status 204

### Requirement: Task completion endpoints
The system SHALL provide endpoints to complete and uncomplete tasks, with completion cascading to subtasks. Completing a recurring task SHALL generate the next occurrence.

#### Scenario: Complete a task with subtasks
- **WHEN** a client sends POST to `/api/tasks/:id/complete/`
- **THEN** the server sets `is_completed=True` and `completed_at` on the task and all its non-completed subtasks recursively, and responds with the updated task including updated subtask states

#### Scenario: Complete a recurring task generates next occurrence
- **WHEN** a client sends POST to `/api/tasks/:id/complete/` for a task with `recurrence_type` other than `none`
- **THEN** the server completes the task, creates a new task in the same section with the next due date and same recurrence rule, and responds with the completed task including a `next_occurrence_id` field pointing to the new task

#### Scenario: Uncomplete a task
- **WHEN** a client sends POST to `/api/tasks/:id/uncomplete/`
- **THEN** the server sets `is_completed=False` and clears `completed_at` on the task only (not subtasks), and responds with the updated task

## ADDED Requirements

### Requirement: Recurrence fields in task serialization
The system SHALL include `recurrence_type` and `recurrence_rule` in all task response schemas. The `TaskSchema` SHALL include a `next_occurrence_id` field (nullable) that is populated only when a recurring task is completed.

#### Scenario: Task response includes recurrence fields
- **WHEN** a client fetches any task via GET, POST, PUT, or PATCH endpoints
- **THEN** the response includes `recurrence_type` (string, default `"none"`) and `recurrence_rule` (object, default `{}`)

#### Scenario: Completion response includes next occurrence ID
- **WHEN** a recurring task is completed via POST `/api/tasks/:id/complete/`
- **THEN** the response includes `next_occurrence_id` set to the ID of the newly created task

#### Scenario: Non-recurring completion has null next occurrence
- **WHEN** a non-recurring task is completed via POST `/api/tasks/:id/complete/`
- **THEN** the response includes `next_occurrence_id` set to `null`

### Requirement: Recurrence fields in task update input
The system SHALL accept `recurrence_type` and `recurrence_rule` as optional fields in the task update endpoint, with validation per the recurrence rule validation requirements.

#### Scenario: Update request with invalid recurrence rejected
- **WHEN** a client sends PUT to `/api/tasks/:id/` with `{"recurrence_type": "weekly", "recurrence_rule": {"days": [9]}}`
- **THEN** the server responds with status 422 and a validation error message

#### Scenario: Partial update preserves existing recurrence
- **WHEN** a client sends PUT to `/api/tasks/:id/` with `{"title": "New title"}` for a task with existing recurrence
- **THEN** the task's `recurrence_type` and `recurrence_rule` remain unchanged
