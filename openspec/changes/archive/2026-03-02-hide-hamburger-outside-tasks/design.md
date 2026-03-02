## Context

The global layout (`+layout.svelte`) renders two `.mobile-only` toggle buttons in the top navbar: a hamburger (☰) for the sidebar and a vertical ellipsis (⋮) for the detail panel. These buttons are CSS-hidden on desktop (≥1024px) and shown on mobile (≤1023px). However, the sidebar (`<aside id="sidebar">`) and detail panel they control are only rendered inside an `{#if isTasksRoute}` block. On non-task routes, the buttons are visible but inert.

## Goals / Non-Goals

**Goals:**
- Hide the two mobile-only toggle buttons when not on the Tasks route, eliminating dead controls.

**Non-Goals:**
- Adding mobile navigation to other routes.
- Changing any desktop layout behavior.
- Restructuring the layout component.

## Decisions

**1. Wrap buttons in the existing `isTasksRoute` guard**
The layout already has `const isTasksRoute = $derived($page.url.pathname === '/');` and uses it for the sidebar/detail panel sections. Wrap both `.mobile-only` buttons in `{#if isTasksRoute}` blocks. This is the simplest approach — no new state, no new derived values, just conditional rendering of existing elements using an existing reactive variable.

Alternative considered: CSS-only approach using route-based body classes — rejected as unnecessarily indirect when Svelte conditional rendering is already the established pattern.

## Risks / Trade-offs

- [Minimal risk] If a future route needs these buttons, they'll need to be re-exposed. Acceptable since each route's mobile UX should be designed intentionally rather than inheriting task-specific controls.
