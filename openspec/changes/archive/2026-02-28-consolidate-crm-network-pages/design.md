## Context

The app currently has 10 top-level navigation tabs, 6 of which are CRM/network-related: People, Organizations, Interactions, Relationships, Graph, and Leads. These pages share substantial duplicated code (~300+ lines across linked-tasks logic, page shell HTML, and CSS). The CRM pages (People, Orgs, Interactions, Leads) all follow the same list+detail pattern with identical scaffolding. The Network pages (Relationships, Graph) operate on the same underlying data but use completely different rendering paradigms (Svelte reactive CRUD vs. imperative D3).

## Goals / Non-Goals

**Goals:**
- Reduce top-level navigation from 10 to 6 tabs: Tasks, Dashboard, Projects, Timesheet, CRM, Network
- Extract duplicated CRM code into shared components
- Use SvelteKit nested routes for clean URLs (`/crm/people`, `/network/graph`)
- Preserve all existing entity-specific functionality unchanged

**Non-Goals:**
- Changing backend APIs or data models
- Adding new CRM/network features
- Refactoring entity-specific logic (follow-up tracking, graph visualization, etc.)
- Creating a shared reactive store between Relationships and Graph pages

## Decisions

### 1. Nested SvelteKit routes over query-param tabs

**Decision**: Use `+layout.svelte` at `/crm` and `/network` levels with nested `+page.svelte` files for each entity.

**Alternatives considered**:
- Query param tabs (`/crm?tab=people`): Simpler single-component approach, but loses deep-linking, browser back/forward semantics, and SvelteKit's built-in route-based code splitting.
- Client-side tab switching with `{#if}` blocks: Loads all entity code upfront regardless of which tab is active.

**Rationale**: Nested routes give real URLs (`/crm/people`), natural browser history, SvelteKit handles the layout persistence, and only the active sub-page's code loads. The sub-tab bar lives in the group `+layout.svelte`.

### 2. CRM layout owns the sub-tab bar and shared CSS only

**Decision**: The `/crm/+layout.svelte` renders a sub-tab bar and provides shared CSS via a `<style>` block. Entity pages remain self-contained `+page.svelte` files — they are moved from their current top-level location but keep their own state, forms, and detail panels.

**Alternatives considered**:
- Deep component extraction (generic `CRMList`, `CRMDetail` components with slot/prop-based entity configuration): Higher upfront effort, more abstraction layers, and the entity pages differ enough (People has tags/follow-up, Interactions has multi-select chips, Leads has autosave) that a generic wrapper would need many escape hatches.

**Rationale**: The biggest wins come from deduplicating CSS and the linked-tasks logic. Moving pages under a shared layout achieves the navigation goal. Entity-specific components can be extracted incrementally later if desired.

### 3. Extract linked-tasks logic into a shared module

**Decision**: Create a `linkedTasks.ts` utility module in `frontend/src/lib/components/shared/` that exports `createLinkedTasksManager(entityType)` returning the `loadAllTasks`, `loadLinkedTasks`, `addTaskLink`, `removeTaskLink`, and `taskName` functions. Each CRM page calls this factory once.

**Alternatives considered**:
- Svelte store for linked tasks: Overkill — linked tasks are per-entity-instance, not global state.
- Keep duplicated: Works but violates DRY with 4 copies of identical logic.

**Rationale**: A plain TypeScript function factory is the simplest approach. No new Svelte paradigms, just extracting identical code into one place.

### 4. Extract shared CRM CSS into a stylesheet

**Decision**: Create `frontend/src/lib/styles/crm.css` containing the ~200 lines of duplicated CSS (`.network-page`, `.network-grid`, `.panel`, `.create-form`, `.list`, `.list-item`, `.detail-header`, `.detail-form`, `.danger`, `.linked-tasks-section`, `.empty-state`, responsive breakpoint). Import it in `/crm/+layout.svelte`. Rename `.network-page` → `.crm-page` and `.network-grid` → `.crm-grid` for clarity.

**Alternatives considered**:
- Keep CSS in each page with `@use` shared partials: More complex build setup.
- Global CSS in `app.css`: Pollutes global namespace.

**Rationale**: A single imported stylesheet in the CRM layout scopes styles to CRM pages without global pollution. Class renaming reflects the new context.

### 5. Network layout is minimal — just a tab bar

**Decision**: `/network/+layout.svelte` is a thin wrapper with a sub-tab bar. The Relationships and Graph pages move under it essentially unchanged. No shared code extraction needed — these pages have completely different component trees and state management.

**Rationale**: Relationships is Svelte reactive CRUD; Graph is imperative D3 with zero Svelte components after mount. Forcing shared abstractions would add complexity with no benefit. The consolidation is purely navigational.

### 6. Root group routes redirect to default sub-page

**Decision**: `/crm/+page.svelte` redirects to `/crm/people` and `/network/+page.svelte` redirects to `/network/relationships` using SvelteKit's `goto()` in `onMount`.

**Alternatives considered**:
- SvelteKit `+page.server.ts` with `redirect()`: Requires server-side handling, but we're using `adapter-static` so this won't work.
- `+layout.ts` load function with redirect: Also SSR-dependent.

**Rationale**: Client-side redirect via `goto()` is the standard pattern for SPA-mode SvelteKit with `adapter-static`.

### 7. Active state highlighting uses `$page.url.pathname` prefix matching

**Decision**: Navbar tabs for CRM and Network use `pathname.startsWith('/crm')` and `pathname.startsWith('/network')` for active state. Sub-tab bars use exact path matching.

**Rationale**: This is the standard SvelteKit pattern for nested route active states and requires no additional state management.

## Risks / Trade-offs

- **Large diff, many files touched**: Moving 6 pages + updating layout + extracting shared code is a significant changeset. → Mitigated by keeping entity page logic unchanged (move, don't rewrite).
- **Broken internal links**: Any hardcoded references to `/people`, `/organizations`, etc. in code or tests will break. → Mitigated by grep-searching for old paths and updating all references.
- **CSS class rename (.network-* → .crm-*)**: Could miss references. → Mitigated by keeping changes scoped to the moved files where the classes are defined and used.
- **E2E test breakage**: Tests targeting old routes will fail. → Update paths in e2e test files.
- **Mobile bottom nav complexity**: 6 items is better than 10, but CRM/Network sub-tabs need to be discoverable on mobile. → Sub-tab bar renders inside the page content area, naturally visible after tapping the parent nav item.
