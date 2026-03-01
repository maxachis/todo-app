## 1. Backend Models & Migration

- [x] 1.1 Create `PersonPersonRelationshipType` model in `network/models/relationship/` with `name` CharField(max_length=255) and `__str__` returning name
- [x] 1.2 Create `OrgPersonRelationshipType` model in `network/models/relationship/` with `name` CharField(max_length=255) and `__str__` returning name
- [x] 1.3 Add optional `relationship_type` ForeignKey to `RelationshipPersonPerson` → `PersonPersonRelationshipType` (null=True, blank=True, on_delete=SET_NULL)
- [x] 1.4 Add optional `relationship_type` ForeignKey to `RelationshipOrganizationPerson` → `OrgPersonRelationshipType` (null=True, blank=True, on_delete=SET_NULL)
- [x] 1.5 Export new models from `network/models/relationship/__init__.py` and `network/models/__init__.py`
- [x] 1.6 Register new type models in `network/admin.py`
- [x] 1.7 Run `makemigrations` and `migrate` to generate and apply the migration

## 2. Backend API — Relationship Type CRUD

- [x] 2.1 Add `PersonPersonRelationshipTypeSchema`, `PersonPersonRelationshipTypeCreateInput`, `PersonPersonRelationshipTypeUpdateInput` to `network/api/schemas.py`
- [x] 2.2 Add `OrgPersonRelationshipTypeSchema`, `OrgPersonRelationshipTypeCreateInput`, `OrgPersonRelationshipTypeUpdateInput` to `network/api/schemas.py`
- [x] 2.3 Create `network/api/relationship_types.py` router with list/create/update/delete endpoints for person-person types at `/relationship-types/people/` (following `org_types.py` pattern)
- [x] 2.4 Add list/create/update/delete endpoints for org-person types at `/relationship-types/organizations/` in the same router
- [x] 2.5 Register the new router in `network/api/__init__.py`

## 3. Backend API — Update Relationship Schemas

- [x] 3.1 Add optional `relationship_type_id` field to `RelationshipPersonPersonCreateInput` and `RelationshipPersonPersonUpdateInput` in `network/api/schemas.py`
- [x] 3.2 Add optional `relationship_type_id` field to `RelationshipOrganizationPersonCreateInput` and `RelationshipOrganizationPersonUpdateInput` in `network/api/schemas.py`
- [x] 3.3 Add `relationship_type_id` and `relationship_type_name` to `RelationshipPersonPersonSchema` and `RelationshipOrganizationPersonSchema` response schemas
- [x] 3.4 Update relationship create endpoints in `network/api/relationships.py` to accept and persist `relationship_type_id`
- [x] 3.5 Update relationship update endpoints in `network/api/relationships.py` to accept and persist `relationship_type_id`

## 4. Frontend — TypeScript Types & API Client

- [x] 4.1 Add `PersonPersonRelationshipType` and `OrgPersonRelationshipType` interfaces to `frontend/src/lib/api/types.ts`
- [x] 4.2 Update `RelationshipPersonPerson` and `RelationshipOrganizationPerson` interfaces to include `relationship_type_id` and `relationship_type_name`
- [x] 4.3 Add `api.relationshipTypes.people.getAll()` and `api.relationshipTypes.people.create()` methods to `frontend/src/lib/api/index.ts`
- [x] 4.4 Add `api.relationshipTypes.organizations.getAll()` and `api.relationshipTypes.organizations.create()` methods to `frontend/src/lib/api/index.ts`
- [x] 4.5 Update `api.relationships.people.create()` and `api.relationships.organizations.create()` payloads to include optional `relationship_type_id`
- [x] 4.6 Update `api.relationships.people.update()` and `api.relationships.organizations.update()` payloads to include optional `relationship_type_id`

## 5. Frontend — Relationships Page UI

- [x] 5.1 Add relationship type state and fetch calls (`onMount`) for both person-person and org-person types in `frontend/src/routes/network/relationships/+page.svelte`
- [x] 5.2 Add `handleCreatePersonPersonRelType` and `handleCreateOrgPersonRelType` inline creation handlers (following the `handleCreateInteractionType` pattern)
- [x] 5.3 Add TypeaheadSelect for person-person relationship type in the person-person create form (after Person B chips, before notes)
- [x] 5.4 Add TypeaheadSelect for org-person relationship type in the org-person create form (after Person chips, before notes)
- [x] 5.5 Include `relationship_type_id` in the create payloads when submitting new relationships
- [x] 5.6 Display relationship type name as a label in each relationship list row
- [x] 5.7 Add inline TypeaheadSelect editing for relationship type on existing relationships (click type label/area to edit, save on selection)

## 6. Verification

- [x] 6.1 Run `npm run check` in `frontend/` to verify TypeScript compilation
- [x] 6.2 Run existing backend API tests to verify no regressions
- [ ] 6.3 Manual smoke test: create relationship types, create relationships with types, edit types inline, verify list display
