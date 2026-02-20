## Context

The app is a single-user task manager running Django 5.1 on a Hetzner server behind Nginx/Gunicorn. The frontend is currently server-rendered Django templates with HTMX for partial updates and 11 vanilla JS modules for client-side behavior (drag-and-drop, keyboard nav, focus tracking, etc.). All views are function-based, returning HTML partials for HTMX requests or full pages for direct navigation.

The app is expanding to include a CRM and potentially other tools. The frontend needs to support that growth without accumulating workarounds for each interactive feature.

## Goals / Non-Goals

**Goals:**
- Replace HTMX + vanilla JS with Svelte/SvelteKit as the sole frontend rendering layer
- Create a clean JSON API in Django that serves both the current task app and future apps (CRM, etc.)
- Preserve all existing user-facing behavior — this is a technology migration, not a feature change
- Keep production deployment simple: single Hetzner server, no Node.js process in production
- Establish patterns (component structure, API conventions, state management) that scale to multiple apps

**Non-Goals:**
- Adding new features (CRM, auth, Postgres migration) — those are separate changes
- Server-side rendering (SSR) — no SEO needs, no public users
- Mobile native app — PWA support continues as-is
- Changing the data model or business logic — Django models and validation rules stay as-is

## Decisions

### 1. API framework: Django Ninja over DRF

**Choice:** Django Ninja

**Why:** Django Ninja is lighter, faster, and uses Python type hints for schema validation (Pydantic). DRF is more mature but heavier — its serializers, viewsets, and browsable API add overhead that a single-user app doesn't need. Django Ninja's function-based approach also maps more naturally to the existing function-based views, making the migration more mechanical.

**Alternatives considered:**
- DRF: More ecosystem support, but the app doesn't need generic viewsets, pagination classes, or authentication backends. Too much machinery for the use case.
- Raw Django JsonResponse: Too low-level. No schema validation, no automatic documentation, manual serialization everywhere.

### 2. Frontend architecture: SvelteKit with adapter-static

**Choice:** SvelteKit in SPA mode with `adapter-static`

**Why:** SvelteKit provides file-based routing, built-in stores, and a standard project structure. `adapter-static` builds to plain HTML/JS/CSS — no Node.js runtime in production. The output is a static SPA that Nginx serves directly, with API calls proxied to Django.

**Alternatives considered:**
- Standalone Svelte (no SvelteKit): Loses file-based routing, would need to wire up a router manually. SvelteKit's structure is worth the minimal overhead.
- SvelteKit with adapter-node (SSR): Adds a Node.js process in production for zero benefit. No SEO, no public users, no crawlers.

### 3. Deployment: Nginx serves static Svelte build, proxies API to Django

**Choice:**
```
Nginx
├── /api/*  →  Django (gunicorn)
├── /admin/* → Django (gunicorn)
└── /*      →  Svelte static files (frontend/build/)
```

**Why:** Production stays a single Django process. Nginx serves the built Svelte assets directly (fast, cacheable). API routes are proxied to Django. No Node.js in production, no new infrastructure, same Hetzner server.

**Dev workflow:** Two processes locally — `vite dev` (port 5173) + `python manage.py runserver` (port 8000). Vite proxies `/api/*` to Django during development.

**Alternatives considered:**
- Django serves Svelte assets via WhiteNoise: Simpler Nginx config but less efficient. Django shouldn't serve static files in production when Nginx is already there.
- Docker/container setup: Unnecessary complexity for a single-user app on a single server.

### 4. API design: RESTful resource endpoints under /api/

**Choice:** REST-style JSON API namespaced under `/api/`

