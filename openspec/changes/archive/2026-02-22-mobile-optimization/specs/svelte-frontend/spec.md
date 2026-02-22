## MODIFIED Requirements

### Requirement: Three-panel layout shell
The system SHALL render a three-panel layout: left sidebar (list navigation), center panel (task list), and right panel (task detail). The panel widths SHALL be user-adjustable via draggable resize handles on desktop viewports. A top navigation bar SHALL provide links to Tasks, People, Organizations, Interactions, Relationships, Graph, Projects, and Timesheet pages. The navigation bar SHALL also include a settings cog button and a theme toggle control. The Import page SHALL NOT appear as a primary navigation tab; it SHALL be accessible via the settings dropdown menu. On phone viewports (640px and below), the app shell SHALL use `100dvh` (with `100vh` fallback) instead of `100vh` to account for mobile browser chrome resizing. All interactive elements in the navigation bar SHALL meet a 44px minimum touch target height on phone viewports.

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
- **THEN** a bottom tab bar shows navigation links for Tasks, People, Organizations, Interactions, Relationships, Graph, Projects, and Timesheet (Import is NOT included)

#### Scenario: Non-task routes hide task side panels
- **WHEN** the user navigates to People, Organizations, Interactions, Relationships, Graph, Projects, Timesheet, or Import routes
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

### Requirement: Task list rendering
The system SHALL display tasks within sections, showing title, tags, due date, subtask count, pin button, and a recurrence indicator. Completed tasks SHALL appear in a separate "Completed" group at the bottom. On phone viewports (640px and below), task row metadata SHALL wrap instead of overflowing, and interactive elements SHALL meet minimum touch target sizes.

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

### Requirement: Task detail panel
The system SHALL display a task's full details in the right panel when selected. All detail fields SHALL auto-save on blur. A recurrence editor SHALL be displayed below the due date field. A "Linked People & Orgs" section SHALL be displayed below the tags section. On phone viewports (640px and below), form elements and buttons SHALL be sized for touch interaction.

#### Scenario: Selecting a task shows detail
- **WHEN** the user clicks a task row
- **THEN** the right panel displays the task's title, notes, due date, priority, tags, parent link, recurrence settings, and linked people & organizations

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

### Requirement: Timesheet page
The system SHALL provide a dedicated page at `/timesheet` for weekly time tracking with navigation and summaries. On phone viewports (640px and below), the summary bar, entry form, week navigation, and entry rows SHALL wrap/stack to prevent horizontal overflow.

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

#### Scenario: Task selector by project
- **WHEN** the user selects a project in the time entry form
- **THEN** a task selector shows incomplete tasks from that project's linked lists

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
- **THEN** entry row content (project, time, description, delete button) wraps to fit without horizontal overflow

## ADDED Requirements

### Requirement: Upcoming dashboard phone layout
The system SHALL render the Upcoming dashboard without horizontal overflow on phone viewports (640px and below). Task location text SHALL be truncated with ellipsis when it exceeds available space.

#### Scenario: Phone viewport location text truncation
- **WHEN** the viewport is 640px or narrower and an upcoming task has a long location path (list name / section name)
- **THEN** the location text is truncated with ellipsis instead of overflowing or wrapping awkwardly

#### Scenario: Phone viewport upcoming task rows fit
- **WHEN** the viewport is 640px or narrower
- **THEN** upcoming task rows render without horizontal overflow, with metadata stacking if needed

### Requirement: Relationships page phone layout
The system SHALL render the Relationships page without text overflow on phone viewports (640px and below). Relationship titles SHALL be truncated with ellipsis and action buttons SHALL meet minimum touch target sizes.

#### Scenario: Phone viewport relationship title truncation
- **WHEN** the viewport is 640px or narrower and a relationship title (e.g., "Person A ↔ Person B") exceeds the card width
- **THEN** the title is truncated with ellipsis

#### Scenario: Phone viewport relationship action buttons are touch-sized
- **WHEN** the viewport is 640px or narrower
- **THEN** relationship card action buttons have a minimum touch target of 44px height
