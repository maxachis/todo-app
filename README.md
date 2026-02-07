# ToDo App

A multi-list task management application built with Django, HTMX, and SortableJS.

## Features

- **Multiple lists** with emoji support and sidebar navigation
- **Sections** within lists for organizing tasks
- **Arbitrary nesting** — subtasks can be nested to any depth
- **Markdown notes** with sanitized rendering and auto-linked URLs
- **Task completion** with undo toast (5-second window)
- **Drag-and-drop** reordering, cross-section and cross-list moves via SortableJS
- **Tags** on tasks
- **Due dates**
- **Export** to JSON, CSV, or Markdown (single list or all lists)
- **No page reloads** — all interactions use HTMX partial updates

## Tech Stack

- Python 3.14, Django 6.0, SQLite
- HTMX 2.0 + SortableJS 1.15 (vendored, no CDN)
- Markdown rendering via `markdown` + `bleach`

## Setup

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver 0.0.0.0:8000
```

The app runs on [http://localhost:8000](http://localhost:8000).

## Running Tests

```bash
# All tests (62 total)
uv run python manage.py test tasks

# By category
uv run python manage.py test tasks.tests.test_models       # 18 model tests
uv run python manage.py test tasks.tests.test_views        # 32 view tests
uv run python manage.py test tasks.tests.test_integration  # 12 integration tests
```

## Project Structure

```
tasks/
  models.py              # List, Section, Task, Tag
  views/
    lists.py             # List CRUD
    sections.py          # Section CRUD
    tasks.py             # Task CRUD, complete/uncomplete, move
    tags.py              # Tag add/remove
    export.py            # JSON, CSV, Markdown export
  urls.py                # All URL patterns
  forms.py               # Django forms
  templatetags/
    markdown_extras.py   # Sanitized Markdown filter
  templates/tasks/
    index.html           # Main page (extends base.html)
    partials/            # HTMX partial templates
  tests/
    test_models.py       # T-M-1 through T-M-18
    test_views.py        # T-V-1 through T-V-32
    test_integration.py  # T-I-1 through T-I-11
templates/
  base.html              # Three-panel layout shell
static/
  css/style.css          # App styles
  js/app.js              # SortableJS init, toast dismiss
  vendor/                # htmx.min.js, Sortable.min.js
```

## Export Formats

| Format   | Description |
|----------|-------------|
| JSON     | Full nested hierarchy (lists > sections > tasks > subtasks) |
| CSV      | One row per task with `parent_task` and `depth` columns |
| Markdown | `#`/`##` headings, `- [ ]`/`- [x]` checkboxes, indented subtasks |

Export endpoints:
- Single list: `/lists/<id>/export/<json|csv|md>/`
- All lists: `/export/<json|csv|md>/`
