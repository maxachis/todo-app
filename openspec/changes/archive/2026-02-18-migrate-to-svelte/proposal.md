## Why

The app's frontend has outgrown HTMX's server-rendered partial model. Client-side state management is spreading across 8+ vanilla JS modules — focus tracking, optimistic completion UI, drag-and-drop DOM synchronization, keyboard navigation state — creating a de facto client-side framework without the tooling benefits of one. Drag-and-drop in particular required extensive workarounds (WeakMap tracking, targeted OOB swaps, flicker fixes) because SortableJS and HTMX compete for DOM ownership. As the app expands to include a CRM and other applications, the frontend needs a unified reactive model that can handle both simple CRUD and rich interactions without accumulating workarounds.

## What Changes

- **BREAKING**: Replace all Django HTML templates (`templates/`, `tasks/templates/`) with a Svelte/SvelteKit frontend
- **BREAKING**: Replace all HTMX-driven Django views with a JSON API layer (Django Ninja or DRF)
- **BREAKING**: Remove all vanilla JS modules (`static/js/`) — their functionality moves into Svelte components
- **BREAKING**: Remove vendored HTMX and SortableJS — replaced by Svelte ecosystem equivalents (e.g., svelte-dnd-action)
- **BREAKING**: All existing Django and Playwright tests will need to be rewritten against the new API and frontend
- Add Node.js / SvelteKit as a frontend build dependency
- Add TypeScript for frontend type safety
- Django continues to serve as the backend — models, migrations, and business logic unchanged
- SQLite remains the database (Postgres migration is a separate future change)

## Capabilities

### New Capabilities
- `django-api`: JSON API layer replacing HTML-rendering views. Covers all existing CRUD operations, search, export, import, and reordering — returning JSON instead of HTML partials. Includes serialization, error responses, and CSRF/session handling.
- `svelte-frontend`: SvelteKit application providing the full UI. Three-panel layout, task management, drag-and-drop, keyboard navigation, markdown editing, emoji picker, toast notifications, search, projects page, timesheet page, import page. All current user-facing behavior preserved in Svelte components.

### Modified Capabilities
- FR-6 (HTMX Interactivity): Entirely replaced. Partial page updates, OOB swaps, and server-rendered toasts become Svelte component reactivity and client-side state management.
- FR-7 (Drag-and-Drop): Implementation changes from SortableJS + HTMX post-drop sync to a Svelte-native drag library with reactive state updates. User-facing behavior unchanged.
- NFR-5 (Optimistic/OOB updates): Implementation changes from HTMX OOB swaps to Svelte reactive stores with optimistic client-side state mutations and background API persistence.

## Impact

- **Templates**: All files in `templates/` and `tasks/templates/` are replaced by Svelte components
- **Static JS**: All files in `static/js/` are replaced by Svelte component logic
- **Static CSS**: Styles move to Svelte component scoped styles or a shared design system
- **Views**: All view functions in `tasks/views/` are rewritten as API endpoints returning JSON
- **URLs**: URL patterns change from returning HTML to serving API routes (e.g., `/api/lists/`, `/api/tasks/`)
- **Tests**: Django view tests rewritten to test JSON API responses; Playwright E2E tests rewritten against the Svelte frontend
- **Dependencies**: New — Node.js, SvelteKit, Vite, TypeScript, svelte-dnd-action. Removed — htmx.min.js, Sortable.min.js
- **Dev workflow**: Two processes needed — Django dev server (API) + Vite dev server (frontend). Production can be a single Django process serving built Svelte assets.
- **Models**: No changes. `tasks/models.py` is untouched.
- **Business logic**: No changes. Validation, cascade rules, position management stay in Django.
