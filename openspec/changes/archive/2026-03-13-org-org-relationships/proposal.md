## Why

The network module tracks relationships between people and between organizations and people, but has no way to capture organization-to-organization relationships (partnerships, subsidiaries, vendor/client, competitors). This is a gap in the network model that limits the graph's usefulness for understanding how organizations relate to each other.

## What Changes

- Add a new `RelationshipOrganizationOrganization` model with symmetric semantics (org_1 < org_2 ordering, like person-person relationships)
- Add a new `OrgOrgRelationshipType` lookup table for categorizing org-org relationships
- Add full CRUD API endpoints for org-org relationships and their types, mirroring existing relationship patterns
- Replace the side-by-side two-panel relationships UI with a tabbed layout (Person ↔ Person | Org → Person | Org ↔ Org)
- Add `organization-organization` edge type to the network graph

## Non-goals

- Directional org-org relationships (using symmetric only, like person-person)
- Changing existing person-person or org-person relationship behavior
- Hierarchical org structures (parent/child trees) - flat relationships only

## Capabilities

### New Capabilities
- `org-org-relationships`: Organization-to-organization relationship model, API, and management UI
- `relationship-tabs`: Tabbed layout for the relationships page replacing side-by-side panels

### Modified Capabilities
- `network-domain-model`: Adding new relationship entity and type to the domain model
- `network-api`: Adding org-org relationship and type CRUD endpoints
- `network-frontend`: Adding org-org tab and switching to tabbed layout

## Impact

- **Backend models**: New `RelationshipOrganizationOrganization` and `OrgOrgRelationshipType` models in `network/models/relationship/`
- **API**: New router or endpoints in `network/api/` for org-org relationships and types
- **Frontend**: `frontend/src/routes/network/relationships/+page.svelte` rewritten with tab navigation
- **Frontend API client**: New types and API methods for org-org relationships
- **Graph**: `network/api/graph.py` updated to include org-org edges
- **Database**: New migration for the two new tables
