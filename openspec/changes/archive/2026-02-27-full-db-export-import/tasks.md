## 1. Full Database Export Service

- [x] 1.1 Create `tasks/services/full_export.py` with serialization functions for every model in `tasks` app (Project, ProjectLink, List, Section, Tag, Task, TimeEntry) — each entity includes `id` and all fields, FKs as `*_id`, M2M as `*_ids` arrays
- [x] 1.2 Add serialization functions for every model in `network` app (Person, Organization, OrgType, Interaction, InteractionType, Lead, LeadTask, TaskPerson, TaskOrganization, InteractionTask, RelationshipPersonPerson, RelationshipOrganizationPerson)
- [x] 1.3 Add top-level `export_full_database()` function that builds the envelope JSON with `format`, `version`, `exported_at`, and all entity collections (empty arrays for missing data)

## 2. Export API Endpoint

- [x] 2.1 Add `GET /api/export/full/` route in `tasks/api/export.py` that calls `export_full_database()` and returns the JSON with `Content-Disposition: attachment; filename="nexus-backup.json"`

## 3. Full Database Import Service

- [x] 3.1 Create `tasks/services/full_import.py` with `import_full_database(data: dict)` function that processes entity collections in dependency order, maintaining `old_id → new_id` mappings per entity type
- [x] 3.2 Implement import for independent entities: tags (by name), org_types (by name), interaction_types (by name), projects (by name), people (by first_name+last_name)
- [x] 3.3 Implement import for FK-dependent entities: organizations (FK→OrgType), lists (FK→Project nullable), project_links (FK→Project), sections (FK→List)
- [x] 3.4 Implement task tree import: sort by parent_id (nulls first, then by depth), create with section_id and parent_id remapping, attach tag M2M
- [x] 3.5 Implement import for remaining entities: time_entries (FK→Project, M2M→Task), interactions (FK→Person, InteractionType), leads (FK→Person, Organization)
- [x] 3.6 Implement import for join/link tables: lead_tasks, relationships_person_person, relationships_organization_person, task_persons, task_organizations, interaction_tasks
- [x] 3.7 Wrap entire import in `transaction.atomic()` and return stats dict with per-entity-type created/skipped counts plus errors

## 4. Import Endpoint Integration

- [x] 4.1 Update `tasks/api/import_tasks.py` to detect `"format": "nexus-full-backup"` in parsed JSON and route to `import_full_database()` before falling through to `import_native_json()`

## 5. Frontend Settings Dropdown

- [x] 5.1 Add "Export Database" item to `settingsItems` in `frontend/src/routes/+layout.svelte` — use an `<a>` tag with `href="/api/export/full/"` and `download` attribute so it triggers a file download and closes the dropdown

## 6. Tests

- [x] 6.1 Add API test for `GET /api/export/full/` in `tasks/tests/` — verify envelope structure, entity keys, Content-Disposition header, and field completeness for a populated database
- [x] 6.2 Add round-trip test: export full DB, clear all tables, import the exported JSON, verify record counts match and FK relationships are intact
- [x] 6.3 Add test for format detection: verify that uploading a full-backup JSON to `/api/import/` routes correctly and that a regular list JSON still uses the old import path
- [x] 6.4 Add duplicate-detection test: import same backup twice, verify second import skips all entities and creates nothing new
