# ToDo App — Implementation Plan

## Phase 1: Project Scaffolding

- [x] Initialize Django project (`django-admin startproject todoapp .`)
- [x] Create the main Django app (`python manage.py startapp tasks`)
- [x] Configure `settings.py`: add `tasks` to `INSTALLED_APPS`, set `ALLOWED_HOSTS`, static files, templates directory
- [x] Set up the base directory structure:
  ```
  /workspaces/ToDo App/
  ├── manage.py
  ├── todoapp/          (project config)
  │   ├── settings.py
  │   ├── urls.py
  │   └── wsgi.py
  ├── tasks/            (main app)
  │   ├── models.py
  │   ├── views.py
  │   ├── urls.py
  │   ├── forms.py
  │   ├── tests/
  │   │   ├── __init__.py
  │   │   ├── test_models.py
  │   │   ├── test_views.py
  │   │   └── test_integration.py
  │   └── templates/
  │       └── tasks/
  ├── static/
  │   ├── css/
  │   ├── js/
  │   └── vendor/       (htmx.min.js, Sortable.min.js)
  └── templates/
      └── base.html
  ```
- [x] Install Python dependencies: `django`, `markdown`, `bleach` (for sanitized Markdown rendering)
- [x] Create `pyproject.toml` with dependencies
- [x] Download HTMX and SortableJS into `static/vendor/` (vendored, no CDN)
- [x] Verify `python manage.py runserver 0.0.0.0:8000` starts cleanly

## Phase 2: Data Models

- [x] Define `List` model: `name`, `emoji` (optional), `position`
- [x] Define `Section` model: `list` (FK), `name`, `emoji` (optional), `position`
- [x] Define `Tag` model: `name` (unique)
- [x] Define `Task` model: `section` (FK), `parent` (self-FK, nullable), `title`, `notes`, `due_date`, `is_completed`, `completed_at`, `position`, `tags` (M2M to Tag)
- [x] Add `Meta` classes with `ordering = ['position']` on List, Section, Task
- [x] Add `__str__` methods for admin/debugging clarity
- [x] Run `makemigrations` and `migrate`
- [x] Verify models in Django shell: create a List > Section > Task > Subtask chain, confirm cascade deletes

## Phase 3: Model Tests

- [x] Write T-M-1: List with name and emoji persists
- [x] Write T-M-2: List without emoji succeeds
- [x] Write T-M-3: Deleting List cascades to Sections and Tasks
- [x] Write T-M-4: Section linked to List persists
- [x] Write T-M-5: Deleting Section cascades to Tasks
- [x] Write T-M-6: Task within Section persists
- [x] Write T-M-7: Nested subtasks (3+ levels) persist parent chain
- [x] Write T-M-8: Deleting parent Task cascades to subtasks
- [x] Write T-M-9: Tag M2M add/remove on Task
- [x] Write T-M-10: Completing task sets `is_completed` and `completed_at`
- [x] Write T-M-11: Un-completing task clears `is_completed` and `completed_at`
- [x] Write T-M-12: Completing parent does not cascade to subtasks
- [x] Write T-M-13: Moving task to different section updates FK
- [x] Write T-M-14: Setting parent makes task a subtask
- [x] Write T-M-15: Clearing parent promotes task
- [x] Write T-M-16: Moving parent preserves subtask relationships
- [x] Write T-M-17: Serializing a list to JSON produces correct nested hierarchy
- [x] Write T-M-18: Serializing tasks to CSV rows includes correct parent and depth
- [x] Run all model tests — confirm green

## Phase 4: URL Routing & Views (CRUD)

- [x] Define `tasks/urls.py` with URL patterns:
  - `GET /` — main page (renders base with sidebar + default list)
  - **Lists:** `POST /lists/`, `GET /lists/<id>/`, `PATCH /lists/<id>/`, `DELETE /lists/<id>/`
  - **Sections:** `POST /lists/<list_id>/sections/`, `PATCH /sections/<id>/`, `DELETE /sections/<id>/`
  - **Tasks:** `POST /sections/<section_id>/tasks/`, `GET /tasks/<id>/detail/`, `PATCH /tasks/<id>/`, `DELETE /tasks/<id>/`
  - **Task actions:** `POST /tasks/<id>/complete/`, `POST /tasks/<id>/uncomplete/`, `POST /tasks/<id>/move/`
  - **Tags:** `POST /tasks/<id>/tags/`, `DELETE /tasks/<id>/tags/<tag_id>/`
  - **Export:** `GET /lists/<id>/export/<format>/`, `GET /export/<format>/` (all lists)
