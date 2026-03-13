## Why

The relationships UI is split across two locations: `/crm/relationships` (Person↔Person and Org→Person in a side-by-side grid) and `/network/relationships` (all three relationship types with sub-tabs, including Org↔Org). The CRM version is missing Org↔Org, and the network version is unreachable — the Network layout has no sub-tab navigation, and `/network` redirects straight to `/network/graph`. Consolidating into CRM provides a single, discoverable location for all relationship management.

## What Changes

- Replace the CRM relationships page (`/crm/relationships/+page.svelte`) with the more complete network version that has sub-tabs for Person↔Person, Org→Person, and Org↔Org
- Remove the orphaned network relationships page (`/network/relationships/+page.svelte`)
- No backend changes — all three API endpoint groups already exist and work

## Capabilities

### New Capabilities

_(none — this consolidates existing UI, not new behavior)_

### Modified Capabilities

- `network-frontend`: Relationships view moves from `/network/relationships` to `/crm/relationships`; the `/network` route group loses its relationships sub-page
- `crm-route-group`: The `/crm/relationships` page gains Org↔Org support and switches from side-by-side grid to tabbed layout

## Non-goals

- Changing the relationship data model or API
- Adding navigation sub-tabs to the Network layout (Graph stays as the sole Network page)
- Refactoring the relationships page into smaller components (can be done later)

## Impact

- **Frontend routes**: `/crm/relationships/+page.svelte` rewritten, `/network/relationships/+page.svelte` deleted
- **Navigation**: No changes needed — CRM layout already has the "Relationships" tab; Network layout has no tab bar to update
- **Specs**: Minor updates to `network-frontend` and `crm-route-group` specs to reflect new location
