## Context

The app currently exports task data only (lists, sections, tasks with subtasks, tags) via `/api/export/{fmt}/` in JSON, CSV, and Markdown formats. Import supports native JSON, native CSV, and TickTick CSV — all task-only. The network/CRM domain (people, organizations, interactions, relationships, leads) and project/timesheet data have no export or import path.

The database has ~20 models across two Django apps (`tasks` and `network`) with foreign keys, M2M relationships, self-referential trees (Task.parent), and cross-app links (TaskPerson, InteractionTask, LeadTask).

## Goals / Non-Goals

**Goals:**
- Single-endpoint full database export as structured JSON
- Round-trip import: export → import restores all data with relational integrity
- Auto-detection of the new format in the existing import endpoint
- "Export Database" action accessible from the settings dropdown

**Non-Goals:**
- Incremental/delta export (always full dump)
- Raw SQLite binary download
- Selective entity filtering
- Schema versioning or cross-version migration
- Overwrite/replace semantics on import (additive with duplicate detection)
- Separate UI page for full export (just a settings menu action that triggers download)

## Decisions

### 1. Export format: envelope JSON with entity collections

The export file is a single JSON object with a format marker and flat entity collections:

```json
{
  "format": "nexus-full-backup",
  "version": 1,
  "exported_at": "2026-02-27T12:00:00Z",
  "tags": [...],
  "org_types": [...],
  "interaction_types": [...],
  "projects": [...],
  "project_links": [...],
  "people": [...],
  "organizations": [...],
  "lists": [...],
  "sections": [...],
  "tasks": [...],
  "time_entries": [...],
  "interactions": [...],
  "leads": [...],
  "lead_tasks": [...],
  "relationships_person_person": [...],
  "relationships_organization_person": [...],
  "task_persons": [...],
  "task_organizations": [...],
  "interaction_tasks": [...]
}
```

Each entity includes its database `id` so that foreign-key references between collections resolve correctly on import. Tasks include `parent_id` (nullable) for tree reconstruction.

**Alternative considered**: Django `dumpdata` — rejected because it produces a flat fixture format that's harder to validate, doesn't support duplicate detection, and ties the format to Django internals.

**Alternative considered**: Nested/hierarchical structure (lists → sections → tasks) — rejected because it duplicates the existing per-list JSON format and makes cross-entity links (TaskPerson, InteractionTask) awkward to represent.

### 2. Import order: topological sort by FK dependencies

Import proceeds in dependency order to satisfy FK constraints:

1. Tags, OrgTypes, InteractionTypes (no FK deps)
2. Projects
3. People
4. Organizations (FK → OrgType)
5. Lists (FK → Project, nullable)
6. ProjectLinks (FK → Project)
7. Sections (FK → List)
8. Tasks — sorted so parents come before children (root tasks first, then depth-1, etc.)
9. TimeEntries (FK → Project, M2M → Task)
10. Interactions (FK → Person, InteractionType)
11. Leads (FK → Person, Organization, both nullable)
12. LeadTasks (FK → Lead, Task)
13. RelationshipPersonPerson, RelationshipOrganizationPerson
14. TaskPerson, TaskOrganization, InteractionTask

An `old_id → new_id` mapping is maintained per entity type so that FK references from the export file resolve to newly created database records.

### 3. Format detection via envelope key

The existing import endpoint (`/api/import/`) reads `.json` files and passes them to `import_native_json`. The full-DB format is detected by checking for `"format": "nexus-full-backup"` at the top level. If present, route to the new `import_full_database` service. Otherwise, fall through to the existing per-list import logic.

This requires no changes to the file upload flow — the same `/import` page and endpoint handle both formats transparently.

### 4. Duplicate detection strategy

Each entity type uses its natural key for duplicate detection:
- **Tags**: `name` (unique)
- **OrgTypes / InteractionTypes**: `name`
- **People**: `(first_name, last_name)` (unique constraint)
- **Organizations**: `name` (unique constraint)
- **Projects**: `name`
- **Lists**: `name`
- **Sections**: `(list, name)`
- **Tasks**: `(section, title, parent)` — same as existing native import
- **Interactions**: `(person, interaction_type, date)`
- **Leads**: `title`
- **Link/join tables**: their composite unique constraints

On duplicate, the existing record is reused (its ID enters the mapping) and no update is performed. Import stats track `*_skipped` counts.

### 5. Frontend: settings dropdown action triggering download

Add an "Export Database" item to the settings dropdown in `+layout.svelte`. On click, navigate to `/api/export/full/` which returns the JSON file with `Content-Disposition: attachment`. This uses the same browser-download pattern as the existing per-list export (no fetch + blob needed).

### 6. API endpoint placement

Add `GET /api/export/full/` in `tasks/api/export.py` alongside the existing per-list export endpoints. The serialization logic lives in a new `tasks/services/full_export.py` service module. The import logic lives in a new `tasks/services/full_import.py` service module, called from the existing `tasks/api/import_tasks.py` router.

## Risks / Trade-offs

- **Large databases**: For very large datasets, the entire JSON is built in memory. → Acceptable for a single-user app; SQLite databases are typically small.
- **ID remapping complexity**: The import must maintain old→new ID maps across ~15 entity types. → Straightforward dict-based mapping; tested per entity type.
- **M2M fields** (Task.tags, TimeEntry.tasks): These require separate handling after the primary record is created. → Process M2M assignments as a final step within each entity type's import.
- **Task tree ordering**: Self-referential parent FK requires importing root tasks first. → Sort tasks by depth (null parent first) or process parent_id=null first, then link children.
- **Atomic import**: If any entity fails mid-import, partial data remains. → Wrap entire import in `transaction.atomic()`.