- [x] Include `tasks.urls` in `todoapp/urls.py`
- [x] Implement list views: create, detail (returns sections + tasks), update, delete
- [x] Implement section views: create, update, delete
- [x] Implement task views: create (with optional `parent` param), detail (right sidebar), update (title, notes, due_date), delete
- [x] Implement task complete/uncomplete views (set `is_completed`, `completed_at`)
- [x] Implement task move view (accepts `section`, `parent`, `position` — used by drag-and-drop)
- [x] Implement tag add/remove views
- [x] Implement export views (see Phase 9a)
- [x] All views return HTMX partial HTML fragments when `HX-Request` header is present; full page otherwise

## Phase 5: View Tests

- [x] Write T-V-1: POST create list
- [x] Write T-V-2: PATCH rename list
- [x] Write T-V-3: DELETE list
- [x] Write T-V-4: GET list detail returns sections and tasks
- [x] Write T-V-5: POST create section
- [x] Write T-V-6: DELETE section
- [x] Write T-V-7: POST create task
- [x] Write T-V-8: POST create subtask with parent
- [x] Write T-V-9: PATCH update task title
- [x] Write T-V-10: DELETE task removes subtasks
- [x] Write T-V-11: PATCH update task notes
- [x] Write T-V-12: PATCH set/clear due date
- [x] Write T-V-13: Rendered notes contain `<a>` tags for URLs
- [x] Write T-V-14: POST complete task
- [x] Write T-V-15: Complete response includes undo toast HTML
- [x] Write T-V-16: POST undo completion
- [x] Write T-V-17: POST un-complete task
- [x] Write T-V-18: PATCH reorder task within section
- [x] Write T-V-19: PATCH move task to different section
- [x] Write T-V-20: PATCH nest task under parent
- [x] Write T-V-21: PATCH promote subtask
- [x] Write T-V-22: PATCH move task to different list
- [x] Write T-V-23: Move to list with no sections returns error
- [x] Write T-V-24: Move parent — subtasks follow
- [x] Write T-V-25: GET export single list returns downloadable file
- [x] Write T-V-26: GET export all lists returns downloadable file
- [x] Write T-V-27: JSON export contains nested hierarchy
- [x] Write T-V-28: CSV export has one row per task with correct columns
- [x] Write T-V-29: Markdown export has headings, checkboxes, indented subtasks
- [x] Write T-V-30: Export response has `Content-Disposition: attachment` with correct filename
- [x] Write T-V-31: Export of empty list returns valid file with headers only
- [x] Write T-V-32: Unsupported export format returns 400
- [x] Run all view tests — confirm green

## Phase 6: Templates & Layout

- [x] Create `base.html`: three-panel layout (left sidebar, center, right sidebar), include HTMX and SortableJS scripts
- [x] Create `tasks/sidebar.html` partial: lists ordered by position, each with emoji + name, "new list" button
- [x] Create `tasks/list_detail.html` partial: sections with tasks, "Completed" section at bottom
- [x] Create `tasks/section.html` partial: section header (emoji + name), task list, "add task" input
- [x] Create `tasks/task_item.html` partial: single task row (checkbox, title, indent for subtasks), nested subtask container
- [x] Create `tasks/task_detail.html` partial: right sidebar content (title, notes editor, due date picker, tags)
- [x] Create `tasks/toast.html` partial: undo completion toast with 5-second auto-dismiss
- [x] Create `tasks/list_form.html` partial: inline form for new/edit list
- [x] Create `tasks/section_form.html` partial: inline form for new/edit section
- [x] Add HTMX attributes to all interactive elements:
  - `hx-post`, `hx-patch`, `hx-delete` for CRUD
  - `hx-target` and `hx-swap` for partial updates
  - `hx-trigger` for events
- [x] Style the three-panel layout with CSS (flexbox/grid)
- [x] Style task nesting with indentation (padding-left per depth level)

## Phase 7: Markdown Rendering & Link Handling

