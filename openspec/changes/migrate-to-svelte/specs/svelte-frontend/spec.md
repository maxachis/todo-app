## ADDED Requirements

### Requirement: SvelteKit application with static adapter
The system SHALL use SvelteKit with `adapter-static` to produce a static SPA build. The build output SHALL be plain HTML, JS, and CSS files requiring no Node.js runtime in production. The frontend SHALL be served by Nginx, with API requests proxied to Django.

#### Scenario: Static build produces deployable output
- **WHEN** the developer runs the SvelteKit build command
- **THEN** the output directory contains static HTML, JS, and CSS files that can be served by any web server

#### Scenario: Frontend loads without server-side rendering
- **WHEN** a user navigates to the app root
- **THEN** the SPA loads and fetches data from the Django API via client-side requests

### Requirement: Three-panel layout shell
The system SHALL render a three-panel layout: left sidebar (list navigation), center panel (task list), and right panel (task detail). A top navigation bar SHALL provide links to Tasks, Projects, Timesheet, and Import pages.

#### Scenario: Desktop layout shows all three panels
- **WHEN** the viewport is wider than 1024px
- **THEN** the sidebar, center panel, and detail panel are all visible simultaneously

#### Scenario: Mobile layout collapses panels
- **WHEN** the viewport is narrower than 1024px
- **THEN** the sidebar is hidden behind a hamburger menu, and the detail panel slides in as an overlay

#### Scenario: Bottom tab bar on mobile
- **WHEN** the viewport is narrower than 1024px
- **THEN** a bottom tab bar shows navigation links for Tasks, Projects, Timesheet, and Import

### Requirement: List sidebar navigation
The system SHALL display all lists in the sidebar, ordered by position. Selecting a list SHALL load its content in the center panel.

#### Scenario: Sidebar displays lists
- **WHEN** the app loads
- **THEN** the sidebar shows all lists with their emoji and name, ordered by position

#### Scenario: Selecting a list loads its content
- **WHEN** the user clicks a list in the sidebar
- **THEN** the center panel displays that list's sections and tasks

#### Scenario: Empty state when no list selected
- **WHEN** no list is selected
- **THEN** the center panel shows "Select or create a list"

#### Scenario: Inline list editing
- **WHEN** the user double-clicks a list in the sidebar
- **THEN** the list name and emoji become editable inline; Enter or emoji selection saves, Escape cancels

#### Scenario: Drag to reorder lists
- **WHEN** the user drags a list to a new position in the sidebar
- **THEN** the list order updates immediately and persists via API

### Requirement: Section display and management
The system SHALL display sections within a list, each collapsible, with tasks nested inside.

#### Scenario: Sections render in order
- **WHEN** a list is loaded
- **THEN** its sections display in position order, each showing its emoji and name

#### Scenario: Sections are collapsible
- **WHEN** the user clicks a section's collapse toggle
- **THEN** the section's tasks are hidden/shown

#### Scenario: Collapse all / expand all
- **WHEN** the user clicks the "Collapse All" toggle in the list header
- **THEN** all sections collapse; clicking again expands all

#### Scenario: Drag to reorder sections
- **WHEN** the user drags a section to a new position within the list
- **THEN** the section order updates immediately and persists via API

### Requirement: Task list rendering
The system SHALL display tasks within sections, showing title, tags, due date, subtask count, and pin button. Completed tasks SHALL appear in a separate "Completed" group at the bottom.

#### Scenario: Tasks render with metadata
- **WHEN** a section is displayed
- **THEN** each task row shows its title, tag badges, abbreviated due date, and subtask count label

#### Scenario: Completed tasks grouped separately
- **WHEN** a section contains completed tasks
- **THEN** completed tasks appear under a collapsible "Completed" subsection

#### Scenario: Subtask count label
- **WHEN** a task has subtasks
- **THEN** the task row displays a label like "3 subtasks — 1 open" that updates reactively

#### Scenario: Subtask nesting display
- **WHEN** a task has subtasks
- **THEN** subtasks are rendered nested below the parent with visual indentation, collapsible via a toggle

### Requirement: Task detail panel
The system SHALL display a task's full details in the right panel when selected. All detail fields SHALL auto-save on blur.

#### Scenario: Selecting a task shows detail
- **WHEN** the user clicks a task row
- **THEN** the right panel displays the task's title, notes, due date, priority, tags, and parent link

#### Scenario: Auto-save on blur
- **WHEN** the user edits the title, due date, or notes and then blurs the field
- **THEN** the change is saved to the API and the center panel task row updates reactively

#### Scenario: Empty state when no task selected
- **WHEN** no task is selected
- **THEN** the detail panel shows "Select a task to view details"

#### Scenario: Parent task link
- **WHEN** viewing a subtask's detail
- **THEN** a link to the parent task is shown with a "jump to" action that scrolls to and highlights the parent in the center panel

### Requirement: Live Markdown editor
The system SHALL provide a block-based Markdown editor for task notes. Inactive blocks SHALL show rendered HTML; the active block SHALL show raw Markdown.

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

### Requirement: Task completion with optimistic UI
The system SHALL provide task completion with immediate visual feedback. Completing a parent SHALL cascade to non-completed subtasks.

