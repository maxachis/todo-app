## Why

Relationships (person-to-person and org-to-person) are fundamentally CRM data — they describe connections between people and organizations. Currently they live under `/network/relationships`, separated from the CRM entities they relate to. Moving the Relationships tab into the CRM group (`/crm/relationships`) puts it alongside People, Orgs, Interactions, and Leads where users naturally expect it. This also simplifies the Network section to focus solely on the Graph visualization.

## Non-goals

- Changing the relationships page functionality, layout, or API
- Removing the Network top-nav tab (it still has Graph)
- Changing any relationship data model or backend API routes

## Capabilities

### New Capabilities

(none — this is a route reorganization)

### Modified Capabilities

- `crm-route-group`: Add `/crm/relationships` sub-route and "Relationships" sub-tab to CRM navigation
- `network-route-group`: Remove `/network/relationships` sub-route; Network becomes Graph-only (redirect `/network` to `/network/graph`)

## Impact

- **Frontend routes**: Move `frontend/src/routes/network/relationships/+page.svelte` to `frontend/src/routes/crm/relationships/+page.svelte`
- **CRM layout**: Add "Relationships" tab to CRM sub-tab navigation
- **Network layout**: Remove "Relationships" tab; redirect `/network` to `/network/graph`; if only Graph remains, the Network sub-tab bar can be simplified or removed
- **Top navbar**: No change (both CRM and Network remain)
- **No backend changes**: API routes for relationships stay at `/api/relationships/` unchanged
