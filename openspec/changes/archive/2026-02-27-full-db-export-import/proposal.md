## Why

There is no way to export the entire database (tasks + network/CRM data) as a single portable backup. The existing export only covers task data (lists, sections, tasks) and ignores people, organizations, interactions, relationships, projects, time entries, leads, and all cross-entity links. A full-database export enables manual backups, migration between instances, and disaster recovery — and the import path must accept the same format to complete the round-trip.

## What Changes

- Add a new **"Export Database"** action in the settings dropdown that downloads a single JSON file containing every model across both Django apps (`tasks` and `network`)
- The export format is a structured JSON object with top-level keys per entity type (lists, tasks, people, organizations, interactions, relationships, projects, time entries, leads, tags, entity links, etc.), preserving all fields and foreign-key references
- Extend the existing **import endpoint** to accept this full-database JSON format, detect it by a format marker/envelope key, and restore all entities with correct relational integrity (creating in dependency order)
- Add an **"Export Database"** link/button to the settings dropdown in the frontend, triggering a browser download
- The existing per-list JSON/CSV/Markdown export and the existing import formats (native JSON, native CSV, TickTick CSV) remain unchanged

## Non-goals

- Automatic/scheduled backups — this is manual, on-demand only
- Binary/SQLite file download — the export is structured JSON, not a raw DB copy
- Selective export (pick which entities to include) — it's all-or-nothing
- Schema migration handling — the export assumes the same app version on import
- Overwrite/replace mode on import — import creates new records (with duplicate detection where applicable)

## Capabilities

### New Capabilities
- `full-db-export`: API endpoint and serialization logic to export the entire database (tasks app + network app) as a single structured JSON file
- `full-db-import`: Detection and import logic for the full-database JSON format, restoring all entity types with relational integrity

### Modified Capabilities
- `settings-menu`: Add an "Export Database" action to the settings dropdown alongside the existing "Import" link

## Impact

- **Backend**: New API endpoint (`/api/export/full/` or similar) with serializers covering all models in `tasks` and `network` apps. Extension to `tasks/api/import_tasks.py` (or new import service) to handle the full-database format.
- **Frontend**: New settings dropdown item in `+layout.svelte` triggering the export download. The existing `/import` page needs no changes if the import endpoint auto-detects the new format (same as it already auto-detects native JSON vs CSV vs TickTick).
- **Models affected**: All models across both apps — List, Section, Task, Tag, Project, ProjectLink, TimeEntry (tasks app); Person, Organization, OrgType, Interaction, InteractionType, Lead, LeadTask, TaskPerson, TaskOrganization, InteractionTask, RelationshipPersonPerson, RelationshipOrganizationPerson (network app).
- **Dependencies**: No new packages required — uses Django ORM and stdlib `json`.
