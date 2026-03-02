### Requirement: SvelteKit application with static adapter
The system SHALL use SvelteKit with `adapter-static` to produce a static SPA build. The build output SHALL be plain HTML, JS, and CSS files requiring no Node.js runtime in production. The frontend SHALL be served by Nginx, with API requests proxied to Django.

#### Scenario: Static build produces deployable output
- **WHEN** the developer runs the SvelteKit build command
- **THEN** the output directory contains static HTML, JS, and CSS files that can be served by any web server

#### Scenario: Frontend loads without server-side rendering
- **WHEN** a user navigates to the app root
- **THEN** the SPA loads and fetches data from the Django API via client-side requests

### Requirement: Three-panel layout shell
The system SHALL render a three-panel layout: left sidebar (list navigation), center panel (task list), and right panel (task detail). The panel widths SHALL be user-adjustable via draggable resize handles on desktop viewports. A top navigation bar SHALL provide links to Tasks, Dashboard, Projects, Timesheet, CRM, Network, and Notebook pages. The navigation bar SHALL also include a settings cog button and a theme toggle control. The Import page SHALL NOT appear as a primary navigation tab; it SHALL be accessible via the settings dropdown menu. On phone viewports (640px and below), the app shell SHALL use `100dvh` (with `100vh` fallback) instead of `100vh` to account for mobile browser chrome resizing. All interactive elements in the navigation bar SHALL meet a 44px minimum touch target height on phone viewports. The CRM nav tab SHALL be highlighted as active when the current path starts with `/crm`. The Network nav tab SHALL be highlighted as active when the current path starts with `/network`. The Notebook nav tab SHALL be highlighted as active when the current path starts with `/notebook`.

#### Scenario: Desktop layout shows all three panels
- **WHEN** the viewport is wider than 1024px
- **THEN** the sidebar, center panel, and detail panel are all visible simultaneously

#### Scenario: Desktop layout includes resize handles
- **WHEN** the viewport is wider than 1024px and the user is on the Tasks route
- **THEN** draggable resize handles are rendered between the sidebar and center panel, and between the center panel and detail panel

#### Scenario: Desktop panel widths are user-adjustable
- **WHEN** the user drags a resize handle on the Tasks route
- **THEN** the grid column widths update to reflect the dragged position, with the center panel using remaining space

#### Scenario: Mobile layout collapses panels
- **WHEN** the viewport is narrower than 1024px
- **THEN** the sidebar is hidden behind a hamburger menu, and the detail panel slides in as an overlay

#### Scenario: Bottom tab bar on mobile
- **WHEN** the viewport is narrower than 1024px
- **THEN** a bottom tab bar shows navigation links for Tasks, Dashboard, Projects, Timesheet, CRM, and Network (Import is NOT included)

#### Scenario: Non-task routes hide task side panels
- **WHEN** the user navigates to CRM, Network, Dashboard, Projects, Timesheet, or Import routes
- **THEN** the list sidebar and task detail panel are not shown

#### Scenario: Navigation bar includes theme toggle and settings cog
- **WHEN** the navigation bar renders
- **THEN** a settings cog button and theme toggle control are displayed in the right area of the navigation bar

#### Scenario: Phone viewport uses dynamic viewport height
- **WHEN** the viewport is 640px or narrower
- **THEN** the app shell height uses `dvh` units (with `vh` fallback) so content is not hidden behind mobile browser chrome

#### Scenario: Phone viewport touch targets in navbar
- **WHEN** the viewport is 640px or narrower
- **THEN** all navbar buttons (hamburger, settings cog, theme toggle, detail panel toggle) have a minimum touch target of 44px height

#### Scenario: CRM nav tab active on CRM sub-routes
- **WHEN** the user is on `/crm/people`, `/crm/orgs`, `/crm/interactions`, or `/crm/leads`
- **THEN** the CRM tab in the top navbar is highlighted as active

#### Scenario: Network nav tab active on Network sub-routes
- **WHEN** the user is on `/network/relationships` or `/network/graph`
- **THEN** the Network tab in the top navbar is highlighted as active

#### Scenario: User sees Notebook tab
- **WHEN** the user views any page
- **THEN** the top navigation bar displays a "Notebook" tab

#### Scenario: Notebook tab is highlighted on notebook routes
- **WHEN** the user is on `/notebook` or `/notebook/some-page`
- **THEN** the "Notebook" tab is highlighted in the navigation bar

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

### Requirement: Section display and management
The system SHALL display sections within a list, each collapsible, with tasks nested inside.

#### Scenario: Sections render in order
- **WHEN** a list is loaded
- **THEN** its sections display in position order, each showing its emoji and name

#### Scenario: Sections are collapsible
- **WHEN** the user clicks a section's collapse toggle
- **THEN** the section's tasks are hidden/shown

#### Scenario: Section title inline editing is single-active
- **WHEN** one section title is being edited and the user starts editing a different section title
- **THEN** the first edit is committed and closed so only one section editor is active

