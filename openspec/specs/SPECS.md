# ToDo App — Specification

## 1. Overview

A multi-list task management application built with **Django** and **HTMX**. The UI consists of three panels: a left sidebar for list navigation, a central area for task display, and a right sidebar for task detail editing. The app also includes dedicated pages for projects, timesheet tracking, and data import, accessible via a top navigation bar.

## 2. Tech Stack

- **Backend:** Django (Python 3.14)
- **Frontend interactivity:** HTMX + SortableJS (drag-and-drop)
- **Database:** SQLite (default Django)
- **Port:** 8000

## 3. Data Model

### 3.1 Project
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| name | CharField | Required, max 255 chars |
| description | TextField | Optional, defaults to empty |
| is_active | BooleanField | Default: True |
| position | IntegerField | For ordering projects |

### 3.2 List
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| name | CharField | Required, max 255 chars |
| emoji | CharField | Optional, max 10 chars |
| position | IntegerField | For ordering lists in the sidebar |
| project | ForeignKey(Project) | Optional (null=True), SET_NULL on delete. Links a list to a project. |

### 3.3 Section
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| list | ForeignKey(List) | Required, CASCADE on delete |
| name | CharField | Required, max 255 chars |
| emoji | CharField | Optional, max 10 chars |
| position | IntegerField | For ordering sections within a list |

### 3.4 Task
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| section | ForeignKey(Section) | Required, CASCADE on delete |
| parent | ForeignKey(self) | Optional (null=True), CASCADE on delete. Enables arbitrary nesting. |
| title | CharField | Required, max 500 chars |
| notes | TextField | Optional, stored as Markdown |
| priority | IntegerField | Choices: None (0), Low (1), Medium (3), High (5). Default: None. |
| due_date | DateField | Optional |
| due_time | TimeField | Optional |
| is_completed | BooleanField | Default: False |
| completed_at | DateTimeField | Optional, set when completed |
| created_at | DateTimeField | Auto-set to now on creation |
| position | IntegerField | For ordering tasks within a section/parent |
| external_id | CharField | Optional, unique, max 100 chars. Used for tracking imported tasks. |
| tags | ManyToManyField(Tag) | Optional |
| is_pinned | BooleanField | Default: False |

### 3.5 Tag
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| name | CharField | Required, unique, max 100 chars |

### 3.6 TimeEntry
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| project | ForeignKey(Project) | Required, CASCADE on delete |
| tasks | ManyToManyField(Task) | Optional. Links time entry to specific tasks. |
| description | CharField | Optional, max 500 chars |
| date | DateField | Required |
| created_at | DateTimeField | Auto-set on creation |

Each TimeEntry represents one hour of work.

## 4. Functional Requirements

### FR-1: List Management
- **FR-1.1:** User can create a new list with a name and optional emoji.
- **FR-1.2:** User can rename a list.
- **FR-1.3:** User can change or remove a list's emoji.
- **FR-1.4:** User can delete a list (deletes all sections and tasks within it).
- **FR-1.5:** Lists are displayed in the left sidebar, ordered by position.
- **FR-1.6:** Selecting a list displays its sections and tasks in the central panel.
- **FR-1.7:** User can double-click a list in the sidebar to edit its name and emoji inline. Enter or emoji selection saves; Escape cancels; clicking away saves.
- **FR-1.8:** An emoji picker modal provides a searchable grid of emojis across categories. Click-away or Escape closes it. Available for lists and sections.
- **FR-1.9:** User can assign a list to a project via a dropdown in the list header.

### FR-2: Section Management
- **FR-2.1:** User can create a section within a list, with a name and optional emoji.
- **FR-2.2:** User can rename a section.
- **FR-2.3:** User can change or remove a section's emoji.
- **FR-2.4:** User can delete a section (deletes all tasks within it).
- **FR-2.5:** Sections are displayed in order within their parent list.
- **FR-2.6:** Sections are collapsible via `<details>` elements (open by default).
- **FR-2.7:** A "Collapse All" / "Expand All" toggle in the list header collapses or expands all sections at once.

