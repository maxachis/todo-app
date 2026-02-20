## 1. Backup + Import Prep

- [x] 1.1 Document backup locations and commands for raw DB copies and `dumpdata` exports (ToDo `db.sqlite3`, network `import/network-app/src/db.sqlite3`).
- [x] 1.2 Add a repeatable import checklist to the repo (paths, order of operations) for unified DB import.

## 2. Merge Network App into Django Project

- [x] 2.1 Move network app code into the main Django project (models, migrations, views, urls, templates) and update `INSTALLED_APPS` in `todoapp/settings.py`.
- [x] 2.2 Wire network app URLs under the Django project (API-only; no template routes).
- [x] 2.3 Remove or disable network template/HTMX views and static references so only API endpoints remain.

## 3. Unified Data Model + Migrations

- [x] 3.1 Add bridge models: `TaskPerson`, `TaskOrganization`, `InteractionTask` with FK fields and timestamps in a new `network` (or shared) app models file.
- [x] 3.2 Create and run migrations for network models and bridge models in the unified database.
- [x] 3.3 Verify model relations (FKs, constraints) and add indexes needed for network list queries.

## 4. Django Ninja API for Network Features

- [x] 4.1 Add schemas for network entities and link tables in `tasks/api/schemas.py` or a new `network/api/schemas.py`.
- [x] 4.2 Implement Ninja routers for people, organizations, org types, interaction types, interactions, and relationships.
- [x] 4.3 Implement Ninja endpoints for task links: link/unlink people, organizations, and interactions to tasks.
- [x] 4.4 Add API routes to `tasks/api/__init__.py` (or new module) and add tests for basic CRUD and linking.

## 5. Svelte UI for Network Features

- [x] 5.1 Add Svelte routes and navigation entries for People, Organizations, Interactions, Relationships, and Graph (update layout/nav components).
- [x] 5.2 Implement list and detail views for People, Organizations, and Interactions using the new API endpoints.
- [x] 5.3 Implement Relationships UI (person-person, org-person) with create/delete flows.
- [x] 5.4 Recreate the graph visualization in Svelte with parity to the legacy network app.

## 6. Data Import Execution + Verification

- [ ] 6.1 Run backups (raw DB + `dumpdata`) and store outputs in a documented location.
- [ ] 6.2 Load network `dumpdata` into unified DB and verify counts for people, orgs, interactions, and relationships.
- [ ] 6.3 Smoke test Svelte network pages and API endpoints against imported data.

## 7. Cleanup + Docs

- [x] 7.1 Remove unused network app HTMX templates and static assets from the unified app surface.
- [x] 7.2 Update README/NOTES with new network features, API endpoints, and migration steps.
- [x] 7.3 Update SPECS.md if needed to reflect unified model and new navigation links.