#### Scenario: Collapse all / expand all
- **WHEN** the user clicks the "Collapse All" toggle in the list header
- **THEN** all sections collapse; clicking again expands all

#### Scenario: Drag to reorder sections
- **WHEN** the user drags a section to a new position within the list
- **THEN** the section order updates immediately and persists via API

#### Scenario: Section drag starts only from header handle
- **WHEN** the user attempts to drag from task rows/body area inside a section
- **THEN** section drag does not initiate; dragging sections is only available from a handle in the section header

### Requirement: Section layout ordering
Within each section in the Tasks view, elements SHALL render in the following order:
1. Section header
2. Active (incomplete) tasks with drag-and-drop
3. Task creation form
4. Completed tasks (collapsible)

The completed tasks section SHALL retain its existing collapsible toggle, count display, and styling. The task creation form SHALL appear directly after active tasks, before any completed tasks.

#### Scenario: Task create form appears before completed tasks
- **WHEN** a section contains both active and completed tasks
- **THEN** the task creation form SHALL render between the active tasks and the completed tasks section

#### Scenario: Section with no completed tasks
- **WHEN** a section has no completed tasks
- **THEN** the task creation form SHALL render directly after active tasks with no completed section visible

#### Scenario: Completed section collapse state preserved
- **WHEN** the user toggles the completed section open or closed
- **THEN** the toggle behavior SHALL work identically to the current implementation, just in its new position below the task creation form

### Requirement: Task list rendering
The system SHALL display tasks within sections, showing title, tags, due date, subtask count, pin button, and a recurrence indicator. Completed tasks SHALL appear in a separate "Completed" group below the task creation form. On phone viewports (640px and below), task row metadata SHALL wrap instead of overflowing, and interactive elements SHALL meet minimum touch target sizes. The inline task title edit input SHALL stop click event propagation so that clicks within the input do not exit edit mode.

#### Scenario: Tasks render with metadata
- **WHEN** a section is displayed
- **THEN** each task row shows its title, tag badges, abbreviated due date, subtask count label, and a repeat icon if the task has recurrence

#### Scenario: Recurring task shows repeat indicator
- **WHEN** a task has `recurrence_type` other than `none`
- **THEN** the task row displays a small repeat icon (e.g., circular arrows) near the due date

#### Scenario: Completed tasks grouped separately
- **WHEN** a section contains completed tasks
- **THEN** completed tasks appear under a collapsible "Completed" subsection

#### Scenario: Subtask count label
- **WHEN** a task has subtasks
- **THEN** the task row displays a label like "3 subtasks — 1 open" that updates reactively

#### Scenario: Subtask nesting display
- **WHEN** a task has subtasks
- **THEN** subtasks are rendered nested below the parent with visual indentation, collapsible via a toggle

#### Scenario: Phone viewport task row metadata wraps
- **WHEN** the viewport is 640px or narrower and a task row has metadata (tags, due date, subtask count)
- **THEN** the metadata section wraps to a second line instead of overflowing horizontally

#### Scenario: Phone viewport task row touch targets
- **WHEN** the viewport is 640px or narrower
- **THEN** task row checkboxes and pin buttons have a minimum touch target of 44px

#### Scenario: Inline title edit stays active on click
- **WHEN** the user has double-clicked a task title to enter edit mode and then clicks inside the title input
- **THEN** the input SHALL retain focus and edit mode SHALL remain active
- **AND** the click SHALL NOT propagate to the parent task row's click handler

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

### Requirement: Task detail panel includes notebook mentions
The task detail panel SHALL include a collapsible "Notebook Mentions" section showing pages that mention the selected task. The section SHALL fetch data from `GET /api/notebook/mentions/task/{id}/` and display each entry as a clickable row with page title, type badge, and content snippet. Clicking an entry SHALL navigate to `/notebook/{slug}`. The section SHALL be hidden when there are no mentions.

#### Scenario: Task with notebook mentions
- **WHEN** the user views a task that is mentioned in 2 notebook pages
- **THEN** a "Notebook Mentions" section displays with 2 entries

#### Scenario: Task with no notebook mentions
- **WHEN** the user views a task with no notebook mentions
- **THEN** the "Notebook Mentions" section is not displayed

### Requirement: Live Markdown editor
The system SHALL provide a block-based Markdown editor for task notes. Inactive blocks SHALL show rendered HTML; the active block SHALL show raw Markdown. The editor SHALL provide visual affordances indicating that content is editable.

#### Scenario: Click to edit a block
- **WHEN** the user clicks a rendered Markdown block in the notes area
- **THEN** that block switches to a raw Markdown textarea for editing

#### Scenario: Blur saves and renders
- **WHEN** the user blurs the active Markdown block
- **THEN** the block saves via API and renders back to HTML