### FR-3: Task Management
- **FR-3.1:** User can create a task within a section.
- **FR-3.2:** User can create a subtask under any existing task (arbitrary depth nesting).
- **FR-3.3:** User can edit a task's title inline.
- **FR-3.4:** User can delete a task (deletes all subtasks recursively).
- **FR-3.5:** Tasks are displayed in order within their section or parent task.
- **FR-3.6:** Task tags are displayed as badges on the task row in the center panel.
- **FR-3.7:** Task due date is displayed in abbreviated format (e.g., "Mar 15") on the task row in the center panel.
- **FR-3.8:** Parent tasks display a subtask count label (e.g., "3 subtasks — 1 open") that updates dynamically.
- **FR-3.9:** Subtask lists are collapsible via `<details>` elements (open by default). Completed subtasks are grouped under a collapsible "Done" subsection.

### FR-4: Task Detail Editing (Right Sidebar)
- **FR-4.1:** Selecting a task opens its details in the right sidebar.
- **FR-4.2:** User can edit the task's Markdown notes. Notes are saved and rendered as HTML.
- **FR-4.3:** User can set, change, or clear a due date.
- **FR-4.4:** User can add or remove tags from a task.
- **FR-4.5:** Links within rendered notes and task content are automatically highlighted and clickable (`<a>` tags with `target="_blank"`).
- **FR-4.6:** A live Markdown editor replaces the plain textarea. Inactive blocks show rendered HTML; the active block shows raw Markdown. Supports headings, bold, italic, strikethrough, inline code, lists, blockquotes, code fences, and horizontal rules.
- **FR-4.7:** Detail fields (title, due date, notes) auto-save on blur — no Save button required. The server responds with OOB swaps to update the detail heading and center panel task row without re-rendering the full detail panel.
- **FR-4.8:** Adding or removing a tag immediately updates the center panel task row via an HTMX OOB swap.
- **FR-4.9:** The tag input offers autocomplete suggestions via an HTML5 `<datalist>` populated with existing tags not already assigned to the current task.
- **FR-4.10:** When viewing a subtask, the detail panel shows a link to the parent task with a "jump to" button.

### FR-5: Task Completion
- **FR-5.1:** User can mark a task as complete.
- **FR-5.2:** Completing a task moves it to a "Completed" section at the bottom of the current section/list view.
- **FR-5.3:** Upon completion, a non-intrusive pop-up (toast) appears offering to undo. The toast auto-dismisses after 5 seconds.
- **FR-5.4:** User can undo completion via the toast within 5 seconds.
- **FR-5.5:** User can un-complete any completed task at any time (not just via the toast).
- **FR-5.6:** Completing a parent task cascades completion to all non-completed subtasks. Each subtask's `is_completed` and `completed_at` are set recursively.
- **FR-5.7:** Completion uses a CSS fade-out animation (180ms). The task is optimistically removed from the active list and moved to the "Completed" section after animation completes.

### FR-6: HTMX Interactivity
- **FR-6.1:** All CRUD operations use HTMX for partial page updates (no full-page reloads).
- **FR-6.2:** The undo toast is rendered via HTMX swap and dismissed via client-side timer. Multiple toasts are supported in a toast container.
- **FR-6.3:** After an HTMX swap, focus is restored to the previously focused input so the user can continue editing without re-clicking.

