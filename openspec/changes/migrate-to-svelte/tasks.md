## 1. Project Scaffolding and Build Pipeline

- [x] 1.1 Create `frontend/` directory with SvelteKit scaffold (`npx sv create`), TypeScript, adapter-static
- [x] 1.2 Configure Vite dev proxy: `/api/*` → `http://localhost:8000`
- [x] 1.3 Add `Makefile` with targets: `dev` (both servers), `build` (frontend), `deploy` (build + collect)
- [x] 1.4 Add `.gitignore` entries for `frontend/node_modules/`, `frontend/build/`, `frontend/.svelte-kit/`
- [x] 1.5 Configure adapter-static for SPA mode (fallback to `index.html` for client-side routing)
- [x] 1.6 Verify static build produces working output with `npx vite preview`

## 2. Django API Layer — Setup

- [x] 2.1 Add `django-ninja` to `pyproject.toml` and install
- [x] 2.2 Create `tasks/api/` package with `__init__.py` exposing the main NinjaAPI router
- [x] 2.3 Create `tasks/api/schemas.py` — Pydantic schemas for all models (ListSchema, SectionSchema, TaskSchema, TagSchema, ProjectSchema, TimeEntrySchema) plus input schemas
- [x] 2.4 Wire API router into `todoapp/urls.py` at `/api/`
- [x] 2.5 Verify CSRF cookie is set on GET requests and required on mutations

## 3. Django API Layer — List Endpoints

- [x] 3.1 Create `tasks/api/lists.py` — GET `/api/lists/` (all lists ordered by position)
- [x] 3.2 POST `/api/lists/` (create list with name/emoji)
- [x] 3.3 GET `/api/lists/:id/` (list detail with nested sections → tasks → subtasks)
- [x] 3.4 PUT `/api/lists/:id/` (update list name/emoji/project)
- [x] 3.5 DELETE `/api/lists/:id/` (cascade delete)
- [x] 3.6 PATCH `/api/lists/:id/move/` (reorder list position)
- [x] 3.7 Write API tests for all list endpoints (`tasks/tests/test_api_lists.py`)

## 4. Django API Layer — Section Endpoints

- [x] 4.1 Create `tasks/api/sections.py` — POST `/api/lists/:id/sections/` (create section)
- [x] 4.2 PUT `/api/sections/:id/` (update section name/emoji)
- [x] 4.3 DELETE `/api/sections/:id/` (cascade delete)
- [x] 4.4 PATCH `/api/sections/:id/move/` (reorder section position)
- [x] 4.5 Write API tests for all section endpoints (`tasks/tests/test_api_sections.py`)

## 5. Django API Layer — Task Endpoints

- [x] 5.1 Create `tasks/api/tasks.py` — POST `/api/sections/:id/tasks/` (create task, optional parent_id)
- [x] 5.2 GET `/api/tasks/:id/` (task detail with subtasks, tags, parent info)
- [x] 5.3 PUT `/api/tasks/:id/` (update title, notes, due_date, due_time, priority)
- [x] 5.4 DELETE `/api/tasks/:id/` (cascade delete)
- [x] 5.5 POST `/api/tasks/:id/complete/` (complete with subtask cascade, return updated tree)
- [x] 5.6 POST `/api/tasks/:id/uncomplete/` (uncomplete task only)
- [x] 5.7 PATCH `/api/tasks/:id/move/` (reorder, reparent, move across sections/lists, circular nesting rejection)
- [x] 5.8 POST `/api/tasks/:id/pin/` (toggle pin, enforce max 3)
- [x] 5.9 Write API tests for all task endpoints (`tasks/tests/test_api_tasks.py`)

## 6. Django API Layer — Tags, Search, Export, Import

- [x] 6.1 Create `tasks/api/tags.py` — POST `/api/tasks/:id/tags/`, DELETE `/api/tasks/:id/tags/:tag_id/`, GET `/api/tags/?exclude_task=`
- [x] 6.2 Create `tasks/api/search.py` — GET `/api/search/?q=` (matches title, notes, tags, grouped by list)
- [x] 6.3 Create `tasks/api/export.py` — GET `/api/export/:format/`, GET `/api/export/:id/:format/` (file downloads with Content-Disposition)
- [x] 6.4 Create `tasks/api/import_tasks.py` — POST `/api/import/` (CSV upload, summary response)
- [x] 6.5 Write API tests for tags, search, export, and import (`tasks/tests/test_api_misc.py`)

## 7. Django API Layer — Projects and Timesheet