```
GET    /api/lists/                  → all lists (sidebar)
POST   /api/lists/                  → create list
GET    /api/lists/:id/              → list detail with sections + tasks
PUT    /api/lists/:id/              → update list
DELETE /api/lists/:id/              → delete list
PATCH  /api/lists/:id/move/         → reorder list

GET    /api/lists/:id/sections/     → sections for a list
POST   /api/lists/:id/sections/     → create section
PUT    /api/sections/:id/           → update section
DELETE /api/sections/:id/           → delete section
PATCH  /api/sections/:id/move/      → reorder section

POST   /api/sections/:id/tasks/     → create task in section
GET    /api/tasks/:id/              → task detail
PUT    /api/tasks/:id/              → update task (title, notes, due_date, priority)
DELETE /api/tasks/:id/              → delete task
POST   /api/tasks/:id/complete/     → complete task (cascades to subtasks)
POST   /api/tasks/:id/uncomplete/   → uncomplete task
PATCH  /api/tasks/:id/move/         → move/reorder/reparent task
POST   /api/tasks/:id/pin/          → toggle pin

POST   /api/tasks/:id/tags/         → add tag
DELETE /api/tasks/:id/tags/:tag_id/ → remove tag

GET    /api/search/?q=              → search across all lists
GET    /api/export/:format/         → export all lists
GET    /api/export/:id/:format/     → export single list

GET    /api/projects/               → all projects
POST   /api/projects/               → create project
PUT    /api/projects/:id/           → update project
DELETE /api/projects/:id/           → delete project
POST   /api/projects/:id/toggle/    → toggle active

GET    /api/timesheet/?week=        → time entries for week
POST   /api/timesheet/              → create time entry
DELETE /api/timesheet/:id/          → delete time entry

POST   /api/import/                 → import TickTick CSV
```

**Why:** Maps directly to existing view functions. Each current view becomes an API endpoint returning JSON instead of HTML. Resource-oriented URLs are predictable and easy to consume from Svelte.

**CSRF handling:** Django Ninja supports session-based CSRF. The Svelte app reads the CSRF token from a cookie and sends it in request headers. Same-origin requests, no CORS needed.

### 5. State management: Svelte stores per resource

**Choice:** Svelte writable stores, one per resource type, co-located with API fetch functions.

```
frontend/src/lib/stores/
  lists.ts       → listsStore, selectedListStore
  tasks.ts       → tasksStore, selectedTaskStore
  projects.ts    → projectsStore
  timesheet.ts   → timesheetStore
  search.ts      → searchStore
  toast.ts       → toastStore
```

**Pattern:** Each store module exports the store + async functions that mutate it:

```ts
// tasks.ts (simplified)
export const tasksStore = writable<Task[]>([]);
export const selectedTask = writable<Task | null>(null);

export async function completeTask(id: number) {
  // Optimistic update
  tasksStore.update(tasks => markComplete(tasks, id));
  // Persist
  await api.post(`/api/tasks/${id}/complete/`);
}
```

**Why:** Svelte's built-in stores are sufficient. No need for a state management library. Stores are reactive, composable, and the API surface is tiny. Each store file contains both state and the async operations that modify it, keeping data flow traceable.

**Alternatives considered:**
- Global store library (like TanStack Query): Adds caching, refetching, and stale management. Overkill for single-user — there's no other user who could change data between fetches.
- Component-local state only: Breaks down when multiple components need the same data (e.g., sidebar list count + center panel both need task data).

### 6. Component structure: Feature-based with shared primitives

```
frontend/src/
  lib/
    api/             → API client, types, fetch wrappers
      client.ts      → fetch wrapper with CSRF, error handling
      types.ts       → TypeScript interfaces matching API responses
    stores/          → Svelte stores (see above)
    components/
      shared/        → Button, Modal, Toast, EmojiPicker, MarkdownEditor
      tasks/         → TaskRow, TaskList, TaskDetail, SubtaskTree, PinnedSection
      sections/      → SectionHeader, SectionList, SectionCollapse
      lists/         → ListSidebar, ListItem, ListHeader
      search/        → SearchBar, SearchResults
      dnd/           → DragContainer, DragItem (svelte-dnd-action wrappers)
    actions/         → Svelte actions (keyboard shortcuts, click-outside, focus-trap)
  routes/
    +layout.svelte   → Three-panel shell (sidebar + center + detail)
    +page.svelte     → Task view (default route)
    projects/
      +page.svelte   → Projects page
    timesheet/
      +page.svelte   → Timesheet page
    import/
      +page.svelte   → Import page
```

**Why:** Feature-based grouping keeps related components together. Shared primitives (Toast, Modal, EmojiPicker) live in `shared/` to avoid duplication across features. SvelteKit's file-based routing maps cleanly to the current nav structure (Tasks, Projects, Timesheet, Import).

### 7. Drag-and-drop: svelte-dnd-action

**Choice:** `svelte-dnd-action` for all drag-and-drop interactions.