#### Scenario: Supported Markdown syntax
- **WHEN** the user writes Markdown using headings, bold, italic, strikethrough, inline code, lists, blockquotes, code fences, or horizontal rules
- **THEN** the rendered output displays the correct HTML formatting

#### Scenario: XSS sanitization
- **WHEN** task notes contain script tags or event handler attributes
- **THEN** the rendered HTML strips all dangerous content

#### Scenario: Empty notes placeholder
- **WHEN** the notes field has no content
- **THEN** the editor SHALL display a muted placeholder text "Click to add notes..." that invites interaction
- **AND** clicking the placeholder SHALL open the editor textarea for that block

#### Scenario: Hover edit affordance on rendered blocks
- **WHEN** the user hovers over a rendered Markdown block that has content
- **THEN** a small pencil icon SHALL appear in the top-right corner of the block to indicate editability
- **AND** the block border and background SHALL become visible to reinforce interactivity

#### Scenario: Keyboard accessibility of edit affordance
- **WHEN** a rendered Markdown block receives keyboard focus
- **THEN** the same visual affordance (border, background) SHALL appear as on hover

### Requirement: Task completion with optimistic UI
The system SHALL provide task completion with immediate visual feedback. Completing a parent SHALL cascade to non-completed subtasks. Completing a recurring task SHALL display a toast indicating the next occurrence.

#### Scenario: Complete a task with animation
- **WHEN** the user checks a task's completion checkbox
- **THEN** the task fades out (180ms), moves to the "Completed" section, and a toast appears offering undo

#### Scenario: Complete a recurring task shows next occurrence toast
- **WHEN** the user completes a recurring task
- **THEN** a toast appears with the message "Next: [due date]" and the new task instance appears in the section

#### Scenario: Undo via toast
- **WHEN** the user clicks "Undo" on the toast within 5 seconds
- **THEN** the task is uncompleted and returns to its original position

#### Scenario: Toast auto-dismisses
- **WHEN** 5 seconds pass after a completion toast appears
- **THEN** the toast dismisses automatically

#### Scenario: Cascade completion to subtasks
- **WHEN** the user completes a parent task
- **THEN** all non-completed subtasks are also marked complete, with the UI updating reactively

### Requirement: Drag-and-drop with svelte-dnd-action
The system SHALL use svelte-dnd-action for section and list drag-and-drop interactions. Task drag-and-drop SHALL use svelte-dnd-action for the drag gesture with pointer events for midpoint-based drop detection, to support both reordering (place before) and nesting (make subtask) from a single drag gesture. Drop events SHALL update the Svelte store optimistically, then persist via API.

#### Scenario: Reorder task within section
- **WHEN** the user drags a task and drops it above the midpoint of another task in the same section
- **THEN** the task is placed before the drop target at the same nesting level and the new position persists via API

#### Scenario: Task drag lock during finalize
- **WHEN** a task drag finalize/persist cycle is in progress
- **THEN** initiating another task drag is disabled until the first cycle completes

#### Scenario: Drag visual tracks cursor
- **WHEN** the user drags a task
- **THEN** the browser's native drag ghost follows the cursor

#### Scenario: Move task to different section
- **WHEN** the user drags a task and drops it above the midpoint of a task in a different section
- **THEN** the task appears in the new section at the drop target's level and the section/position change persists

#### Scenario: Nest task as subtask
- **WHEN** the user drags a task and drops it below the midpoint of another task
- **THEN** the dragged task becomes a subtask of the drop target, updating visually and persisting via API

#### Scenario: Midpoint controls drop intent on task rows
- **WHEN** the user drags task A over task B
- **THEN** dropping above task B's midpoint inserts task A before task B at task B's current hierarchy level, and dropping below task B's midpoint nests task A under task B

#### Scenario: Promote subtask
- **WHEN** the user drags a subtask and drops it above the midpoint of a top-level task
- **THEN** the subtask becomes a top-level task in the section

#### Scenario: Move task to different list via sidebar
- **WHEN** the user drags a task onto a list in the sidebar
- **THEN** the task moves to the first section of that list, with all subtasks following

#### Scenario: API failure rolls back
- **WHEN** a drag operation succeeds visually but the API call fails
- **THEN** the store reverts to the pre-drag state and a toast shows an error message

#### Scenario: Reorder sections within list
- **WHEN** the user drags a section to a new position within the list
- **THEN** the section order updates immediately via svelte-dnd-action and persists via API

#### Scenario: Reorder lists in sidebar
- **WHEN** the user drags a list to a new position in the sidebar
- **THEN** the list order updates immediately via svelte-dnd-action and persists via API

#### Scenario: Reorder does not create duplicate keyed items
- **WHEN** the user reorders lists, sections, or tasks via drag-and-drop
- **THEN** keyed render collections remain unique by item id and no duplicate-key runtime error is produced

#### Scenario: Reordered items remain visible
- **WHEN** a drag reorder finalize completes
- **THEN** both moved and non-moved items remain visible in the list (no disappearing rows/sections)