- [x] 7.1 Create `tasks/api/projects.py` — full CRUD + toggle active, GET includes metrics (hours, list count, task counts)
- [x] 7.2 GET `/api/projects/:id/tasks/` (incomplete tasks for project's linked lists)
- [x] 7.3 Create `tasks/api/timesheet.py` — GET with `?week=` (grouped by date + summary), POST, DELETE
- [x] 7.4 Write API tests for projects and timesheet endpoints (`tasks/tests/test_api_projects.py`)

## 8. Svelte — API Client and Types

- [x] 8.1 Create `frontend/src/lib/api/types.ts` — TypeScript interfaces for all API response/request shapes
- [x] 8.2 Create `frontend/src/lib/api/client.ts` — fetch wrapper with CSRF token from cookie, JSON parsing, error handling, base URL config
- [x] 8.3 Create typed API functions: `api.lists.getAll()`, `api.lists.get(id)`, `api.tasks.complete(id)`, etc.

## 9. Svelte — Stores

- [x] 9.1 Create `frontend/src/lib/stores/lists.ts` — listsStore, selectedListStore, CRUD + reorder functions
- [x] 9.2 Create `frontend/src/lib/stores/tasks.ts` — tasksStore, selectedTaskStore, CRUD + complete/uncomplete + move/reparent + pin functions with optimistic updates
- [x] 9.3 Create `frontend/src/lib/stores/search.ts` — searchStore, debounced search function
- [x] 9.4 Create `frontend/src/lib/stores/toast.ts` — toastStore, addToast/dismissToast with auto-timeout
- [x] 9.5 Create `frontend/src/lib/stores/projects.ts` — projectsStore, CRUD + toggle functions
- [x] 9.6 Create `frontend/src/lib/stores/timesheet.ts` — timesheetStore, weekly fetch + create/delete

## 10. Svelte — Layout Shell and Navigation

- [x] 10.1 Create `frontend/src/routes/+layout.svelte` — three-panel shell (sidebar slot, center slot, detail slot)
- [x] 10.2 Implement responsive breakpoint: sidebar hamburger + detail overlay at <1024px
- [x] 10.3 Implement top navigation bar with links to Tasks, Projects, Timesheet, Import
- [x] 10.4 Implement bottom tab bar for mobile
- [x] 10.5 Create `frontend/src/routes/+page.svelte` — task view (default route)

## 11. Svelte — Sidebar and List Management

- [x] 11.1 Create `ListSidebar.svelte` — renders list items from listsStore, highlights selected
- [x] 11.2 Create `ListItem.svelte` — displays emoji + name, click to select, double-click to edit inline
- [x] 11.3 Implement list create form in sidebar
- [x] 11.4 Implement list delete with confirmation
- [x] 11.5 Integrate svelte-dnd-action for list reordering in sidebar
- [x] 11.6 Create `EmojiPicker.svelte` — searchable grid modal with categories, click-away/Escape to close

## 12. Svelte — Section and Task List

- [x] 12.1 Create `SectionList.svelte` — renders sections for selected list, each collapsible
- [x] 12.2 Create `SectionHeader.svelte` — section name/emoji, collapse toggle, edit/delete actions
- [x] 12.3 Implement collapse all / expand all toggle in list header
- [x] 12.4 Create `TaskList.svelte` — renders tasks for a section, separating active and completed
- [x] 12.5 Create `TaskRow.svelte` — title, checkbox, tag badges, due date, subtask count, pin button
- [x] 12.6 Create `SubtaskTree.svelte` — recursive component for nested subtask rendering
- [x] 12.7 Create `PinnedSection.svelte` — compact pinned tasks at top of list, hidden when empty
- [x] 12.8 Implement task create form (per section, with add-task input)
- [x] 12.9 Implement inline title editing on task rows

## 13. Svelte — Task Detail Panel

- [x] 13.1 Create `TaskDetail.svelte` — full detail view with title, notes, due date, priority, tags
- [x] 13.2 Implement auto-save on blur for title, due date, notes, priority fields
- [x] 13.3 Implement tag add/remove with autocomplete (fetches available tags from API)
- [x] 13.4 Implement parent task link with "jump to" scroll-and-highlight behavior
- [x] 13.5 Create `MarkdownEditor.svelte` — block-based editor: click to edit block (raw MD), blur to render (HTML), XSS sanitization via DOMPurify

## 14. Svelte — Task Completion and Toasts

- [x] 14.1 Implement completion flow: checkbox click → optimistic store update → fade-out animation (180ms) → move to Completed section → API call
- [x] 14.2 Create `ToastContainer.svelte` and `Toast.svelte` — stacking, auto-dismiss at 5s, undo action
- [x] 14.3 Implement undo: revert store state + API uncomplete call
- [x] 14.4 Implement uncomplete from Completed section (not just via toast)

## 15. Svelte — Drag-and-Drop

- [x] 15.1 Install `svelte-dnd-action`, create `DragContainer.svelte` and `DragItem.svelte` wrapper components
- [x] 15.2 Implement task reorder within section (position update)
- [x] 15.3 Implement task move across sections (section FK + position)
- [x] 15.4 Implement task nesting via drag (parent FK)
- [x] 15.5 Implement subtask promotion via drag (clear parent FK)
- [x] 15.6 Implement cross-list drag via sidebar drop targets (move to first section of target list)
- [x] 15.7 Implement section reorder drag within list
- [x] 15.8 Implement API failure rollback for all drag operations
- [x] 15.9 Prototype and test arbitrary-depth subtask nesting with svelte-dnd-action

## 16. Svelte — Keyboard Navigation

- [x] 16.1 Create `keyboard` Svelte action (`use:keyboard`) — attach to task list container
- [x] 16.2 Implement Arrow Up/Down and j/k navigation between non-completed tasks
- [x] 16.3 Implement Tab indent / Shift+Tab outdent (reparent via store + API)
- [x] 16.4 Implement x to complete focused task
- [x] 16.5 Implement Delete key with confirmation dialog
- [x] 16.6 Implement Escape to clear selection
- [x] 16.7 Implement Ctrl+Arrow Up/Down for section jumping
- [x] 16.8 Implement Ctrl+Arrow Left/Right for list cycling
- [x] 16.9 Implement collapsed section skipping
- [x] 16.10 Implement auto-scroll focused task into view

## 17. Svelte — Search

- [x] 17.1 Create `SearchBar.svelte` — input with 300ms debounce, triggers API search
- [x] 17.2 Create `SearchResults.svelte` — dropdown grouped by list, click to navigate
- [x] 17.3 Implement click-outside to close results
- [x] 17.4 Implement result navigation: select list + task, load detail panel

## 18. Svelte — Projects Page

- [x] 18.1 Create `frontend/src/routes/projects/+page.svelte` — project cards with metrics
- [x] 18.2 Implement project create form
- [x] 18.3 Implement project edit (name, description) and delete with confirmation
- [x] 18.4 Implement active/inactive toggle
- [x] 18.5 Implement list-to-project assignment (dropdown in list header on task view)

## 19. Svelte — Timesheet Page

- [x] 19.1 Create `frontend/src/routes/timesheet/+page.svelte` — weekly view with prev/next navigation
- [x] 19.2 Implement summary bar (total hours, per-project breakdowns)
- [x] 19.3 Implement time entry create form with project selector and task multi-select
- [x] 19.4 Implement date-grouped entry display
- [x] 19.5 Implement time entry delete

## 20. Svelte — Import Page

- [x] 20.1 Create `frontend/src/routes/import/+page.svelte` — file upload form
- [x] 20.2 Implement CSV upload to API with progress/loading state
- [x] 20.3 Implement import summary display (created/skipped counts)
- [x] 20.4 Implement error display for invalid files

## 21. Svelte — Export Integration

- [x] 21.1 Add export button component to list header (single list export)
- [x] 21.2 Add "Export All" button to sidebar header
- [x] 21.3 Implement format selector (JSON, CSV, Markdown) and trigger browser file download from API

## 22. Nginx and Deployment Configuration

- [x] 22.1 Create/update Nginx config: serve `frontend/build/` at `/`, proxy `/api/*` and `/admin/*` to Django
- [x] 22.2 Configure Nginx SPA fallback: all non-file, non-API routes serve `index.html`
- [x] 22.3 Add frontend build step to deploy script (npm install + npm run build)
- [x] 22.4 Test production build: static assets served by Nginx, API proxied to Gunicorn

## 23. E2E Tests (Playwright)

- [x] 23.1 Update `e2e/conftest.py` — fixtures now start both Django API and Vite preview server (or test against built static files)
- [x] 23.2 Rewrite `e2e/test_task_crud.py` — task create/update/delete against Svelte UI
- [x] 23.3 Rewrite `e2e/test_task_completion.py` — complete, undo toast, uncomplete
- [x] 23.4 Rewrite `e2e/test_keyboard.py` — arrow keys, j/k, Tab, Delete, Escape
- [x] 23.5 Rewrite `e2e/test_drag_drop.py` — reorder within/across sections, cross-list
- [x] 23.6 Rewrite `e2e/test_search.py` — search bar and result navigation
- [x] 23.7 Rewrite `e2e/test_navigation.py` — sidebar, detail panel, empty states
- [x] 23.8 Rewrite `e2e/test_list_crud.py` — list create/rename/delete
- [x] 23.9 Rewrite `e2e/test_section_crud.py` — section create/rename/delete
- [x] 23.10 Rewrite `e2e/test_tags.py` — tag add/remove
- [x] 23.11 Rewrite `e2e/test_export.py` — JSON/CSV/MD export downloads
- [x] 23.12 Rewrite `e2e/test_markdown.py` — markdown editor
- [x] 23.13 Rewrite `e2e/test_pinning.py` — pin/unpin tasks

## 24. Cleanup and Cut-Over

- [x] 24.1 Remove `templates/` directory (Django HTML templates)
- [x] 24.2 Remove `tasks/templates/` directory (HTMX partials)
- [x] 24.3 Remove `static/js/` directory (vanilla JS modules)
- [x] 24.4 Remove `static/vendor/` directory (htmx.min.js, Sortable.min.js)
- [x] 24.5 Remove old HTML-rendering view functions from `tasks/views/` (keep only if API reuses logic)
- [x] 24.6 Remove `tasks/templatetags/` if Markdown rendering moves to client-side
- [x] 24.7 Update `CLAUDE.md` — new project structure, commands, architecture decisions
- [x] 24.8 Update `SPECS.md` — replace FR-6 (HTMX) with Svelte reactivity, update tech stack section
- [x] 24.9 Verify all E2E tests pass against Svelte frontend
- [ ] 24.10 Verify production deployment on Hetzner











