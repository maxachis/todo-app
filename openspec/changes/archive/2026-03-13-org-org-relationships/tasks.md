## 1. Backend Models & Migration

- [x] 1.1 Create `OrgOrgRelationshipType` model in `network/models/relationship/org_org_type.py` with `name` CharField
- [x] 1.2 Create `RelationshipOrganizationOrganization` model in `network/models/relationship/organization_organization.py` with `org_1`/`org_2` FKs, `relationship_type` FK, `notes`, timestamps, symmetric constraints (no-self, ordering, uniqueness), and `save()` normalization
- [x] 1.3 Export new models from `network/models/relationship/__init__.py` and `network/models/__init__.py`
- [x] 1.4 Run `makemigrations` and `migrate` for the two new tables

## 2. Backend API

- [x] 2.1 Add Ninja schemas in `network/api/schemas.py`: `OrgOrgRelationshipTypeSchema`, `RelationshipOrganizationOrganizationSchema`, `RelationshipOrganizationOrganizationCreateInput`, `RelationshipOrganizationOrganizationUpdateInput`
- [x] 2.2 Add org-org relationship type endpoints (list, create) to `network/api/relationship_types.py`
- [x] 2.3 Add org-org relationship CRUD endpoints (list, create, update, delete) to `network/api/relationships.py`
- [x] 2.4 Update `network/api/graph.py` to include `organization-organization` edges from `RelationshipOrganizationOrganization`

## 3. Frontend API Client

- [x] 3.1 Add TypeScript types in `frontend/src/lib/api/types.ts`: `RelationshipOrganizationOrganization`, `OrgOrgRelationshipType`
- [x] 3.2 Add API methods in `frontend/src/lib/api/client.ts`: `api.relationships.orgOrg` (getAll, create, update, remove) and `api.relationshipTypes.orgOrg` (getAll, create)
- [x] 3.3 Export new types from `frontend/src/lib/api/index.ts`

## 4. Frontend UI - Tabbed Layout

- [x] 4.1 Refactor `frontend/src/routes/network/relationships/+page.svelte`: replace `.network-grid` two-column layout with tab navigation (Person ↔ Person, Org → Person, Org ↔ Org) using a reactive `activeTab` variable
- [x] 4.2 Move existing person-person panel content into the first tab
- [x] 4.3 Move existing org-person panel content into the second tab
- [x] 4.4 Add tab styles matching existing sub-tab patterns in the app

## 5. Frontend UI - Org ↔ Org Tab

- [x] 5.1 Add org-org state variables, derived filters, and data loading (mirror person-person pattern)
- [x] 5.2 Add org-org create form with Organization A typeahead, multi-select Organization B, type typeahead with inline creation, and notes textarea
- [x] 5.3 Add org-org filter row with organization typeahead and auto-sync from Organization A
- [x] 5.4 Add org-org relationship list with inline type editing, notes editing, and delete
- [x] 5.5 Wire up org-org CRUD functions (create, update type, edit notes, delete)

## 6. Verification

- [x] 6.1 Run `cd frontend && npm run check` to verify TypeScript types and Svelte compilation
- [x] 6.2 Test org-org relationship CRUD through the UI manually
- [x] 6.3 Verify graph renders org-org edges between organization nodes
- [x] 6.4 Verify tab switching preserves form state across all three tabs