### Requirement: Keyboard navigation
The system SHALL support full keyboard navigation for tasks. Navigation state SHALL be managed in a Svelte store. Destructive single-key shortcuts ("x" for complete, "Delete" for delete) SHALL only fire when the keyboard event originates from within a task row element (`[data-task-id]`). Non-destructive navigation shortcuts (j/k, arrow keys, Tab/Shift+Tab, Ctrl+arrows, Escape) SHALL continue to work from any focused element within the keyboard scope.

#### Scenario: Arrow key navigation
- **WHEN** the user presses Arrow Up or Arrow Down (or j/k)
- **THEN** the focus moves to the previous/next non-completed task, scrolling into view

#### Scenario: Click-to-keyboard continuity
- **WHEN** the user clicks a task row and then presses Arrow Up or Arrow Down
- **THEN** keyboard navigation applies immediately without requiring an additional focus click

#### Scenario: Arrow key navigation from task-add input
- **WHEN** the user is focused on a task-add input ("Add task..." or "Add subtask...") and presses Arrow Up or Arrow Down
- **THEN** the input SHALL be blurred and keyboard navigation SHALL select the nearest task in the pressed direction immediately, without requiring a second keypress

#### Scenario: Escape in task-add input
- **WHEN** the user is focused on a task-add input and presses Escape
- **THEN** any typed text SHALL be cleared and the input SHALL be blurred

#### Scenario: Tab indent / Shift+Tab outdent
- **WHEN** the user presses Tab on a focused task
- **THEN** the task becomes a subtask of the previous sibling; Shift+Tab promotes it

#### Scenario: Tab indent is section-bounded
- **WHEN** the user presses Tab and the previous visible task is in a different section
- **THEN** no cross-section indent/reparent occurs and the task remains in its current section

#### Scenario: Tab indent is same-level bounded
- **WHEN** the user presses Tab on a task and the closest previous visible task is a deeper child level
- **THEN** the task does not indent under that child and instead uses the closest previous task at the same current level

#### Scenario: Outdent places task after former parent
- **WHEN** the user presses Shift+Tab on a subtask
- **THEN** the task is promoted one level and inserted immediately after its former parent in sibling order

#### Scenario: Shift+Tab applies on first press
- **WHEN** the user presses Shift+Tab on a focused subtask
- **THEN** outdent is applied immediately without requiring a second keypress

#### Scenario: Browser tab traversal is suppressed for task hierarchy shortcuts
- **WHEN** a task is selected and the user presses Tab or Shift+Tab outside text-entry fields
- **THEN** browser focus traversal does not run, and task indent/outdent is applied immediately

#### Scenario: Complete with x key when focused on task row
- **WHEN** the user presses "x" and focus is on a task row element (`[data-task-id]`)
- **THEN** the task is completed (same behavior as clicking the checkbox)

#### Scenario: x key ignored when focus is not on task row
- **WHEN** the user presses "x" and focus is NOT on a task row element (e.g., focus is on a section header, button, or any other element inside the keyboard scope)
- **THEN** the keystroke SHALL be ignored and no task SHALL be completed

#### Scenario: Delete with Delete key when focused on task row
- **WHEN** the user presses Delete and focus is on a task row element (`[data-task-id]`)
- **THEN** a confirmation dialog appears; confirming deletes the task

#### Scenario: Delete key ignored when focus is not on task row
- **WHEN** the user presses Delete and focus is NOT on a task row element
- **THEN** the keystroke SHALL be ignored and no task SHALL be deleted

#### Scenario: Escape clears selection
- **WHEN** the user presses Escape
- **THEN** the task selection is cleared and the detail panel shows empty state

#### Scenario: Section jumping
- **WHEN** the user presses Ctrl+Arrow Down or Ctrl+Arrow Up
- **THEN** focus jumps to the first task of the next/previous section

#### Scenario: List cycling
- **WHEN** the user presses Ctrl+Arrow Left or Ctrl+Arrow Right
- **THEN** the previous/next list in the sidebar is selected

#### Scenario: Collapsed sections are skipped
- **WHEN** navigating with arrow keys and a section is collapsed
- **THEN** tasks inside that section are skipped

### Requirement: Emoji picker component
The system SHALL provide a searchable emoji picker modal for lists and sections.

#### Scenario: Open emoji picker
- **WHEN** the user clicks the emoji field on a list or section edit form
- **THEN** a modal appears with a searchable grid of emojis across categories

#### Scenario: Search uses names and keywords across an expansive set
- **WHEN** the user types a text query in the emoji search input
- **THEN** results are filtered by category label, emoji name, and related keywords across a broad emoji catalog (not only a small fixed subset)

#### Scenario: Select emoji
- **WHEN** the user clicks an emoji in the picker
- **THEN** the emoji is applied to the list/section and the picker closes