### FR-7: Drag-and-Drop
- **FR-7.1:** User can drag a task to reorder it within its current section.
- **FR-7.2:** User can drag a task into a different section within the same list.
- **FR-7.3:** User can drag a task onto another task to make it a subtask of that task.
- **FR-7.4:** User can drag a subtask out of its parent to promote it to a top-level task in the section.
- **FR-7.5:** User can drag a task to a different list (via the left sidebar). The task moves to the target list's first section.
- **FR-7.6:** When a task is moved, all its subtasks move with it.
- **FR-7.7:** After a drop, the `position`, `section`, `parent`, and/or list assignment are updated on the server via an HTMX request.
- **FR-7.8:** Drag-and-drop uses SortableJS for the client-side interaction.
- **FR-7.9:** Drag-and-drop and keyboard indent/outdent use optimistic DOM updates — the UI moves the task immediately, and the server persists the change silently in the background.
- **FR-7.10:** The server prevents circular nesting (a task cannot become a subtask of itself or any of its descendants).
- **FR-7.11:** User can drag lists in the sidebar to reorder them.
- **FR-7.12:** User can drag sections within a list to reorder them.

### FR-8: Export
- **FR-8.1:** User can export a single list or all lists.
- **FR-8.2:** Supported export formats: JSON, CSV, and Markdown.
- **FR-8.3:** Export is triggered via a download button accessible from the list view (single list) and from the sidebar header (all lists).
- **FR-8.4:** JSON export preserves the full hierarchy: lists > sections > tasks > subtasks (nested). Includes all fields: title, notes, due date, tags, completion status, and position.
- **FR-8.5:** CSV export flattens tasks to one row per task. Columns: `list`, `section`, `task`, `parent_task` (title of parent or blank), `depth`, `notes`, `due_date`, `tags` (comma-separated), `is_completed`.
- **FR-8.6:** Markdown export renders a human-readable document: list name as `#`, sections as `##`, tasks as checkbox lists (`- [ ]` / `- [x]`) with indentation for subtask depth. Notes, due dates, and tags are included inline beneath each task.
- **FR-8.7:** Export response sets `Content-Disposition: attachment` with a filename based on the list name (or `all-lists`) and format extension.
- **FR-8.8:** Export of an empty list returns a valid file with only the list/section headers and no tasks.

### FR-9: Keyboard Navigation
- **FR-9.1:** User can navigate between non-completed tasks using Arrow Up/Down or j/k keys.
- **FR-9.2:** User can indent a focused task (make it a subtask of the previous task) using Tab, and outdent using Shift+Tab.
- **FR-9.3:** User can mark the focused task as complete using the x key.
- **FR-9.4:** User can clear task selection using Escape.
- **FR-9.5:** Clicking a task row highlights it and loads its detail panel. Clicking outside any task row (sidebar, detail panel, empty area) clears the highlight.
- **FR-9.6:** The focused task scrolls into view automatically.
- **FR-9.7:** User can jump to the next section using Ctrl+Arrow Down, and to the previous section using Ctrl+Arrow Up.
- **FR-9.8:** User can delete the focused task using the Delete key (shows confirmation dialog).
- **FR-9.9:** Arrow Up/Down keys work within add-task inputs to navigate to tasks or adjacent section inputs.
- **FR-9.10:** Ctrl+Arrow Left/Right cycles through lists/pages in the sidebar navigation.
- **FR-9.11:** Keyboard navigation respects collapsed sections — tasks inside collapsed `<details>` are skipped.

### FR-10: Task Pinning
- **FR-10.1:** User can pin a task to keep it at the top of the list in a "Pinned" section.
- **FR-10.2:** Maximum of 3 pinned tasks per list.
- **FR-10.3:** Pinning is toggled via a pin button on the task row (not shown on completed tasks).
- **FR-10.4:** Pinned tasks appear in a compact view without subtask details.
- **FR-10.5:** Clicking a pinned task in the pinned section jumps to the task's actual location in the list (with a flash animation).
- **FR-10.6:** The pinned section is hidden when no tasks are pinned.
- **FR-10.7:** Pin state is toggled via `POST /tasks/<id>/pin/` and updates the UI with targeted OOB swaps.

