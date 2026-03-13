## Context

The app currently sets a static document title. The upcoming store already fetches tasks with due dates from `/api/upcoming/`, grouping them by time horizon (Overdue, Today, Tomorrow, etc.). The layout component (`+layout.svelte`) manages global UI concerns like the navbar and theme.

## Goals / Non-Goals

**Goals:**
- Show a live count of actionable tasks (overdue + due today) in the browser tab title
- Update reactively as tasks are completed, added, or rescheduled
- Keep implementation minimal — reuse existing data where possible

**Non-Goals:**
- Adding a new API endpoint for counts
- Favicon badge or desktop notifications
- Per-route page titles

## Decisions

### 1. Reuse the upcoming store rather than adding a new API endpoint

The `upcomingStore` already contains all tasks with due dates. Deriving a count from it avoids an extra network request and keeps the implementation frontend-only.

**Alternative considered**: A dedicated `/api/upcoming/count/` endpoint would be lighter on data but adds backend surface area for a simple derived value. Not worth it for a single-user app.

### 2. Use a derived Svelte store for the count

A derived store that filters `upcomingStore` for overdue + today tasks and returns the count. This keeps the reactivity chain clean and the count updates automatically when tasks change.

### 3. Set document.title in +layout.svelte via $effect

The layout already manages global concerns. An `$effect` block that watches the count store and sets `document.title` is the simplest approach — no new files needed.

### 4. Load upcoming data on app init

The upcoming store needs to be populated for the count to work on any page, not just the dashboard. The layout will call `loadUpcoming()` on mount and the count will derive from whatever data is loaded.

## Risks / Trade-offs

- **Stale count if upcoming data isn't refreshed**: The count reflects the last `loadUpcoming()` call. If the user leaves the app open overnight, the count won't update until they navigate. This is acceptable for a single-user app — the data refreshes on dashboard visit.
- **Extra API call on non-dashboard pages**: Loading upcoming data globally adds one API call on app start. This is lightweight (small payload, SQLite) and the UX benefit justifies it.