#### Scenario: Close picker
- **WHEN** the user presses Escape or clicks outside the picker
- **THEN** the picker closes without changing the emoji

### Requirement: Search across all lists
The system SHALL provide a global search bar that queries the API with debounced input. On phone viewports (640px and below), the search input SHALL use fluid width instead of a fixed pixel width.

#### Scenario: Debounced search
- **WHEN** the user types in the search bar
- **THEN** a search request fires after 300ms of inactivity

#### Scenario: Results display
- **WHEN** search results are returned
- **THEN** they display in a dropdown grouped by list, showing task title, section name, and tags

#### Scenario: Navigate to result
- **WHEN** the user clicks a search result
- **THEN** the app navigates to that task's list and selects the task, loading its detail panel

#### Scenario: Close results
- **WHEN** the user clicks outside the search dropdown
- **THEN** the results close

#### Scenario: Phone viewport search is fluid width
- **WHEN** the viewport is 640px or narrower
- **THEN** the search input uses fluid width (not fixed 220px) to fit within the available navbar space

### Requirement: Task pinning UI
The system SHALL display a "Pinned" section at the top of the list when any tasks are pinned, and provide a pin toggle button on task rows.

#### Scenario: Pinned section displays
- **WHEN** a list has pinned tasks
- **THEN** a "Pinned" section appears at the top showing pinned tasks in compact view

#### Scenario: Pinned section hidden when empty
- **WHEN** no tasks are pinned in the current list
- **THEN** the pinned section is not rendered

#### Scenario: Click pinned task jumps to location
- **WHEN** the user clicks a task in the pinned section
- **THEN** the view scrolls to the task's actual location in the list with a flash animation

#### Scenario: Pin button hidden on completed tasks
- **WHEN** a task is completed
- **THEN** the pin button is not shown on its task row

#### Scenario: Pinned order remains stable across source reorders
- **WHEN** pinned tasks are reordered within section/task lists
- **THEN** the pinned section keeps a stable orientation independent of source list position changes

#### Scenario: Reorder pinned tasks inside pinned section
- **WHEN** the user drags pinned tasks within the pinned section
- **THEN** the pinned section order updates to the new arrangement

### Requirement: Export UI
The system SHALL provide export buttons that trigger file downloads from the API.

#### Scenario: Export single list
- **WHEN** the user clicks an export button on a list and selects a format
- **THEN** the browser downloads the exported file

#### Scenario: Export all lists
- **WHEN** the user clicks the "Export All" button in the sidebar header
- **THEN** the browser downloads a file containing all lists in the selected format

### Requirement: Projects page
The system SHALL provide a dedicated page at `/projects` for project management with CRUD operations and metrics display. On phone viewports (640px and below), the create form SHALL stack vertically and card action buttons SHALL be touch-sized.

#### Scenario: Projects page displays cards
- **WHEN** the user navigates to `/projects`
- **THEN** the page shows project cards ordered by position, each displaying name, description, total hours, linked lists count, total tasks, and completed tasks

#### Scenario: Create project
- **WHEN** the user fills in the create project form and submits
- **THEN** the project is created and appears in the list

#### Scenario: Toggle project active status
- **WHEN** the user clicks the active/inactive toggle on a project card
- **THEN** the project's status flips and the UI updates

#### Scenario: Phone viewport create form stacks vertically
- **WHEN** the viewport is 640px or narrower
- **THEN** the project create form fields stack vertically (single column) instead of side-by-side

#### Scenario: Phone viewport card action buttons are touch-sized
- **WHEN** the viewport is 640px or narrower
- **THEN** project card action buttons have a minimum touch target of 44px height

### Requirement: Project detail view includes notebook mentions
The project page SHALL include a collapsible "Notebook Mentions" section on project cards for projects that are mentioned in notebook pages. The section SHALL fetch data from `GET /api/notebook/mentions/project/{id}/` and display entries as clickable rows.

#### Scenario: Project with notebook mentions
- **WHEN** a project is mentioned in notebook pages
- **THEN** the project card displays a "Notebook Mentions" section with clickable entries

#### Scenario: Project with no notebook mentions
- **WHEN** a project has no notebook mentions
- **THEN** no "Notebook Mentions" section is shown on the project card

### Requirement: Timesheet page
The system SHALL provide a dedicated page at `/timesheet` for weekly time tracking with navigation and summaries. The task selector SHALL use a hierarchical checkbox-based picker that displays tasks with indentation reflecting their parent-child nesting, replacing the native `<select multiple>`. Time entry rows SHALL display associated task names with hierarchy breadcrumbs instead of omitting task information. On phone viewports (640px and below), the summary bar, entry form, week navigation, and entry rows SHALL wrap/stack to prevent horizontal overflow.

#### Scenario: Weekly view with navigation
- **WHEN** the user navigates to `/timesheet`
- **THEN** the page shows the current week's time entries with previous/next week navigation