### FR-11: Search
- **FR-11.1:** A global search bar in the navigation bar searches across all lists.
- **FR-11.2:** Search matches task titles, notes, and tag names (case-insensitive).
- **FR-11.3:** Search is debounced (300ms delay) and triggered on keyup via HTMX.
- **FR-11.4:** Results are displayed in a dropdown, grouped by list, showing task title, section name, and tags.
- **FR-11.5:** Clicking a search result navigates to that task's list and loads its detail panel.
- **FR-11.6:** Results close when clicking outside the search area.

### FR-12: Projects
- **FR-12.1:** User can create a project with a name and optional description.
- **FR-12.2:** User can rename a project or update its description.
- **FR-12.3:** User can delete a project (lists linked to it are unlinked, not deleted).
- **FR-12.4:** User can toggle a project's active/inactive status.
- **FR-12.5:** The projects page displays project cards with metrics: total hours logged, number of linked lists, total tasks, and completed tasks.
- **FR-12.6:** Projects are ordered by position.
- **FR-12.7:** Projects are accessible via a dedicated `/projects/` page linked from the navigation bar.

### FR-13: Timesheet
- **FR-13.1:** User can log time entries, each representing one hour of work.
- **FR-13.2:** A time entry is linked to a project and optionally to specific tasks from that project's lists.
- **FR-13.3:** User can set a date and optional description on each time entry.
- **FR-13.4:** The timesheet page shows a weekly view with navigation to previous/next weeks.
- **FR-13.5:** A summary bar shows total hours and per-project hour breakdowns for the current week.
- **FR-13.6:** Entries are grouped by date within the week view.
- **FR-13.7:** User can delete individual time entries.
- **FR-13.8:** A task selector fetches incomplete tasks for the selected project's linked lists.
- **FR-13.9:** Timesheet is accessible via a dedicated `/timesheet/` page linked from the navigation bar.

### FR-14: Import
- **FR-14.1:** User can import tasks from a TickTick CSV export.
- **FR-14.2:** Import creates lists, sections, tasks, and tags as needed from the CSV data.
- **FR-14.3:** Import uses `external_id` for duplicate detection, making re-imports safe (existing tasks are skipped).
- **FR-14.4:** After import, a summary shows counts of tasks created/skipped, lists/sections/tags created, parent links resolved, and any errors.
- **FR-14.5:** Import runs in an atomic transaction — all or nothing on failure.
- **FR-14.6:** Only `.csv` files are accepted; other formats return an error.
- **FR-14.7:** Import is accessible via a dedicated `/import/` page linked from the navigation bar.

### FR-15: UI Layout and Responsiveness
- **FR-15.1:** The app uses a three-panel layout: left sidebar (list navigation), center (task list), right (task detail). A top navigation bar provides links to Tasks, Projects, Timesheet, and Import pages.
- **FR-15.2:** On screens narrower than 1024px, the layout collapses: the sidebar is hidden behind a hamburger menu, and the detail panel slides in as an overlay.
- **FR-15.3:** A bottom tab bar mirrors the navigation links on mobile.
- **FR-15.4:** When no list is selected, the center panel shows an empty state: "Select or create a list."
- **FR-15.5:** When no task is selected, the detail panel shows an empty state: "Select a task to view details."
- **FR-15.6:** The app registers a service worker and includes a web app manifest for PWA support (installable on mobile via "Add to Home Screen").

## 5. Non-Functional Requirements

- **NFR-1:** The app runs on port 8000.
- **NFR-2:** All task/section/list ordering uses a `position` field to allow reordering.
- **NFR-3:** No user authentication required (single-user app).
- **NFR-4:** Markdown rendering must sanitize HTML to prevent XSS.
- **NFR-5:** Drag-and-drop, task creation, and detail edits use optimistic/OOB updates for a flicker-free experience.
- **NFR-6:** Core task operations (navigate, complete, indent/outdent) are fully accessible via keyboard.
- **NFR-7:** The app is installable as a PWA with service worker caching for static assets.

## 6. Test Requirements

All tests use Django's built-in test framework (`django.test`).

### 6.1 Model Tests