**Why:** It's the most mature Svelte drag library, integrates natively with Svelte's reactivity (no DOM ownership conflict), supports nested containers (for subtask nesting), and handles cross-container drags (moving tasks between sections). This directly solves the core pain point that motivated the migration.

**Pattern:** Drop events update the Svelte store (optimistic), then fire an API call to persist. On API failure, revert the store.

### 8. Keyboard navigation: Svelte actions

**Choice:** Implement keyboard navigation as Svelte actions (`use:keyboard`) rather than a global event listener module.

**Why:** Svelte actions attach behavior to DOM elements declaratively. The keyboard handler can read component state directly (which task is focused, which section is collapsed) without the manual DOM querying and state synchronization the current `keyboard.js` requires.

### 9. Testing strategy

- **API tests:** Django TestCase with `self.client`, asserting JSON responses. Direct migration of existing view tests — change assertions from HTML fragments to JSON payloads.
- **Component tests:** Svelte component tests with `@testing-library/svelte` for critical interactive components (TaskRow, DragContainer, SearchBar).
- **E2E tests:** Playwright tests rewritten against the Svelte frontend. Same scenarios, updated selectors and interaction patterns.

### 10. Migration approach: parallel build, feature-by-feature

**Choice:** Build the Svelte frontend alongside the existing HTMX app. Migrate one feature area at a time. Switch over when parity is reached.

**Sequence:**
1. Set up SvelteKit project, API client, build pipeline
2. API layer — migrate views to Django Ninja endpoints (can coexist with existing views)
3. Core layout — three-panel shell, sidebar, navigation
4. Task CRUD — list detail, sections, task rows, task detail panel
5. Drag-and-drop — task reordering, cross-section, cross-list
6. Keyboard navigation
7. Remaining features — search, export, projects, timesheet, import
8. Cut over — remove old templates, static JS, HTMX views

**Why:** Parallel build means the existing app stays functional throughout migration. Each step can be tested independently. If the migration stalls, the old app still works.

## Risks / Trade-offs

**Two dev servers locally** → Minor inconvenience. Use a `Makefile` or `just` recipe to start both with one command.

**Loss of Django form validation in templates** → API endpoints must return structured validation errors. Svelte forms must display them. More code for simple forms, but consistent pattern across all forms.

**svelte-dnd-action maturity for complex nesting** → The library handles nested containers but arbitrary-depth subtask nesting may need custom work. Mitigate by prototyping the deepest nesting scenario early (phase 5).

**Parallel maintenance during migration** → During the transition, both HTMX views and API endpoints exist. Keep the API endpoints in a separate `api/` URL namespace to avoid confusion. Old views can be removed once parity is confirmed.

**TypeScript learning curve** → The codebase is currently pure Python + vanilla JS. TypeScript adds a type system to learn. Mitigate by starting with loose types (`any` where expedient) and tightening over time.

## Migration Plan

1. **Prepare:** Create `frontend/` directory with SvelteKit scaffold. Configure Vite proxy to Django. Add `Makefile` targets for dev and build.
2. **API layer:** Add Django Ninja to `pyproject.toml`. Create `api/` app or `tasks/api.py` with endpoints. Existing views remain untouched.
3. **Build pipeline:** Configure `adapter-static`. Add build step to deploy script. Update Nginx config with `/api/*` proxy and static file serving for `/*`.
4. **Feature migration:** One route at a time (tasks → projects → timesheet → import). Each route is fully functional in Svelte before moving to the next.
5. **Test migration:** API tests written alongside each endpoint. E2E tests rewritten per route.
6. **Cut over:** Remove `templates/`, `static/js/`, `static/vendor/`, HTMX view functions. Update `CLAUDE.md` and `SPECS.md`.
7. **Rollback:** During migration, the old app is always one `git revert` away. After cut-over, the old code exists in git history.

## Open Questions

- **Django Ninja router organization:** Single `api.py` per app, or split into `api/lists.py`, `api/tasks.py`, etc. mirroring the current views split? Leaning toward split for consistency.
- **Markdown rendering:** Currently server-side (Python `markdown` + `bleach`). Move to client-side (`marked` + `DOMPurify`) or keep as an API endpoint that returns rendered HTML? Client-side is faster for the editor preview; server-side is safer for sanitization.
- **Emoji data:** Currently a static JS file (`emoji_data.js`). Bundle into the Svelte app or serve from Django API? Likely bundle — it's static data.