- [x] Create a utility function to render Markdown to sanitized HTML using `markdown` + `bleach`
- [x] Whitelist safe tags/attributes in bleach (no `<script>`, no event handlers)
- [x] Auto-linkify URLs in rendered output (bleach's `linkify` or markdown extension)
- [x] Ensure all rendered links have `target="_blank"` and `rel="noopener noreferrer"`
- [x] Use this utility in the task detail view and template

## Phase 8: Task Completion & Undo Toast

- [x] Complete view: set `is_completed=True`, `completed_at=now()`, return updated task list + toast partial
- [x] Uncomplete view: set `is_completed=False`, `completed_at=None`, return updated task list
- [x] Toast partial: includes undo button with `hx-post` to uncomplete endpoint
- [x] Client-side: toast auto-dismisses after 5 seconds via `setTimeout` removing the element
- [x] Completed tasks rendered in a separate "Completed" group at the bottom of each section

## Phase 9a: Export

- [x] Create `tasks/views/export.py` with export logic
- [x] Implement `serialize_list_to_json(task_list)`: build nested dict (list > sections > tasks > subtasks with all fields)
- [x] Implement `serialize_list_to_csv(task_list)`: flatten tasks to rows with columns: `list`, `section`, `task`, `parent_task`, `depth`, `notes`, `due_date`, `tags`, `is_completed`
- [x] Implement `serialize_list_to_markdown(task_list)`: list name as `#`, sections as `##`, tasks as `- [ ]`/`- [x]` with indentation per depth, notes/due date/tags inline beneath each task
- [x] Single-list export view: `GET /lists/<id>/export/<format>/` — format is `json`, `csv`, or `md`
- [x] All-lists export view: `GET /export/<format>/` — exports every list into one file
- [x] Set `Content-Disposition: attachment; filename="<list-name>.<ext>"` (or `all-lists.<ext>`)
- [x] Return 400 for unsupported format values
- [x] Handle empty lists: produce valid file with list/section headers and no task entries
- [x] Add export buttons to templates: per-list button in the list view header, all-lists button in the sidebar header

## Phase 9b: Drag-and-Drop

- [x] Initialize SortableJS on task lists (each section's task container)
- [x] Configure SortableJS `group` option to allow dragging between sections
- [x] On `onEnd` event: extract task ID, new section ID, new position, new parent (if dropped onto a task)
- [x] Fire HTMX request to `/tasks/<id>/move/` with new `section`, `parent`, `position`
- [x] Move view: update task's `section`, `parent`, `position`; recalculate sibling positions; if cross-list, update subtask section FKs
- [x] Enable dropping tasks onto list items in the sidebar (cross-list move): on drop, move task to target list's first section
- [x] Handle nesting: dropping onto a task's drop zone sets `parent`; dropping between tasks at root clears `parent`
- [x] Return updated partials for affected sections after move

## Phase 10: Integration Tests

- [x] Write T-I-1: HTMX requests return partial HTML (not full page)
- [x] Write T-I-2: Clicking task returns right-sidebar detail HTML
- [x] Write T-I-3: Completed tasks appear under "Completed" heading
- [x] Write T-I-4: Toast contains 5-second dismiss mechanism
- [x] Write T-I-5: Markdown rendering strips script tags and event handlers
- [x] Write T-I-6: Drop triggers HTMX request, server returns updated partial
- [x] Write T-I-7: Nesting a task via move returns indented subtask in response
- [x] Write T-I-8: Cross-list move re-renders both source and target lists
- [x] Write T-I-9: Export button triggers file download (Content-Disposition header present)
- [x] Write T-I-10: JSON export of list with nested subtasks is valid JSON and round-trippable
- [x] Write T-I-11: Markdown export of completed tasks uses `[x]` checkbox syntax
- [x] Run full test suite — confirm all green

## Phase 11: Polish & Final Verification

- [x] Verify all CRUD operations work end-to-end in the browser
- [x] Test drag-and-drop: reorder, cross-section, nesting, cross-list
- [x] Test completion flow: complete, undo via toast, un-complete from completed section
- [x] Test Markdown notes: rendering, link clickability, XSS prevention
- [x] Test export: download JSON/CSV/Markdown for a populated list and an empty list
- [x] Test edge cases: empty lists, deeply nested subtasks, deleting a list with many tasks
- [x] Run full test suite one final time
- [x] Confirm app starts cleanly on port 8000
