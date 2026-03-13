## Context

The network module currently supports two relationship types: person-person (symmetric) and organization-person (directional). These are stored in separate models with separate type lookup tables. The relationships page displays both in a side-by-side two-panel grid layout. The network graph renders both as edges between nodes.

Adding org-org relationships introduces a third relationship kind following the same patterns.

## Goals / Non-Goals

**Goals:**
- Add org-org relationships following the established symmetric pattern (like person-person)
- Provide a clean tabbed UI that scales to three relationship kinds
- Include org-org edges in the network graph

**Non-Goals:**
- Unifying the three relationship models into a polymorphic structure
- Directional org-org relationships or hierarchical org trees
- Changing any existing relationship behavior

## Decisions

### 1. Symmetric model with ordered IDs

**Decision**: Use `org_1_id < org_2_id` constraint, identical to person-person.

**Rationale**: Org-org relationships are inherently bidirectional ("Acme partners with Globex"). The person-person pattern is proven and handles deduplication cleanly via the ordering constraint. Relationship types carry the semantic meaning.

**Alternative considered**: Directional model (like org-person) - rejected because most org-org relationship types are symmetric, and directionality can be inferred from context/type name.

### 2. Separate OrgOrgRelationshipType table

**Decision**: New `OrgOrgRelationshipType` model, following the existing pattern of one type table per relationship kind.

**Rationale**: Keeps type lists independent (org-org types like "partner", "subsidiary", "competitor" don't overlap with person-person types like "friend", "colleague"). Consistent with existing architecture.

**Alternative considered**: Unified relationship type table with a `kind` discriminator - would require migrating existing data and changing existing API contracts for no real benefit.

### 3. Tabbed UI replacing side-by-side panels

**Decision**: Replace the `.network-grid` two-column layout with tabs: "Person ↔ Person", "Org → Person", "Org ↔ Org". Each tab shows the full-width create form, filter, and list for that relationship kind.

**Rationale**: Three side-by-side panels are too cramped at typical viewport widths. Tabs give each relationship kind full width and match the sub-tab patterns already used in CRM and Network sections. State for inactive tabs is preserved in component variables.

**Implementation**: In-page tabs using a reactive `activeTab` variable (not separate routes), since all data is already loaded in `onMount` and shared state (people, organizations) is needed across tabs.

### 4. Graph edge type

**Decision**: Add `organization-organization` edge type in graph API response, with source/target as `organization-{id}` nodes.

**Rationale**: Straightforward extension of existing graph data structure. No changes needed to how nodes are rendered - org nodes already exist. Just adds new edges between them.

## Risks / Trade-offs

- **Tab state loss on switch**: Partially-filled create forms reset when switching tabs. Mitigation: state variables persist across tab switches since they're component-level, not DOM-level. Svelte reactivity handles this naturally.
- **Data loading**: All three relationship lists load on mount regardless of active tab. For a personal app with modest data volumes, this is fine and avoids loading spinners on tab switch.