#### Scenario: Summary bar
- **WHEN** viewing a week's timesheet
- **THEN** a summary bar shows total hours and per-project breakdowns

#### Scenario: Week bounds are Sunday through Saturday
- **WHEN** a week is loaded in the timesheet view
- **THEN** the range begins on Sunday and ends on Saturday

#### Scenario: Create time entry
- **WHEN** the user fills in the time entry form (project, date, description, optional tasks) and submits
- **THEN** the entry is created and appears in the appropriate date group

#### Scenario: Entry rows display local creation time
- **WHEN** timesheet entries are listed
- **THEN** each row shows the entry creation time in the user's local device time

#### Scenario: Task selector shows hierarchical tree by project
- **WHEN** the user selects a project in the time entry form
- **THEN** a checkbox-based task picker shows incomplete tasks from that project's linked lists, indented by their nesting depth

#### Scenario: Entry rows display associated task names
- **WHEN** timesheet entries with linked tasks are listed
- **THEN** each entry row displays task names with parent hierarchy breadcrumbs

#### Scenario: Phone viewport summary bar wraps
- **WHEN** the viewport is 640px or narrower
- **THEN** the summary bar items wrap to multiple lines instead of overflowing horizontally

#### Scenario: Phone viewport entry form stacks
- **WHEN** the viewport is 640px or narrower
- **THEN** the time entry form fields stack vertically to fit the narrow viewport

#### Scenario: Phone viewport week navigation fits
- **WHEN** the viewport is 640px or narrower
- **THEN** the week navigation (prev/next buttons and date range) fits within the viewport without overflow

#### Scenario: Phone viewport entry rows wrap
- **WHEN** the viewport is 640px or narrower
- **THEN** entry row content (project, time, description, tasks, delete button) wraps to fit without horizontal overflow

### Requirement: Import page
The system SHALL provide a dedicated page at `/import` for importing tasks from TickTick CSV files, the app's native JSON export, and the app's native CSV export.

#### Scenario: Upload CSV file
- **WHEN** the user selects a `.csv` file and submits the import form
- **THEN** the file is uploaded to the API and a summary shows counts of created/skipped entities

#### Scenario: Upload JSON file
- **WHEN** the user selects a `.json` file and submits the import form
- **THEN** the file is uploaded to the API and a summary shows counts of created/skipped entities

#### Scenario: Import error display
- **WHEN** the import fails (invalid file, parse error, unrecognized format)
- **THEN** the error message is displayed to the user

#### Scenario: File picker accepts JSON and CSV
- **WHEN** the user clicks the file input on the import page
- **THEN** the file picker filters for `.csv` and `.json` files

### Requirement: Svelte store state management
The system SHALL manage application state using Svelte writable stores, one per resource type, with co-located async mutation functions. Tag add and remove operations SHALL update the task in both `selectedTaskDetail` and `listsStore` so that all subscribed components (detail panel and task list rows) re-render with current tag data.

#### Scenario: Store updates propagate to all subscribers
- **WHEN** a task is completed via the store's `completeTask()` function
- **THEN** all components subscribed to the tasks store re-render with the updated state

#### Scenario: Optimistic updates with rollback
- **WHEN** a mutation function updates the store optimistically and the API call fails
- **THEN** the store reverts to the previous state and a toast shows the error

#### Scenario: Tag add updates task in list store
- **WHEN** a user adds a tag to a task via the detail panel
- **THEN** the task object in `listsStore` SHALL be replaced with the refreshed task, causing `TaskRow` to display the new tag immediately

#### Scenario: Tag remove updates task in list store
- **WHEN** a user removes a tag from a task via the detail panel
- **THEN** the task object in `listsStore` SHALL be replaced with the refreshed task, causing `TaskRow` to remove the tag immediately

### Requirement: Toast notification system
The system SHALL provide a toast notification component that supports multiple concurrent toasts with auto-dismiss.

#### Scenario: Toast appears on action
- **WHEN** a task is completed
- **THEN** a toast appears with an "Undo" button

#### Scenario: Multiple toasts stack
- **WHEN** multiple actions trigger toasts in rapid succession
- **THEN** toasts stack vertically without replacing each other

#### Scenario: Auto-dismiss after timeout
- **WHEN** 5 seconds pass after a toast appears
- **THEN** the toast dismisses automatically

### Requirement: TypeScript type safety
The system SHALL use TypeScript for all frontend code. API response types SHALL be defined as TypeScript interfaces matching the Django Ninja response schemas.

#### Scenario: Type mismatch caught at build time
- **WHEN** a component accesses a property that doesn't exist on the API response type
- **THEN** the TypeScript compiler reports an error during build

### Requirement: Recurrence editor in task detail
The system SHALL provide a recurrence editor in the task detail panel that allows setting and modifying repeat schedules. The editor SHALL appear below the due date field.

