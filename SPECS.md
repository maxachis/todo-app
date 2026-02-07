# ToDo App — Specification

## 1. Overview

A multi-list task management application built with **Django** and **HTMX**. The UI consists of three panels: a left sidebar for list navigation, a central area for task display, and a right sidebar for task detail editing.

## 2. Tech Stack

- **Backend:** Django (Python 3.14)
- **Frontend interactivity:** HTMX + SortableJS (drag-and-drop)
- **Database:** SQLite (default Django)
- **Port:** 8000

## 3. Data Model

### 3.1 List
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| name | CharField | Required, max 255 chars |
| emoji | CharField | Optional, max 10 chars |
| position | IntegerField | For ordering lists in the sidebar |

### 3.2 Section
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| list | ForeignKey(List) | Required, CASCADE on delete |
| name | CharField | Required, max 255 chars |
| emoji | CharField | Optional, max 10 chars |
| position | IntegerField | For ordering sections within a list |

### 3.3 Task
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| section | ForeignKey(Section) | Required, CASCADE on delete |
| parent | ForeignKey(self) | Optional (null=True), CASCADE on delete. Enables arbitrary nesting. |
| title | CharField | Required, max 500 chars |
| notes | TextField | Optional, stored as Markdown |
| due_date | DateField | Optional |
| is_completed | BooleanField | Default: False |
| completed_at | DateTimeField | Optional, set when completed |
| position | IntegerField | For ordering tasks within a section/parent |

### 3.4 Tag
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| name | CharField | Required, unique, max 100 chars |

### 3.5 TaskTag (M2M through or Django's ManyToManyField)
- Links Task ↔ Tag.

## 4. Functional Requirements

### FR-1: List Management
- **FR-1.1:** User can create a new list with a name and optional emoji.
- **FR-1.2:** User can rename a list.
- **FR-1.3:** User can change or remove a list's emoji.
- **FR-1.4:** User can delete a list (deletes all sections and tasks within it).
- **FR-1.5:** Lists are displayed in the left sidebar, ordered by position.
- **FR-1.6:** Selecting a list displays its sections and tasks in the central panel.

### FR-2: Section Management
- **FR-2.1:** User can create a section within a list, with a name and optional emoji.
- **FR-2.2:** User can rename a section.
- **FR-2.3:** User can change or remove a section's emoji.
- **FR-2.4:** User can delete a section (deletes all tasks within it).
- **FR-2.5:** Sections are displayed in order within their parent list.

### FR-3: Task Management
- **FR-3.1:** User can create a task within a section.
- **FR-3.2:** User can create a subtask under any existing task (arbitrary depth nesting).
- **FR-3.3:** User can edit a task's title inline.
- **FR-3.4:** User can delete a task (deletes all subtasks recursively).
- **FR-3.5:** Tasks are displayed in order within their section or parent task.

### FR-4: Task Detail Editing (Right Sidebar)
- **FR-4.1:** Selecting a task opens its details in the right sidebar.
- **FR-4.2:** User can edit the task's Markdown notes. Notes are saved and rendered as HTML.
- **FR-4.3:** User can set, change, or clear a due date.
- **FR-4.4:** User can add or remove tags from a task.
- **FR-4.5:** Links within rendered notes and task content are automatically highlighted and clickable (`<a>` tags with `target="_blank"`).

### FR-5: Task Completion
- **FR-5.1:** User can mark a task as complete.
- **FR-5.2:** Completing a task moves it to a "Completed" section at the bottom of the current section/list view.
- **FR-5.3:** Upon completion, a non-intrusive pop-up (toast) appears offering to undo. The toast auto-dismisses after 5 seconds.
- **FR-5.4:** User can undo completion via the toast within 5 seconds.
- **FR-5.5:** User can un-complete any completed task at any time (not just via the toast).
- **FR-5.6:** Completing a parent task does NOT automatically complete its subtasks (subtasks retain their own status).

### FR-6: HTMX Interactivity
- **FR-6.1:** All CRUD operations use HTMX for partial page updates (no full-page reloads).
- **FR-6.2:** The undo toast is rendered via HTMX swap and dismissed via client-side timer.

### FR-7: Drag-and-Drop
- **FR-7.1:** User can drag a task to reorder it within its current section.
- **FR-7.2:** User can drag a task into a different section within the same list.
- **FR-7.3:** User can drag a task onto another task to make it a subtask of that task.
- **FR-7.4:** User can drag a subtask out of its parent to promote it to a top-level task in the section.
- **FR-7.5:** User can drag a task to a different list (via the left sidebar). The task moves to the target list's first section.
- **FR-7.6:** When a task is moved, all its subtasks move with it.
- **FR-7.7:** After a drop, the `position`, `section`, `parent`, and/or list assignment are updated on the server via an HTMX request.
- **FR-7.8:** Drag-and-drop uses SortableJS for the client-side interaction.

### FR-8: Export
- **FR-8.1:** User can export a single list or all lists.
- **FR-8.2:** Supported export formats: JSON, CSV, and Markdown.
- **FR-8.3:** Export is triggered via a download button accessible from the list view (single list) and from the sidebar header (all lists).
- **FR-8.4:** JSON export preserves the full hierarchy: lists > sections > tasks > subtasks (nested). Includes all fields: title, notes, due date, tags, completion status, and position.
- **FR-8.5:** CSV export flattens tasks to one row per task. Columns: `list`, `section`, `task`, `parent_task` (title of parent or blank), `depth`, `notes`, `due_date`, `tags` (comma-separated), `is_completed`.
- **FR-8.6:** Markdown export renders a human-readable document: list name as `#`, sections as `##`, tasks as checkbox lists (`- [ ]` / `- [x]`) with indentation for subtask depth. Notes, due dates, and tags are included inline beneath each task.
- **FR-8.7:** Export response sets `Content-Disposition: attachment` with a filename based on the list name (or `all-lists`) and format extension.
- **FR-8.8:** Export of an empty list returns a valid file with only the list/section headers and no tasks.

## 5. Non-Functional Requirements

- **NFR-1:** The app runs on port 8000.
- **NFR-2:** All task/section/list ordering uses a `position` field to allow reordering.
- **NFR-3:** No user authentication required (single-user app).
- **NFR-4:** Markdown rendering must sanitize HTML to prevent XSS.

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
| T-M-12 | FR-5.6 | Completing a parent does not cascade completion to subtasks |
| T-M-13 | FR-7.2 | Moving a task to a different section updates its `section` FK |
| T-M-14 | FR-7.3 | Setting a task's `parent` makes it a subtask and preserves its data |
| T-M-15 | FR-7.4 | Clearing a task's `parent` promotes it to a top-level task |
| T-M-16 | FR-7.6 | Moving a parent task preserves all subtask relationships |
| T-M-17 | FR-8.4 | Serializing a list to JSON produces correct nested hierarchy |
| T-M-18 | FR-8.5 | Serializing tasks to CSV rows includes correct parent and depth values |

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
