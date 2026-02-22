## Why

We need a single unified application and data model so task data and network/contact data live together in one system, with a single Svelte UI and Django Ninja API. This enables cross-linking tasks to people/organizations and removes the split between the imported network app and the ToDo app.

## What Changes

- Merge the network app into the ToDo Django project and store all data in the ToDo SQLite database.
- Add bridge tables to relate tasks to people, organizations, and interactions (related-to semantics).
- Provide new Django Ninja API endpoints for people, organizations, interactions, and relationships.
- Rebuild network app pages (People, Organizations, Interactions, Relationships, Graph) in Svelte and remove Django template/HTMX views.
- Perform a one-time data integration with explicit backups (raw DB copies and `dumpdata` exports) from both apps before import.

## Capabilities

### New Capabilities
- `network-domain-model`: Unified schema for people/organizations/interactions plus bridge tables linking tasks to network entities.
- `network-api`: JSON API endpoints (Django Ninja) for network entities and task links.
- `network-frontend`: Svelte UI for network features, including the graph visualization.
- `data-integration`: One-time backup and data import process for merging the network app data into the unified database.

### Modified Capabilities
- `django-api`: Extend the existing API surface with network endpoints while preserving current task behavior (no changes to FR-1 through FR-10).
- `svelte-frontend`: Extend navigation and routes to include network features while preserving current task UI behavior (no changes to FR-1 through FR-10).

## Impact

- Backend: New Django app/models, migrations, and Ninja routers under `/api/`.
- Frontend: New Svelte routes/components and navigation updates.
- Data: One-time migration/import into `db.sqlite3` with backups generated for both apps.
- Removal: Network app’s Django template/HTMX views and related static assets will be removed from the unified product surface.

## Non-goals

- No user authentication or permissions changes.
- No deduplication or data cleaning between the two datasets.
- No redesign of existing task workflows or UI (existing FR-1 through FR-10 remain intact).
