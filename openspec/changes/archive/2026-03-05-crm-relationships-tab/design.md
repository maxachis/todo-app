## Context

The CRM section at `/crm` has sub-tabs: Inbox, People, Orgs, Interactions, Leads. The Network section at `/network` has sub-tabs: Relationships, Graph. Relationships manage person-person and org-person connections — data that belongs with CRM entities.

## Goals / Non-Goals

**Goals:**
- Move Relationships from Network to CRM as a new sub-tab
- Simplify Network to Graph-only

**Non-Goals:**
- Changing relationship page functionality
- Backend API changes
- Removing the Network top-nav item

## Decisions

### 1. Move the Svelte route file

**Decision**: Move `frontend/src/routes/network/relationships/+page.svelte` to `frontend/src/routes/crm/relationships/+page.svelte`. The page component is self-contained and doesn't depend on the Network layout for anything.

### 2. Tab placement in CRM

**Decision**: Add "Relationships" tab after "Leads" in the CRM sub-tab bar. Order: Inbox, People, Orgs, Interactions, Leads, Relationships.

**Rationale**: Relationships are a cross-cutting view across people and orgs, so placing it last keeps the entity-focused tabs (People, Orgs) prominent.

### 3. Network layout simplification

**Decision**: Keep the Network top-nav tab and layout, but with only Graph remaining. Remove the sub-tab bar since there's only one sub-route. Redirect `/network` to `/network/graph`.

**Alternative considered**: Remove Network entirely and move Graph to a top-level route — rejected because it's a larger change and the Network grouping still makes conceptual sense for graph visualization.

## Risks / Trade-offs

- **Bookmarks/links**: Any existing bookmarks to `/network/relationships` will break. Since this is a single-user personal app, this is acceptable. Could add a redirect but it's unnecessary complexity.
- **CRM tab count**: Goes from 5 to 6 sub-tabs, which may feel crowded on narrow screens. The existing CSS handles horizontal overflow gracefully.
