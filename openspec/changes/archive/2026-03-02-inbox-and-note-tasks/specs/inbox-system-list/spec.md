## ADDED Requirements

### Requirement: System-managed Inbox list
The system SHALL include a system-managed list named "Inbox" with `is_system=True`, `emoji="📥"`, and `position=0`. The Inbox list SHALL be created by a Django migration along with a single section with an empty name. The Inbox list SHALL always appear at position 0 in the sidebar, above all user-created lists.

#### Scenario: Inbox exists after migration
- **WHEN** the database migration runs
- **THEN** a List record exists with `name="Inbox"`, `emoji="📥"`, `is_system=True`, `position=0`, and one Section with `name=""`

#### Scenario: Inbox appears first in sidebar
- **WHEN** the user loads the Tasks view
- **THEN** the Inbox list appears at the top of the sidebar, above all user-created lists

#### Scenario: Existing list positions shifted
- **WHEN** the migration runs on a database with existing lists
- **THEN** all existing list positions are incremented by 1 before the Inbox is inserted at position 0

### Requirement: Inbox list is rename-locked and non-deletable
The system SHALL prevent renaming or deleting the Inbox list. The API update endpoint SHALL reject name changes on system lists with status 409. The API delete endpoint SHALL reject deletion of system lists with status 409. The frontend SHALL hide rename and delete controls for system lists.

#### Scenario: Attempt to rename Inbox via API
- **WHEN** a client sends PUT to `/api/lists/:inbox_id/` with `{"name": "My Inbox"}`
- **THEN** the server responds with status 409 and an error message indicating system lists cannot be renamed

#### Scenario: Attempt to delete Inbox via API
- **WHEN** a client sends DELETE to `/api/lists/:inbox_id/`
- **THEN** the server responds with status 409 and an error message indicating system lists cannot be deleted

#### Scenario: Emoji can be changed on system lists
- **WHEN** a client sends PUT to `/api/lists/:inbox_id/` with `{"emoji": "📬"}`
- **THEN** the server updates the emoji and responds with the updated list object

#### Scenario: Frontend hides rename/delete for Inbox
- **WHEN** the Inbox list renders in the sidebar
- **THEN** the double-click-to-edit and delete button controls are not present

### Requirement: Inbox section header is visually hidden
The system SHALL suppress the section header in the center panel when a section has an empty name. This allows the Inbox list's single section to display tasks without a visible section divider.

#### Scenario: Empty-name section has no header
- **WHEN** a list's section has `name=""`
- **THEN** the section header row (name, edit, delete controls) is not rendered, and tasks appear directly

#### Scenario: Named sections still show headers
- **WHEN** a section has a non-empty name
- **THEN** the section header renders normally with name, edit, and delete controls

### Requirement: Inbox excluded from drag reordering
The system SHALL exclude the Inbox list from drag-and-drop reordering in the sidebar. User-created lists remain reorderable among themselves.

#### Scenario: Inbox is not draggable
- **WHEN** the user attempts to drag the Inbox list in the sidebar
- **THEN** the drag does not initiate; the Inbox stays in its fixed position

#### Scenario: User lists reorder below Inbox
- **WHEN** the user drags a user-created list to a new position
- **THEN** the list reorders among other user-created lists, and the Inbox remains at the top

### Requirement: Section creation hidden for Inbox
The system SHALL hide the "Create section" form when viewing the Inbox list, since it uses a single implicit section.

#### Scenario: Inbox list has no create-section form
- **WHEN** the user selects the Inbox list
- **THEN** the section creation form is not displayed in the center panel

#### Scenario: Non-Inbox lists show create-section form
- **WHEN** the user selects a non-system list
- **THEN** the section creation form is displayed normally
