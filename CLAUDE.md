# CLAUDE.md - ToDo App

## Project Overview

Single-user task manager migrated to a Svelte frontend + Django JSON API backend.

- Frontend: SvelteKit (SPA) in `frontend/`
- Backend: Django + Django Ninja API in `tasks/api/`
- Database: SQLite
- Production routing: Nginx serves `frontend/build`, proxies `/api/*` and `/admin/*` to Django

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
      api/         # typed API client + request/response types
      stores/      # Svelte stores for lists/tasks/projects/timesheet/search/toast
      components/  # feature UI components
      actions/     # keyboard and other Svelte actions
    routes/
      +layout.svelte
      +page.svelte
      projects/+page.svelte
      timesheet/+page.svelte
      import/+page.svelte

tasks/
  api/             # Django Ninja routers: lists/sections/tasks/tags/search/export/import/projects/timesheet
  models.py
  services/
  tests/

e2e/
  conftest.py
  test_*.py

deploy/
  nginx.todoapp.conf
  update.sh
```

## Architecture Notes

- Client-side reactivity and optimistic UI are implemented in Svelte stores.
- Task detail editing auto-saves via API on blur.
- Drag/drop and keyboard navigation are handled in Svelte components/actions.
- Export/import/search/project/timesheet behavior is API-driven.
- Legacy server-rendered HTMX templates and vanilla JS modules have been removed.

## Testing Notes

- Current canonical backend tests are API-focused (`tasks/tests/test_api_*.py`).
- E2E suite targets Svelte UI selectors and runs against Django API + Vite preview.
- Legacy HTMX view tests are obsolete after cut-over.
