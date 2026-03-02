## MODIFIED Requirements

### Requirement: List sidebar navigation
The system SHALL display all lists in the sidebar, ordered by position, with system lists (Inbox) rendered first above a visual separator and excluded from drag-and-drop reordering. Selecting a list SHALL load its content in the center panel. System lists SHALL NOT display rename (double-click-to-edit) or delete controls.

#### Scenario: Sidebar displays lists with Inbox first
- **WHEN** the app loads
- **THEN** the sidebar shows the Inbox list at the top with a subtle separator below it, followed by user-created lists with their emoji and name, ordered by position

#### Scenario: Selecting a list loads its content
- **WHEN** the user clicks a list in the sidebar
- **THEN** the center panel displays that list's sections and tasks

#### Scenario: Initial selected list loads full content
- **WHEN** the Tasks route first loads with a default selected list
- **THEN** the list header and its sections/tasks are both loaded without requiring an extra click

#### Scenario: Empty state when no list selected
- **WHEN** no list is selected
- **THEN** the center panel shows "Select or create a list"

#### Scenario: Inline list editing
- **WHEN** the user double-clicks a non-system list in the sidebar
- **THEN** the list name and emoji become editable inline; Enter or emoji selection saves, Escape cancels

#### Scenario: Inline editing is single-active
- **WHEN** one list is already in inline edit mode and the user starts editing another list
- **THEN** the previous list is auto-saved and exits edit mode so only one inline editor remains active

#### Scenario: Sidebar emoji double-click edits list emoji
- **WHEN** the user double-clicks a non-system list emoji in the sidebar
- **THEN** an emoji picker opens for that list and selecting an emoji persists it

#### Scenario: Content header supports emoji and title double-click edits
- **WHEN** the user double-clicks the current list emoji or title in the center panel header for a non-system list
- **THEN** the corresponding list field enters edit flow and persists changes on selection/commit

#### Scenario: Header title edit exits on list change
- **WHEN** list-title inline edit is active and the user selects a different list
- **THEN** the prior title edit is committed and edit mode exits for the previous list

#### Scenario: Drag to reorder lists
- **WHEN** the user drags a non-system list in the sidebar
- **THEN** the list is repositioned among other non-system lists via svelte-dnd-action and the server is updated

#### Scenario: Inbox is not draggable
- **WHEN** the user attempts to drag the Inbox list
- **THEN** the drag does not initiate; the Inbox remains at the top of the sidebar

#### Scenario: System list hides rename and delete controls
- **WHEN** the Inbox list renders in the sidebar
- **THEN** no double-click-to-edit or delete button is available

### Requirement: Task detail panel
The system SHALL display a task's full details in the right panel when selected. All detail fields SHALL auto-save on blur. The detail panel SHALL include a List selector and a Section selector that allow moving the task to a different list and section. Changing the list SHALL reload the section dropdown with sections from the selected list. Selecting a new section SHALL move the task via the existing move API. A recurrence editor SHALL be displayed below the due date field. A "Linked People & Orgs" section SHALL be displayed below the tags section. On phone viewports (640px and below), form elements and buttons SHALL be sized for touch interaction.

#### Scenario: Selecting a task shows detail
- **WHEN** the user clicks a task row
- **THEN** the right panel displays the task's title, notes, due date, priority, tags, list, section, parent link, recurrence settings, and linked people & organizations

#### Scenario: List and section selectors show current location
- **WHEN** a task is selected
- **THEN** the List dropdown shows the task's current list and the Section dropdown shows the task's current section

#### Scenario: Change list loads target sections
- **WHEN** the user changes the List dropdown to a different list
- **THEN** the Section dropdown reloads with sections from the newly selected list and the first section is pre-selected

#### Scenario: Change section moves task
- **WHEN** the user selects a new section from the Section dropdown
- **THEN** the task is moved to that section via the move API and the center panel updates reactively

#### Scenario: Linked section appears in detail panel
- **WHEN** a task is selected
- **THEN** the detail panel includes a "Linked People & Orgs" section after the tags section, showing linked entities with add/remove controls

#### Scenario: Auto-save on blur
- **WHEN** the user edits the title, due date, or notes and then blurs the field
- **THEN** the change is saved to the API and the center panel task row updates reactively

#### Scenario: Empty state when no task selected
- **WHEN** no task is selected
- **THEN** the detail panel shows "Select a task to view details"

#### Scenario: Parent task link
- **WHEN** viewing a subtask's detail
- **THEN** a link to the parent task is shown with a "jump to" action that scrolls to and highlights the parent in the center panel

#### Scenario: Phone viewport detail panel touch targets
- **WHEN** the viewport is 640px or narrower
- **THEN** tag buttons, form inputs, and action buttons in the detail panel have a minimum touch target of 44px height