#### Scenario: Recurrence type selector
- **WHEN** the user views a task's detail panel
- **THEN** a "Repeat" dropdown is shown with options: None, Daily, Weekly, Monthly, Yearly, Custom Dates

#### Scenario: Weekly recurrence shows day picker
- **WHEN** the user selects "Weekly" from the repeat dropdown
- **THEN** a row of weekday toggles (Mon-Sun) appears for selecting which days the task repeats

#### Scenario: Monthly recurrence shows day-of-month input
- **WHEN** the user selects "Monthly" from the repeat dropdown
- **THEN** a numeric input appears for selecting the day of the month (1-31)

#### Scenario: Yearly recurrence shows month and day inputs
- **WHEN** the user selects "Yearly" from the repeat dropdown
- **THEN** month and day inputs appear for selecting the annual date

#### Scenario: Custom dates shows date list editor
- **WHEN** the user selects "Custom Dates" from the repeat dropdown
- **THEN** an interface appears to add/remove MM-DD date entries, displayed as a list

#### Scenario: Recurrence changes auto-save on blur
- **WHEN** the user changes the recurrence type or rule parameters and blurs the editor
- **THEN** the recurrence settings are saved to the API via the task update endpoint

#### Scenario: Daily recurrence has no extra options
- **WHEN** the user selects "Daily" from the repeat dropdown
- **THEN** no additional configuration inputs appear (daily is the only option needed)

#### Scenario: Clearing recurrence
- **WHEN** the user selects "None" from the repeat dropdown on a recurring task
- **THEN** the recurrence is removed and the task behaves as a one-off task on next completion

### Requirement: Recurrence-aware TypeScript types
The system SHALL extend the frontend Task type to include recurrence fields for type-safe access throughout the UI.

#### Scenario: Task type includes recurrence fields
- **WHEN** the frontend TypeScript types are defined
- **THEN** the `Task` interface includes `recurrence_type: string`, `recurrence_rule: object`, and `next_occurrence_id: number | null`

#### Scenario: UpdateTaskInput includes recurrence fields
- **WHEN** the frontend update input type is defined
- **THEN** the `UpdateTaskInput` interface includes optional `recurrence_type?: string` and `recurrence_rule?: object`

### Requirement: Upcoming dashboard phone layout
The system SHALL render the Upcoming dashboard without horizontal overflow on phone viewports (640px and below). Task location text SHALL be truncated with ellipsis when it exceeds available space.

#### Scenario: Phone viewport location text truncation
- **WHEN** the viewport is 640px or narrower and an upcoming task has a long location path (list name / section name)
- **THEN** the location text is truncated with ellipsis instead of overflowing or wrapping awkwardly

#### Scenario: Phone viewport upcoming task rows fit
- **WHEN** the viewport is 640px or narrower
- **THEN** upcoming task rows render without horizontal overflow, with metadata stacking if needed

### Requirement: Relationships page phone layout
The system SHALL render the Relationships page at `/network/relationships` without text overflow on phone viewports (640px and below). Relationship titles SHALL be truncated with ellipsis and action buttons SHALL meet minimum touch target sizes.

#### Scenario: Phone viewport relationship title truncation
- **WHEN** the viewport is 640px or narrower and a relationship title (e.g., "Person A ↔ Person B") exceeds the card width
- **THEN** the title is truncated with ellipsis

#### Scenario: Phone viewport relationship action buttons are touch-sized
- **WHEN** the viewport is 640px or narrower
- **THEN** relationship card action buttons have a minimum touch target of 44px height

### Requirement: CRM sub-tab navigation
The CRM layout SHALL display sub-tabs in the order: **Inbox**, People, Orgs, Interactions, Leads. The Inbox tab SHALL link to `/crm/inbox`. The Inbox tab SHALL display a count badge showing the number of pending contact drafts (non-promoted, non-dismissed). The badge SHALL be hidden when the count is zero.

#### Scenario: CRM tabs include Inbox first
- **WHEN** the user navigates to any `/crm/*` route
- **THEN** the sub-tabs display in order: Inbox, People, Orgs, Interactions, Leads

#### Scenario: Inbox badge shows pending count
- **WHEN** there are 3 pending contact drafts
- **THEN** the Inbox tab displays "Inbox (3)" or a numeric badge next to the label

#### Scenario: Inbox badge hidden when empty
- **WHEN** there are no pending contact drafts
- **THEN** the Inbox tab displays "Inbox" with no badge

### Requirement: CRM Inbox page
The system SHALL provide a `/crm/inbox` route displaying pending contact drafts in a two-panel layout matching the existing CRM pattern: a list of drafts (left) and a triage detail panel (right). The `/crm` root route SHALL redirect to `/crm/inbox` instead of `/crm/people`.

#### Scenario: Inbox loads with pending drafts
- **WHEN** the user navigates to `/crm/inbox` with pending drafts
- **THEN** the left panel shows a list of drafts with name and quick notes preview, ordered by most recent first

