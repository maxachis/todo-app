# CLAUDE.md — ToDo App

## Project Overview

Multi-list task management app. Django + HTMX + SortableJS. Single-user, no auth. SQLite. Port 8000.

See `SPECS.md` for full requirements and test matrix. See `plan.md` for implementation phases.

## Commands

```bash
# Run dev server
python manage.py runserver 0.0.0.0:8000

# Run all tests
python manage.py test tasks

# Run specific test file
python manage.py test tasks.tests.test_models
python manage.py test tasks.tests.test_views
python manage.py test tasks.tests.test_integration

# Run E2E tests (Playwright — requires dev server)
pytest e2e/ -x -v

# Run specific E2E test file
pytest e2e/test_keyboard.py -x -v

# Migrations
python manage.py makemigrations && python manage.py migrate

# Format
black .
```

## Project Structure

```
tasks/                  # Main Django app
  models.py             # List, Section, Task, Tag
  views/                # Split by concern (see below)
    lists.py            # List CRUD views
    sections.py         # Section CRUD views
    tasks.py            # Task CRUD, complete/uncomplete, move
    tags.py             # Tag add/remove on tasks
    export.py           # Export views (JSON, CSV, Markdown)
    reorder.py          # Shared reorder_siblings() utility
  urls.py               # All URL patterns
  forms.py              # Django forms for validation
  tests/
    test_models.py      # T-M-* tests
    test_views.py       # T-V-* tests
    test_integration.py # T-I-* tests
  templates/tasks/      # HTMX partials and full pages
  templatetags/         # Custom filters (markdown rendering)
static/
  css/                  # App styles
  js/                   # Modular JS (see below)
    app.js              # Thin orchestrator — calls init from each module
    utils.js            # Shared: getCsrfToken, postMove, updateSubtaskCounts
    sortable_init.js    # SortableJS init with targeted WeakMap tracking
    keyboard.js         # Keyboard navigation and shortcuts
    toast.js            # Toast display, dismiss, auto-timeout
    emoji_picker.js     # Emoji picker modal
    markdown_editor.js  # Live markdown block editor
    completion.js       # Check-off transitions and optimistic UI
    focus.js            # Focus tracking and restoration after HTMX swaps
    panels.js           # Mobile panels, nav highlight, sidebar/section editing
  vendor/               # htmx.min.js, Sortable.min.js (vendored, no CDN)
e2e/                    # Playwright E2E tests
  conftest.py           # Fixtures: dev server, seed data, DB reset
  test_task_crud.py     # Task create/update/delete
  test_task_completion.py # Complete, undo toast, uncomplete
  test_keyboard.py      # Arrow keys, j/k, Tab indent, Delete, Escape
  test_drag_drop.py     # SortableJS reorder within/across sections
  test_search.py        # Search bar results and navigation
  test_navigation.py    # Sidebar, detail panel, empty states
  test_list_crud.py     # List create/rename/delete
  test_section_crud.py  # Section create/rename/delete
  test_tags.py          # Tag add/remove on tasks
  test_export.py        # JSON/CSV/MD export
  test_markdown.py      # Markdown editor
templates/
  base.html             # Three-panel shell: sidebar, center, right detail
```

### When to split vs. combine

**Split** views into separate files per concern (`lists.py`, `sections.py`, `tasks.py`, `tags.py`) — they have low coupling and tasks are typically scoped to one entity at a time.

**Keep combined:**
- `models.py` — all four models in one file. They're tightly coupled (FK chains) and small enough that splitting adds overhead with no benefit.
- `urls.py` — single file. All routes in one place is easier to scan than scattered URL configs.
- `forms.py` — single file unless it exceeds ~100 lines, then split to match views.

**Isolate** Markdown rendering into `tasks/templatetags/markdown_extras.py` — it wraps an external dependency (markdown + bleach), is independently testable, and has security implications (XSS sanitization).

**Isolate** export serializers into `tasks/views/export.py` — each format (JSON, CSV, Markdown) is a distinct serialization concern with its own output structure, independently testable, and only touched when export logic changes.

## Code Style

### Python (Django)

- **Formatter:** Black, 4-space indent, 88-char line length
- **Naming:**
  - Variables/functions: `snake_case` — descriptive names (`task_list`, not `tl`)
  - Booleans: `is_completed`, `has_subtasks`, `can_edit`
  - Functions: verb + noun: `get_task_by_id`, `validate_move_target`
  - Constants: `SCREAMING_SNAKE_CASE` — `MAX_TASK_DEPTH`, `TOAST_TIMEOUT_MS`
  - Models/classes: `PascalCase` — `TaskList`, `Section`
- **Functions:** single responsibility, max ~25 lines, max 3-4 parameters, return early for guards
- **Comments:** explain *why*, not *what*. Docstrings on view functions and utility functions.
- **Errors:** use specific Django exceptions (`Http404`, `ValidationError`). Return helpful messages. Log with context.
- **No commented-out code.** Delete it; git has history.

### Templates (HTML/HTMX)

- 2-space indent in HTML templates
- HTMX attributes on the element that triggers the action, not on wrappers
- Every HTMX-driven view must work for both full requests (return full page) and `HX-Request` (return partial)
- Name partials with a `_` prefix or place in a `partials/` subdirectory — be consistent, pick one

### JavaScript

- Minimal JS — only for SortableJS initialization and toast auto-dismiss
- No framework, no build step. Vanilla JS in `static/js/`
- `snake_case` for filenames, `camelCase` for variables/functions

## Key Architecture Decisions

- **Task.section FK is always set** — even for subtasks. When a task moves across lists, update `section` on the task and all its descendants.
- **Arbitrary nesting** via self-referential `parent` FK. No depth limit enforced at the model level.
- **Position fields** on List, Section, Task. Reordering updates positions of affected siblings. Use gap-based numbering (10, 20, 30) to reduce writes on reorder.
- **Markdown rendering** uses `markdown` + `bleach`. Sanitize on *output* (when rendering), not on input (store raw Markdown). Linkify URLs automatically. All links get `target="_blank" rel="noopener noreferrer"`.
- **Completing a parent does not cascade** to subtasks.
- **Undo toast** is a server-rendered HTMX partial dismissed client-side via `setTimeout`.
- **Export** serves file downloads (not HTMX partials). JSON preserves full nested hierarchy. CSV flattens to one row per task with `parent_task` and `depth` columns. Markdown uses `#`/`##` headings and `- [ ]`/`- [x]` checkboxes. All responses set `Content-Disposition: attachment`.
- **Annotated querysets need explicit ordering** — `annotate()` can drop `Meta.ordering`. Always chain `.order_by()` on querysets used for rendering.
- **HTMX scroll stability** — when an action only changes a small part of the page (e.g., toggling a pin), return targeted OOB swaps for just the affected elements — never replace the entire `#center-panel`. Use `HX-Trigger` headers for client-side state toggles.
- **Playwright locators in nested DOMs** — always scope pin/action button locators with `> .task-row >` or similar direct-child selectors to avoid matching buttons inside nested subtasks.

## Testing Conventions

- Use `django.test.TestCase` for all tests
- Test file maps to spec: `test_models.py` = T-M-*, `test_views.py` = T-V-*, `test_integration.py` = T-I-*
- Each test method name includes the test ID: `test_tm1_list_with_emoji`, `test_tv14_complete_task`
- Use `setUp` for shared fixtures (a List + Section + Task chain). Don't over-share — if a test needs unique data, create it locally.
- View tests use `self.client` with `HTTP_HX_REQUEST='true'` header for HTMX tests
- Assert on status codes, database state, and HTML fragment content (for HTMX responses)