| Test ID | Requirement | Description |
|---------|-------------|-------------|
| T-M-1 | FR-1.1 | Creating a List with name and emoji persists correctly |
| T-M-2 | FR-1.1 | Creating a List without emoji succeeds (emoji is optional) |
| T-M-3 | FR-1.4 | Deleting a List cascades to its Sections and Tasks |
| T-M-4 | FR-2.1 | Creating a Section linked to a List persists correctly |
| T-M-5 | FR-2.4 | Deleting a Section cascades to its Tasks |
| T-M-6 | FR-3.1 | Creating a Task within a Section persists correctly |
| T-M-7 | FR-3.2 | Creating nested subtasks (3+ levels) persists parent chain |
| T-M-8 | FR-3.4 | Deleting a parent Task cascades to all subtasks |
| T-M-9 | FR-4.4 | Adding/removing Tags on a Task via M2M works correctly |
| T-M-10 | FR-5.1 | Marking a task complete sets `is_completed=True` and `completed_at` |
| T-M-11 | FR-5.5 | Un-completing a task sets `is_completed=False` and clears `completed_at` |
| T-M-12 | FR-5.6 | Completing a parent cascades completion to all non-completed subtasks |
| T-M-13 | FR-7.2 | Moving a task to a different section updates its `section` FK |
| T-M-14 | FR-7.3 | Setting a task's `parent` makes it a subtask and preserves its data |
| T-M-15 | FR-7.4 | Clearing a task's `parent` promotes it to a top-level task |
| T-M-16 | FR-7.6 | Moving a parent task preserves all subtask relationships |
| T-M-17 | FR-8.4 | Serializing a list to JSON produces correct nested hierarchy |
| T-M-18 | FR-8.5 | Serializing tasks to CSV rows includes correct parent and depth values |
| T-M-19 | FR-10.2 | Pinning a task sets `is_pinned=True`; max 3 per list enforced |
| T-M-20 | FR-12.1 | Creating a Project with name and description persists correctly |
| T-M-21 | FR-12.3 | Deleting a Project sets linked Lists' `project` FK to null (SET_NULL) |
| T-M-22 | FR-13.1 | Creating a TimeEntry linked to a Project persists correctly |
| T-M-23 | FR-3.4, 3.8 | `open_subtask_count` property returns correct count of non-completed direct subtasks |

### 6.2 View / API Tests

