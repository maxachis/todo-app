## MODIFIED Requirements

### Requirement: List CRUD endpoints
The system SHALL provide endpoints for list management: create, read, update, delete, and reorder. System lists (where `is_system=True`) SHALL have restricted operations: the update endpoint SHALL reject name changes with status 409 (emoji changes are allowed), and the delete endpoint SHALL reject deletion with status 409. The GET endpoints SHALL include `is_system` in the serialized list response.

#### Scenario: Create a list
- **WHEN** a client sends POST to `/api/lists/` with `{"name": "Work", "emoji": "💼"}`
- **THEN** the server creates the list and responds with status 201 and the serialized list object including its assigned `id`, `position`, and `is_system` (false)

#### Scenario: Get all lists
- **WHEN** a client sends GET to `/api/lists/`
- **THEN** the server responds with a JSON array of all lists ordered by position, each including `id`, `name`, `emoji`, `position`, `project` FK, and `is_system`

#### Scenario: Get list detail with sections and tasks
- **WHEN** a client sends GET to `/api/lists/:id/`
- **THEN** the server responds with the list object including `is_system` and nested `sections`, each containing nested `tasks` with their subtasks, tags, pinned status, and completion state

#### Scenario: Update a list
- **WHEN** a client sends PUT to `/api/lists/:id/` with `{"name": "Updated", "emoji": "🔥"}`
- **THEN** the server updates the list and responds with the updated list object

#### Scenario: Update system list emoji
- **WHEN** a client sends PUT to `/api/lists/:inbox_id/` with `{"emoji": "📬"}` where the list has `is_system=True`
- **THEN** the server updates the emoji and responds with the updated list object

#### Scenario: Reject system list rename
- **WHEN** a client sends PUT to `/api/lists/:inbox_id/` with `{"name": "My Inbox"}` where the list has `is_system=True`
- **THEN** the server responds with status 409 and an error message

#### Scenario: Delete a list
- **WHEN** a client sends DELETE to `/api/lists/:id/` where `is_system=False`
- **THEN** the server deletes the list, its sections, and all tasks, and responds with status 204

#### Scenario: Reject system list deletion
- **WHEN** a client sends DELETE to `/api/lists/:id/` where `is_system=True`
- **THEN** the server responds with status 409 and an error message

#### Scenario: Reorder a list
- **WHEN** a client sends PATCH to `/api/lists/:id/move/` with `{"position": 2}`
- **THEN** the server updates the list's position and reorders siblings accordingly