#### Scenario: Inbox empty state
- **WHEN** the user navigates to `/crm/inbox` with no pending drafts
- **THEN** the page shows an empty state message (e.g., "No contacts to triage. Use @new[Name] in notebook pages to capture contacts.")

#### Scenario: Select a draft shows triage detail
- **WHEN** the user clicks a draft in the list
- **THEN** the right panel shows the draft's name, full quick notes, source page link, match hints (if any), and action buttons

### Requirement: Triage detail panel
The triage detail panel SHALL display: the draft name (as heading), quick notes (as body text), source page (as clickable link to `/notebook/{slug}`), match hints (people and org matches from the API), and action buttons. The action buttons SHALL be: "→ Person" (opens promotion form for Person), "→ Org" (opens promotion form for Organization), and "Dismiss" (dismisses the draft).

#### Scenario: Source page link navigates to notebook
- **WHEN** the user clicks the source page link in the triage detail
- **THEN** the app navigates to `/notebook/{source_page_slug}`

#### Scenario: Match hints displayed
- **WHEN** a draft is selected and the matches API returns existing people or orgs
- **THEN** the detail panel shows a "Possible matches" section listing each match with a "Link to [Name]" button

#### Scenario: No match hints
- **WHEN** a draft is selected and the matches API returns empty arrays
- **THEN** no "Possible matches" section is shown

### Requirement: Promote to Person form
Clicking "→ Person" in the triage detail SHALL display an inline form pre-filled from the draft. The first token of the draft name SHALL pre-fill `first_name`, the remaining tokens SHALL pre-fill `last_name`. The `notes` field SHALL pre-fill with the draft's `quick_notes`. Additional optional fields SHALL be shown: `middle_name`, `email`, `linkedin_url`, `follow_up_cadence_days`. The form SHALL submit to the promote-to-person API endpoint. On success, the draft disappears from the list and the next pending draft (if any) is auto-selected.

#### Scenario: Name split pre-fill
- **WHEN** the user clicks "→ Person" for a draft named "Jane Smith"
- **THEN** the form shows `first_name="Jane"` and `last_name="Smith"`

#### Scenario: Multi-word name split
- **WHEN** the user clicks "→ Person" for a draft named "Mary Jane Watson"
- **THEN** the form shows `first_name="Mary"` and `last_name="Jane Watson"` (first token vs rest)

#### Scenario: Quick notes pre-fill
- **WHEN** the draft has `quick_notes="works at Stripe"`
- **THEN** the notes field is pre-filled with "works at Stripe"

#### Scenario: Successful promotion
- **WHEN** the user fills in required fields and submits the Person form
- **THEN** the draft is promoted, removed from the inbox list, and the next draft is selected

#### Scenario: Duplicate person name error
- **WHEN** the user submits a Person form with a name that already exists (409 from API)
- **THEN** an error toast is shown and the form remains open

### Requirement: Promote to Organization form
Clicking "→ Org" in the triage detail SHALL display an inline form pre-filled from the draft. The `name` field SHALL pre-fill with the full draft name. The `org_type` field SHALL use a TypeaheadSelect with inline creation (matching the existing Orgs page pattern). The `notes` field SHALL pre-fill with the draft's `quick_notes`. The form SHALL submit to the promote-to-org API endpoint.

#### Scenario: Org form pre-fill
- **WHEN** the user clicks "→ Org" for a draft named "Acme Corp"
- **THEN** the form shows `name="Acme Corp"` and `notes` pre-filled from quick_notes

#### Scenario: Org type required
- **WHEN** the user submits the Org form without selecting an org type
- **THEN** validation prevents submission (org type is required)

#### Scenario: Inline org type creation
- **WHEN** the user types a new org type name in the TypeaheadSelect
- **THEN** an inline creation option appears, matching the existing Orgs page behavior

### Requirement: Link to existing record
Clicking "Link to [Name]" on a match hint SHALL call the link API endpoint, skipping the promotion form entirely. On success, the draft is removed from the inbox list.

#### Scenario: Link to existing person
- **WHEN** the user clicks "Link to Jane Smith" on a person match hint
- **THEN** the draft is linked to the existing Person, quick notes are appended to the person's notes, and the draft is removed from the inbox list

#### Scenario: Link to existing org
- **WHEN** the user clicks "Link to Acme Corp" on an org match hint
- **THEN** the draft is linked to the existing Organization and removed from the inbox list

### Requirement: Dismiss action
Clicking "Dismiss" SHALL call the dismiss API endpoint and remove the draft from the inbox list. The next pending draft (if any) SHALL be auto-selected.

#### Scenario: Dismiss a draft
- **WHEN** the user clicks "Dismiss"
- **THEN** the draft is dismissed via API and removed from the list

#### Scenario: Dismiss last draft shows empty state
- **WHEN** the user dismisses the last pending draft
- **THEN** the inbox shows the empty state message
