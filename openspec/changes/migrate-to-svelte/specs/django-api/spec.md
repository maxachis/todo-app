## ADDED Requirements

### Requirement: JSON API layer using Django Ninja
The system SHALL expose all data operations as JSON API endpoints under the `/api/` URL prefix using Django Ninja. All endpoints SHALL accept and return `application/json` (except export/import which handle file downloads/uploads). All endpoints SHALL return appropriate HTTP status codes (200, 201, 400, 404, 409, 422).

#### Scenario: API returns JSON for valid request
- **WHEN** a client sends a GET request to `/api/lists/`
- **THEN** the server responds with status 200 and a JSON array of list objects

#### Scenario: API returns error for invalid request
- **WHEN** a client sends a POST to `/api/lists/` with an empty name
- **THEN** the server responds with status 422 and a JSON object containing field-level error messages

### Requirement: List CRUD endpoints
The system SHALL provide endpoints for list management: create, read, update, delete, and reorder.

#### Scenario: Create a list
- **WHEN** a client sends POST to `/api/lists/` with `{"name": "Work", "emoji": "💼"}`
- **THEN** the server creates the list and responds with status 201 and the serialized list object including its assigned `id` and `position`

#### Scenario: Get all lists
- **WHEN** a client sends GET to `/api/lists/`
- **THEN** the server responds with a JSON array of all lists ordered by position, each including `id`, `name`, `emoji`, `position`, and `project` FK

#### Scenario: Get list detail with sections and tasks
- **WHEN** a client sends GET to `/api/lists/:id/`
- **THEN** the server responds with the list object including nested `sections`, each containing nested `tasks` with their subtasks, tags, pinned status, and completion state

#### Scenario: Update a list
- **WHEN** a client sends PUT to `/api/lists/:id/` with `{"name": "Updated", "emoji": "🔥"}`
- **THEN** the server updates the list and responds with the updated list object

#### Scenario: Delete a list
- **WHEN** a client sends DELETE to `/api/lists/:id/`
- **THEN** the server deletes the list, its sections, and all tasks, and responds with status 204

#### Scenario: Reorder a list
- **WHEN** a client sends PATCH to `/api/lists/:id/move/` with `{"position": 2}`
- **THEN** the server updates the list's position and reorders siblings accordingly

### Requirement: Section CRUD endpoints
The system SHALL provide endpoints for section management within a list.

#### Scenario: Create a section
- **WHEN** a client sends POST to `/api/lists/:list_id/sections/` with `{"name": "To Do", "emoji": "📋"}`
- **THEN** the server creates the section in the specified list and responds with status 201

#### Scenario: Update a section
- **WHEN** a client sends PUT to `/api/sections/:id/` with `{"name": "In Progress"}`
- **THEN** the server updates the section and responds with the updated object

#### Scenario: Delete a section
- **WHEN** a client sends DELETE to `/api/sections/:id/`
- **THEN** the server deletes the section and all its tasks, responding with status 204

#### Scenario: Reorder a section
- **WHEN** a client sends PATCH to `/api/sections/:id/move/` with `{"position": 1}`
- **THEN** the server updates the section's position within its list

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
- **THEN** the server responds with the full task object including `title`, `notes`, `priority`, `due_date`, `due_time`, `is_completed`, `completed_at`, `is_pinned`, `tags`, `parent`, `section`, and nested `subtasks`

#### Scenario: Update task fields
- **WHEN** a client sends PUT to `/api/tasks/:id/` with `{"title": "Updated", "notes": "# Heading", "due_date": "2026-03-15", "priority": 3}`
- **THEN** the server updates the specified fields and responds with the updated task

#### Scenario: Delete a task
- **WHEN** a client sends DELETE to `/api/tasks/:id/`
- **THEN** the server deletes the task and all its subtasks, responding with status 204

### Requirement: Task completion endpoints
The system SHALL provide endpoints to complete and uncomplete tasks, with completion cascading to subtasks.

