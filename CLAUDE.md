# CLAUDE.md - Nexus

## Project Overview

Personal operations hub (tasks, CRM, projects, timesheets, network graph), built as a SvelteKit SPA frontend + Django JSON API backend.

- Frontend: SvelteKit (SPA, static adapter) in `frontend/` — TypeScript throughout
- Backend: Django + Django Ninja API in `tasks/api/` and `network/api/`
- Database: SQLite
- Production routing: Nginx serves `frontend/build`, proxies `/api/*` and `/admin/*` to Django

### Key Features

- **Task management**: Lists, sections, tasks with arbitrary subtask nesting, drag-and-drop (svelte-dnd-action), keyboard navigation, pinning, search, export (JSON/CSV/Markdown)
- **Task recurrence**: Daily, weekly, monthly, yearly, and custom-date repeat schedules with automatic next-occurrence generation on completion
- **Network/CRM**: People (with email/LinkedIn), Organizations, Interactions, Relationships (person-person and org-person), and a Graph visualization
- **Task-entity links**: Tasks can link to people and organizations; interactions can link to tasks
- **Upcoming dashboard**: Tasks grouped by time horizon (Overdue, Today, Tomorrow, This Week, Later)
- **Projects & timesheet**: Project management with metrics, weekly time tracking
- **Import**: TickTick CSV, native JSON, and native CSV import with auto-format detection
- **Dark mode**: Light/system/dark theme with CSS variable overrides, localStorage persistence, FOUC prevention
- **Resizable panels**: Draggable resize handles between the three task-view panels with min-width constraints and localStorage persistence
- **Settings menu**: Cog button in navbar with dropdown (Import lives here, not in primary nav)

### Navigation

Top navbar tabs: Tasks, Upcoming, People, Organizations, Interactions, Relationships, Graph, Projects, Timesheet. Import is accessed via the settings cog dropdown. Theme toggle is in the navbar.

## Commands

```bash
# Backend dev server
python manage.py runserver 0.0.0.0:8000

# Frontend dev server
cd frontend && npm run dev

# Frontend type/lint checks
cd frontend && npm run check

# Frontend production build
cd frontend && npm run build

# API tests (pytest)
uv run python -m pytest tasks/tests/test_api_setup.py -q
uv run python -m pytest tasks/tests/test_api_lists.py tasks/tests/test_api_sections.py tasks/tests/test_api_tasks.py tasks/tests/test_api_misc.py tasks/tests/test_api_projects.py -q

# E2E tests (Svelte + preview + Django API)
uv run python -m pytest e2e -q

# Migrations
python manage.py makemigrations && python manage.py migrate
```

## Project Structure

```text
frontend/
  src/
    lib/
      api/           # typed API client (client.ts, types.ts, index.ts)
      stores/        # Svelte stores: lists, tasks, projects, timesheet, search, toast, theme, panelWidths, upcoming
      components/
        dnd/         # drag-and-drop components
        lists/       # list sidebar components
        search/      # search UI
        sections/    # section components
        shared/      # ExportButton, LinkedEntities, MarkdownEditor, ResizeHandle, Toast, TypeaheadSelect
        tasks/       # task row and detail components
      actions/       # keyboard and other Svelte actions
    routes/
      +layout.svelte
      +page.svelte         # Tasks (main three-panel view)
      upcoming/            # Upcoming dashboard
      people/              # People list + detail
      organizations/       # Organizations list + detail
      interactions/        # Interactions list + detail
      relationships/       # Person-person and org-person relationships
      graph/               # Network graph visualization
      projects/            # Project management
      timesheet/           # Weekly time tracking
      import/              # Data import (TickTick CSV, native JSON/CSV)

tasks/
  api/               # Django Ninja routers: lists, sections, tasks, tags, search, export, import, projects, timesheet, upcoming
  models.py          # List, Section, Task (with recurrence fields), Tag, TimeEntry, Project
  services/
    recurrence.py    # next-occurrence computation
    ticktick_import.py
    native_import.py # native JSON + CSV import
  tests/

network/
  api/               # Django Ninja routers: people, organizations, org_types, interactions, interaction_types, relationships, graph, task_links
  models/
    person.py        # Person (with email, linkedin_url)
    organization.py
    org_type.py
    interaction.py
    interaction_type.py
    relationship/    # person_person.py, organization_person.py
    task_links.py    # TaskPersonLink, TaskOrganizationLink, InteractionTaskLink

e2e/
  conftest.py
  test_*.py

deploy/
  nginx.nexus.conf
  update.sh
```

## Architecture Notes

- Client-side reactivity and optimistic UI are implemented in Svelte stores (one per resource type, with co-located async mutation functions and rollback on API failure).
- Task detail editing auto-saves via API on blur.
- Drag-and-drop uses svelte-dnd-action with optimistic store updates and API persistence.
- Keyboard navigation state is managed in Svelte stores and actions.
- Three-panel layout on the Tasks route has draggable resize handles; widths persist in localStorage.
- Panels scroll independently; the app shell is viewport-locked on desktop (no document scroll).
- Theme preference (light/system/dark) is stored in localStorage and applied via `data-theme` attribute on `<html>`.
- Entity selection fields (people, org types, interaction types) use the reusable TypeaheadSelect component with optional inline creation via `onCreate` callback.
- Task recurrence is handled server-side: completing a recurring task generates the next occurrence in the same section.
- Import auto-detects format from file extension and CSV header structure.

## Testing Notes

- Current canonical backend tests are API-focused (`tasks/tests/test_api_*.py`).
- E2E suite targets Svelte UI selectors and runs against Django API + Vite preview.
- Legacy HTMX view tests are obsolete after cut-over.

## Mistakes

- **[env]**: Use `uv run python manage.py runserver` instead of bare `python manage.py runserver` — Django is installed in the uv-managed virtualenv, not globally.
- **[tooling]**: `openspec` CLI must be run from the project root (`/workspaces/todo-app/`), not from subdirectories like `frontend/`. After `cd frontend && npm run check`, return to root or use absolute paths.