| Test ID | Requirement | Description |
|---------|-------------|-------------|
| T-V-1 | FR-1.1 | POST to create list returns success and list appears in sidebar |
| T-V-2 | FR-1.2 | PATCH/PUT to rename list updates name |
| T-V-3 | FR-1.4 | DELETE list returns success and list is removed |
| T-V-4 | FR-1.6 | GET list detail returns its sections and tasks |
| T-V-5 | FR-2.1 | POST to create section within a list succeeds |
| T-V-6 | FR-2.4 | DELETE section returns success |
| T-V-7 | FR-3.1 | POST to create task within a section succeeds |
| T-V-8 | FR-3.2 | POST to create subtask with parent ID succeeds |
| T-V-9 | FR-3.3 | PATCH to update task title succeeds |
| T-V-10 | FR-3.4 | DELETE task removes it and its subtasks |
| T-V-11 | FR-4.2 | PATCH to update task notes saves Markdown content |
| T-V-12 | FR-4.3 | PATCH to set/clear due date succeeds |
| T-V-13 | FR-4.5 | Rendered notes contain clickable `<a>` tags for URLs |
| T-V-14 | FR-5.1 | POST to complete task returns updated task in "Completed" section |
| T-V-15 | FR-5.3 | Complete task response includes undo toast HTML fragment |
| T-V-16 | FR-5.4 | POST to undo completion within window reverts task status |
| T-V-17 | FR-5.5 | POST to un-complete a task at any time succeeds |
| T-V-18 | FR-7.1 | PATCH to reorder task within section updates positions |
| T-V-19 | FR-7.2 | PATCH to move task to different section updates section FK and position |
| T-V-20 | FR-7.3 | PATCH to nest task under a parent sets parent FK |
| T-V-21 | FR-7.4 | PATCH to promote subtask clears parent FK |
| T-V-22 | FR-7.5 | PATCH to move task to different list updates section to target list's first section |
| T-V-23 | FR-7.5 | Moving task to a list with no sections returns an error |
| T-V-24 | FR-7.6 | Moving a parent task — subtasks remain attached (section FKs updated) |
| T-V-25 | FR-8.1 | GET export for a single list returns a downloadable file |
| T-V-26 | FR-8.1 | GET export for all lists returns a downloadable file |
| T-V-27 | FR-8.4 | JSON export contains nested lists > sections > tasks > subtasks |
| T-V-28 | FR-8.5 | CSV export contains one row per task with correct columns and flattened parent/depth |
| T-V-29 | FR-8.6 | Markdown export contains headings, checkbox syntax, and indented subtasks |
| T-V-30 | FR-8.7 | Export response has `Content-Disposition: attachment` with correct filename |
| T-V-31 | FR-8.8 | Exporting an empty list returns a valid file with headers only |
| T-V-32 | FR-8.2 | Requesting an unsupported export format returns 400 error |
| T-V-33 | FR-10.1 | POST to pin a task sets `is_pinned=True` and returns updated pinned section |
| T-V-34 | FR-10.2 | Pinning a 4th task in a list returns an error (max 3 enforced) |
| T-V-35 | FR-11.1 | GET search with query returns matching tasks grouped by list |
| T-V-36 | FR-11.2 | Search matches on title, notes, and tag names |
| T-V-37 | FR-12.1 | POST to create project returns success |
| T-V-38 | FR-12.2 | POST to update project name/description succeeds |
| T-V-39 | FR-12.3 | DELETE project removes it and unlinks lists |
| T-V-40 | FR-12.4 | POST to toggle project active status flips `is_active` |
| T-V-41 | FR-13.1 | POST to create time entry linked to a project succeeds |
| T-V-42 | FR-13.7 | DELETE time entry removes it |
| T-V-43 | FR-14.1 | POST CSV upload creates tasks, lists, sections, and tags |
| T-V-44 | FR-14.3 | Re-importing the same CSV skips duplicates (external_id dedup) |
| T-V-45 | FR-14.6 | Uploading a non-CSV file returns an error |

### 6.3 Integration / UI Behavior Tests

| Test ID | Requirement | Description |
|---------|-------------|-------------|
| T-I-1 | FR-6.1 | HTMX requests return partial HTML fragments (not full pages) |
| T-I-2 | FR-4.1 | Clicking a task returns right-sidebar HTML with task details |
| T-I-3 | FR-5.2 | Completed tasks appear under a "Completed" heading in the response |
| T-I-4 | FR-5.3 | Undo toast fragment contains a 5-second auto-dismiss mechanism |
| T-I-5 | NFR-4 | Markdown rendering strips dangerous HTML (script tags, event handlers) |
| T-I-6 | FR-7.7 | Drop event triggers HTMX request and server responds with updated partial |
| T-I-7 | FR-7.3 | Dropping a task onto another task indents it as a subtask in the response |
| T-I-8 | FR-7.5 | Dropping a task on a list in the sidebar moves it and re-renders both lists |
| T-I-9 | FR-8.3 | Export button on list view triggers file download (Content-Disposition header present) |
| T-I-10 | FR-8.4 | JSON export of a list with nested subtasks is valid JSON and round-trippable |
| T-I-11 | FR-8.6 | Markdown export of completed tasks uses `[x]` checkbox syntax |
| T-I-12 | FR-10.7 | Pinning a task updates the pinned section via OOB swap |
| T-I-13 | FR-11.3 | Search input triggers debounced HTMX request and returns results partial |
| T-I-14 | FR-15.4 | Center panel shows empty state when no list is selected |
| T-I-15 | FR-15.5 | Detail panel shows empty state when no task is selected |