#### Scenario: Complete a task with subtasks
- **WHEN** a client sends POST to `/api/tasks/:id/complete/`
- **THEN** the server sets `is_completed=True` and `completed_at` on the task and all its non-completed subtasks recursively, and responds with the updated task including updated subtask states

#### Scenario: Uncomplete a task
- **WHEN** a client sends POST to `/api/tasks/:id/uncomplete/`
- **THEN** the server sets `is_completed=False` and clears `completed_at` on the task only (not subtasks), and responds with the updated task

### Requirement: Task move and reorder endpoint
The system SHALL provide an endpoint to move, reorder, and reparent tasks.

#### Scenario: Reorder task within section
- **WHEN** a client sends PATCH to `/api/tasks/:id/move/` with `{"position": 3}`
- **THEN** the server updates the task's position within its current section

#### Scenario: Move task to different section
- **WHEN** a client sends PATCH to `/api/tasks/:id/move/` with `{"section_id": 7, "position": 0}`
- **THEN** the server updates the task's section FK (and all descendants' section FKs) and sets its position

#### Scenario: Reparent task as subtask
- **WHEN** a client sends PATCH to `/api/tasks/:id/move/` with `{"parent_id": 12, "position": 0}`
- **THEN** the server sets the task's parent FK, making it a subtask

#### Scenario: Promote subtask to top-level
- **WHEN** a client sends PATCH to `/api/tasks/:id/move/` with `{"parent_id": null, "position": 5}`
- **THEN** the server clears the task's parent FK, promoting it to a top-level task

#### Scenario: Move task to different list
- **WHEN** a client sends PATCH to `/api/tasks/:id/move/` with `{"list_id": 3}`
- **THEN** the server moves the task (and descendants) to the first section of list 3

#### Scenario: Reject circular nesting
- **WHEN** a client sends PATCH to `/api/tasks/:id/move/` with `{"parent_id": <descendant_id>}`
- **THEN** the server responds with status 409 and an error message

### Requirement: Task pin toggle endpoint
The system SHALL provide an endpoint to toggle a task's pinned state, enforcing a maximum of 3 pinned tasks per list.

#### Scenario: Pin a task
- **WHEN** a client sends POST to `/api/tasks/:id/pin/` for an unpinned task with fewer than 3 pinned tasks in its list
- **THEN** the server sets `is_pinned=True` and responds with the updated task

#### Scenario: Unpin a task
- **WHEN** a client sends POST to `/api/tasks/:id/pin/` for a pinned task
- **THEN** the server sets `is_pinned=False` and responds with the updated task

#### Scenario: Reject pin over limit
- **WHEN** a client sends POST to `/api/tasks/:id/pin/` and the list already has 3 pinned tasks
- **THEN** the server responds with status 409 and an error message

### Requirement: Tag management endpoints
The system SHALL provide endpoints to add and remove tags on tasks.

#### Scenario: Add a tag to a task
- **WHEN** a client sends POST to `/api/tasks/:id/tags/` with `{"name": "urgent"}`
- **THEN** the server creates the tag if it doesn't exist, adds it to the task, and responds with the updated tag list

#### Scenario: Remove a tag from a task
- **WHEN** a client sends DELETE to `/api/tasks/:id/tags/:tag_id/`
- **THEN** the server removes the tag association and responds with status 204

#### Scenario: Tag autocomplete
- **WHEN** a client sends GET to `/api/tags/?exclude_task=:id`
- **THEN** the server responds with all tags not already assigned to the specified task

### Requirement: Search endpoint
The system SHALL provide a search endpoint that queries across all lists.

#### Scenario: Search returns grouped results
- **WHEN** a client sends GET to `/api/search/?q=groceries`
- **THEN** the server responds with matching tasks grouped by list, each including task title, section name, tags, and list info

#### Scenario: Search matches title, notes, and tags
- **WHEN** a client sends GET to `/api/search/?q=urgent`
- **THEN** the results include tasks where "urgent" appears in the title, notes, or any tag name (case-insensitive)

### Requirement: Export endpoints
The system SHALL provide endpoints to export lists in JSON, CSV, and Markdown formats as file downloads.

