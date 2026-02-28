## Why

The top navbar has 10 tabs, 6 of which are CRM/network-related (People, Orgs, Interactions, Relationships, Graph, Leads). This crowds the navigation — especially on mobile — and obscures the conceptual grouping. The four CRM pages (People, Organizations, Interactions, Leads) also share ~300+ lines of duplicated code (linked tasks logic, page shell HTML, CSS). Consolidating into `/crm` and `/network` route groups reduces nav items from 10 to 6, improves mobile usability, and enables extracting shared code into reusable components.

## What Changes

- **New `/crm` route group** with nested sub-routes: `/crm/people`, `/crm/orgs`, `/crm/interactions`, `/crm/leads`. A shared CRM layout provides sub-tab navigation between entities.
- **New `/network` route group** with nested sub-routes: `/network/relationships`, `/network/graph`. A shared Network layout provides sub-tab navigation.
- **Shared CRM components extracted**: linked-tasks logic (loadAllTasks, addTaskLink, removeTaskLink, taskName), page shell CSS (~200 lines), list+detail layout pattern.
- **Top navbar updated** from 10 tabs to 6: Tasks, Dashboard, Projects, Timesheet, CRM, Network. Sub-tabs within CRM and Network handle entity switching.
- **Mobile bottom nav updated** to match the 6-tab structure.
- **Old standalone routes removed**: `/people`, `/organizations`, `/interactions`, `/relationships`, `/graph`, `/leads`.
- `/crm` redirects to `/crm/people`; `/network` redirects to `/network/relationships`.

## Non-goals

- No changes to backend API endpoints or data models.
- No changes to entity-specific functionality (follow-up tracking, graph visualization, etc.).
- No changes to the Tasks, Dashboard, Projects, or Timesheet pages.
- Not adding new features — this is purely a structural consolidation.

## Capabilities

### New Capabilities
- `crm-route-group`: Nested SvelteKit route group at `/crm` with shared layout, sub-tab navigation, and extracted common CRM components (linked tasks, shared CSS, list+detail shell).
- `network-route-group`: Nested SvelteKit route group at `/network` with shared layout and sub-tab navigation for Relationships and Graph.

### Modified Capabilities
- `svelte-frontend`: Navigation bar tabs change from 10 individual entries to 6 grouped entries. Mobile bottom nav updated accordingly. Active-state highlighting must account for nested route prefixes.
- `network-frontend`: Routes for People, Organizations, Interactions, Relationships, and Graph move under `/crm` or `/network` prefixes. All existing entity functionality preserved, but page components are restructured into sub-route modules.

## Impact

- **Frontend routes**: 6 top-level routes removed, 2 route groups with 6 nested routes added.
- **Frontend components**: New shared CRM layout, shared linked-tasks mixin/component, shared CRM CSS. Entity-specific components extracted from monolithic page files into focused sub-components.
- **Navigation**: `+layout.svelte` navbar and mobile bottom nav updated. Sub-tab bars added in CRM and Network layouts.
- **No backend changes**: All API endpoints remain at their current paths.
- **E2E tests**: Any tests referencing old route paths (`/people`, `/organizations`, etc.) will need path updates.