#### Scenario: Complete a task with animation
- **WHEN** the user checks a task's completion checkbox
- **THEN** the task fades out (180ms), moves to the "Completed" section, and a toast appears offering undo

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
The system SHALL use svelte-dnd-action for all drag-and-drop interactions. Drop events SHALL update the Svelte store optimistically, then persist via API.

#### Scenario: Reorder task within section
- **WHEN** the user drags a task to a new position within the same section
- **THEN** the task list reorders immediately and the new position persists via API

#### Scenario: Move task to different section
- **WHEN** the user drags a task into a different section
- **THEN** the task appears in the new section immediately and the section/position change persists

#### Scenario: Nest task as subtask
- **WHEN** the user drags a task onto another task
- **THEN** the dragged task becomes a subtask of the drop target, updating visually and persisting via API

#### Scenario: Promote subtask
- **WHEN** the user drags a subtask out of its parent's nesting area
- **THEN** the subtask becomes a top-level task in the section

#### Scenario: Move task to different list via sidebar
- **WHEN** the user drags a task onto a list in the sidebar
- **THEN** the task moves to the first section of that list, with all subtasks following

#### Scenario: API failure rolls back
- **WHEN** a drag operation succeeds visually but the API call fails
- **THEN** the store reverts to the pre-drag state and a toast shows an error message

### Requirement: Keyboard navigation
The system SHALL support full keyboard navigation for tasks. Navigation state SHALL be managed in a Svelte store.

#### Scenario: Arrow key navigation
- **WHEN** the user presses Arrow Up or Arrow Down (or j/k)
- **THEN** the focus moves to the previous/next non-completed task, scrolling into view

#### Scenario: Tab indent / Shift+Tab outdent
- **WHEN** the user presses Tab on a focused task
- **THEN** the task becomes a subtask of the previous sibling; Shift+Tab promotes it

#### Scenario: Complete with x key
- **WHEN** the user presses x on a focused task
- **THEN** the task is completed (same behavior as clicking the checkbox)

#### Scenario: Delete with Delete key
- **WHEN** the user presses Delete on a focused task
- **THEN** a confirmation dialog appears; confirming deletes the task

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

#### Scenario: Select emoji
- **WHEN** the user clicks an emoji in the picker
- **THEN** the emoji is applied to the list/section and the picker closes

#### Scenario: Close picker
- **WHEN** the user presses Escape or clicks outside the picker
- **THEN** the picker closes without changing the emoji

### Requirement: Search across all lists
The system SHALL provide a global search bar that queries the API with debounced input.

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

### Requirement: Export UI
The system SHALL provide export buttons that trigger file downloads from the API.

#### Scenario: Export single list
- **WHEN** the user clicks an export button on a list and selects a format
- **THEN** the browser downloads the exported file

#### Scenario: Export all lists
- **WHEN** the user clicks the "Export All" button in the sidebar header
- **THEN** the browser downloads a file containing all lists in the selected format

### Requirement: Projects page
The system SHALL provide a dedicated page at `/projects` for project management with CRUD operations and metrics display.

#### Scenario: Projects page displays cards
- **WHEN** the user navigates to `/projects`
- **THEN** the page shows project cards ordered by position, each displaying name, description, total hours, linked lists count, total tasks, and completed tasks

#### Scenario: Create project
- **WHEN** the user fills in the create project form and submits
- **THEN** the project is created and appears in the list

#### Scenario: Toggle project active status
- **WHEN** the user clicks the active/inactive toggle on a project card
- **THEN** the project's status flips and the UI updates

### Requirement: Timesheet page
The system SHALL provide a dedicated page at `/timesheet` for weekly time tracking with navigation and summaries.

#### Scenario: Weekly view with navigation
- **WHEN** the user navigates to `/timesheet`
- **THEN** the page shows the current week's time entries with previous/next week navigation

#### Scenario: Summary bar
- **WHEN** viewing a week's timesheet
- **THEN** a summary bar shows total hours and per-project breakdowns

#### Scenario: Create time entry
- **WHEN** the user fills in the time entry form (project, date, description, optional tasks) and submits
- **THEN** the entry is created and appears in the appropriate date group

#### Scenario: Task selector by project
- **WHEN** the user selects a project in the time entry form
- **THEN** a task selector shows incomplete tasks from that project's linked lists

### Requirement: Import page
The system SHALL provide a dedicated page at `/import` for importing tasks from TickTick CSV files.

#### Scenario: Upload CSV
- **WHEN** the user selects a CSV file and submits the import form
- **THEN** the file is uploaded to the API and a summary shows counts of created/skipped entities

#### Scenario: Import error display
- **WHEN** the import fails (invalid file, parse error)
- **THEN** the error message is displayed to the user

### Requirement: Svelte store state management
The system SHALL manage application state using Svelte writable stores, one per resource type, with co-located async mutation functions.

#### Scenario: Store updates propagate to all subscribers
- **WHEN** a task is completed via the store's `completeTask()` function
- **THEN** all components subscribed to the tasks store re-render with the updated state

#### Scenario: Optimistic updates with rollback
- **WHEN** a mutation function updates the store optimistically and the API call fails
- **THEN** the store reverts to the previous state and a toast shows the error

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