#### Scenario: Export single list as JSON
- **WHEN** a client sends GET to `/api/export/:id/json/`
- **THEN** the server responds with `Content-Disposition: attachment` and a JSON file containing the full nested hierarchy

#### Scenario: Export all lists as CSV
- **WHEN** a client sends GET to `/api/export/csv/`
- **THEN** the server responds with a CSV file with one row per task including `list`, `section`, `task`, `parent_task`, `depth`, `notes`, `due_date`, `tags`, `is_completed`

#### Scenario: Export as Markdown
- **WHEN** a client sends GET to `/api/export/:id/markdown/`
- **THEN** the server responds with a Markdown file using `#`/`##` headings and `- [ ]`/`- [x]` checkboxes

#### Scenario: Unsupported format returns error
- **WHEN** a client sends GET to `/api/export/:id/xml/`
- **THEN** the server responds with status 400

### Requirement: Import endpoint
The system SHALL provide an endpoint to import tasks from a TickTick CSV file.

#### Scenario: Successful import
- **WHEN** a client sends POST to `/api/import/` with a CSV file upload
- **THEN** the server creates lists, sections, tasks, and tags as needed and responds with a summary JSON including counts of created/skipped entities

#### Scenario: Duplicate detection
- **WHEN** a client re-imports a CSV containing tasks with `external_id` values that already exist
- **THEN** the server skips those tasks and reports them as skipped in the summary

#### Scenario: Invalid file type
- **WHEN** a client sends POST to `/api/import/` with a non-CSV file
- **THEN** the server responds with status 400

### Requirement: Project CRUD endpoints
The system SHALL provide endpoints for project management.

#### Scenario: Create a project
- **WHEN** a client sends POST to `/api/projects/` with `{"name": "Q1 Sprint", "description": "First quarter work"}`
- **THEN** the server creates the project and responds with status 201

#### Scenario: Get all projects with metrics
- **WHEN** a client sends GET to `/api/projects/`
- **THEN** the server responds with projects ordered by position, each including `total_hours`, `linked_lists_count`, `total_tasks`, and `completed_tasks`

#### Scenario: Delete a project
- **WHEN** a client sends DELETE to `/api/projects/:id/`
- **THEN** the server deletes the project, unlinks associated lists (sets `project=null`), and responds with status 204

#### Scenario: Toggle project active
- **WHEN** a client sends POST to `/api/projects/:id/toggle/`
- **THEN** the server flips `is_active` and responds with the updated project

### Requirement: Timesheet endpoints
The system SHALL provide endpoints for time entry management with weekly views.

#### Scenario: Get weekly timesheet
- **WHEN** a client sends GET to `/api/timesheet/?week=2026-02-16`
- **THEN** the server responds with time entries for that week grouped by date, plus a summary with total hours and per-project breakdowns

#### Scenario: Create time entry
- **WHEN** a client sends POST to `/api/timesheet/` with `{"project_id": 1, "date": "2026-02-17", "description": "API design", "task_ids": [3, 7]}`
- **THEN** the server creates the time entry and responds with status 201

#### Scenario: Delete time entry
- **WHEN** a client sends DELETE to `/api/timesheet/:id/`
- **THEN** the server deletes the entry and responds with status 204

#### Scenario: Get tasks for project
- **WHEN** a client sends GET to `/api/projects/:id/tasks/`
- **THEN** the server responds with incomplete tasks from all lists linked to that project

### Requirement: CSRF protection for same-origin requests
The system SHALL use Django's CSRF cookie mechanism for API protection. The API SHALL NOT require CORS headers since the frontend is served from the same origin.

#### Scenario: CSRF token in cookie
- **WHEN** a client makes any GET request
- **THEN** the server includes a `csrftoken` cookie in the response

#### Scenario: Mutating request with CSRF token
- **WHEN** a client sends a POST/PUT/PATCH/DELETE request with the `X-CSRFToken` header matching the cookie value
- **THEN** the server accepts the request

#### Scenario: Mutating request without CSRF token
- **WHEN** a client sends a POST request without the `X-CSRFToken` header
- **THEN** the server responds with status 403
