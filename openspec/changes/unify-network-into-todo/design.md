## Context

The ToDo app is a Django + SvelteKit application with a JSON API implemented via Django Ninja and a SQLite database. The network app is a separate Django project using Django templates + HTMX, with its own SQLite database and data export. The goal is to merge the network app into the ToDo project, unify data in the ToDo database, and rebuild the network UI in Svelte while keeping existing task functionality intact.

Key constraints: single-user, no auth, no deduping, and removal of Django template/HTMX views for network features. Data must be backed up in raw DB form and via `dumpdata` before integration.

## Goals / Non-Goals

**Goals:**
- Merge network models into the ToDo Django project and migrate them into the unified SQLite database.
- Add explicit bridge tables to link tasks to people, organizations, and interactions (related-to semantics).
- Provide Django Ninja API endpoints for network entities and the new link tables.
- Rebuild network pages (People, Organizations, Interactions, Relationships, Graph) in Svelte.
- Perform a one-time backup + import of network data into the unified DB.

**Non-Goals:**
- Authentication/authorization changes.
- Deduplication or data cleansing.
- Redesigning existing task workflows or UI.
- Preserving Django template/HTMX views for network features.

## Decisions

1. **Single Django project with unified SQLite DB**
   - **Decision:** Move the network app into the ToDo project and use the ToDo `db.sqlite3` as the unified database.
   - **Alternatives considered:** Keep two Django projects and sync data; keep network DB separate.
   - **Why:** Simplifies data access and supports cross-linking tasks to people/orgs without multi-DB complexity.

2. **Explicit bridge tables for links**
   - **Decision:** Create three new models: `TaskPerson`, `TaskOrganization`, `InteractionTask` with FKs and timestamps.
   - **Alternatives considered:** Generic FK link table; embedding fields directly on Task/Interaction.
   - **Why:** Clear, typed relationships without ContentTypes complexity; preserves existing schemas.

3. **API style: Django Ninja**
   - **Decision:** Implement new network endpoints and link endpoints using Django Ninja routers.
   - **Alternatives considered:** Django REST Framework; template/HTMX endpoints.
   - **Why:** Consistency with existing API patterns and simpler integration with Svelte.

4. **Frontend unification in Svelte**
   - **Decision:** Rebuild network pages in Svelte and remove Django template/HTMX views.
   - **Alternatives considered:** Keep HTMX views; hybrid approach.
   - **Why:** Single UI framework and consistent user experience.

5. **One-time data integration with backups**
   - **Decision:** Generate raw DB copies and `dumpdata` exports for both apps, then import network data into the unified DB.
   - **Alternatives considered:** Direct DB attach/merge without logical export.
   - **Why:** Safer rollback and easier auditing of imported data; aligns with no-deduping requirement.

## Risks / Trade-offs

- **Risk:** Data import collisions (PK conflicts) when loading network data into unified DB. → **Mitigation:** Preserve network PKs via `dumpdata` and import into empty network tables; ensure sequences are updated post-import if needed.
- **Risk:** UI parity gaps when porting HTMX screens to Svelte. → **Mitigation:** Implement page-by-page with acceptance checks; keep graph visualization behavior identical.
- **Risk:** Removal of Django views breaks any hidden dependencies. → **Mitigation:** Audit URL usage and ensure Svelte routes replace all network routes.
- **Risk:** Migration complexity in a single database. → **Mitigation:** Run migrations on a clean copy of the ToDo DB, then import network data; document rollback steps.

## Migration Plan

1. Backup both databases (raw file copy) and export JSON via `dumpdata` for both apps.
2. Move network Django app code into this project and add it to `INSTALLED_APPS`.
3. Create migrations for network models and new bridge tables.
4. Migrate the unified database.
5. Verify data integrity (basic counts and FK integrity checks).
6. Build Svelte pages for network features and replace navigation.
7. Remove Django template/HTMX URLs and assets for network views.

## Open Questions

- Which graph visualization library is used in the network app, and do we keep the same implementation or re-create it in Svelte?
- Do we need a bulk-linking UI between tasks and people/orgs initially, or just per-entity linking?
