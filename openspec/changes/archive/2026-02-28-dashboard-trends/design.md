## Context

The Upcoming page (`/upcoming`) currently shows tasks with due dates grouped by time horizon. The app already has all the raw data needed for trend analytics — `Interaction.date`, `Task.completed_at`, `Person.follow_up_cadence_days` — but no aggregation layer or visualization for it.

The existing Graph page uses d3 for network visualization, so d3 is already a project dependency. The frontend is a SvelteKit SPA with a typed API client and per-resource Svelte stores.

## Goals / Non-Goals

**Goals:**
- Rename Upcoming to Dashboard with sub-tab navigation (Upcoming | Trends)
- Surface follow-up overdue people alongside task groups in the Upcoming sub-tab
- Provide three trend charts: interactions/week, tasks completed/week, follow-up compliance
- Keep all metrics computed live from existing data — no new models or stored aggregations

**Non-Goals:**
- Custom date range selection or configurable chart types
- Push notifications or email reminders for overdue follow-ups
- Historical snapshots or pre-computed metrics tables
- Changes to the Graph (network visualization) page

## Decisions

### 1. Sub-tab state management: local variable vs URL param

**Decision**: Use a query parameter (`?tab=upcoming` / `?tab=trends`) so tabs are linkable and browser back/forward works.

**Alternatives considered**:
- Local `$state` variable — simpler but loses tab state on refresh or link sharing
- Separate routes (`/dashboard/upcoming`, `/dashboard/trends`) — overkill for two tabs within one page, adds routing complexity

**Rationale**: Query param is minimal effort (read from `$page.url.searchParams`), preserves browser behavior, and doesn't require SvelteKit route restructuring.

### 2. Route path: keep `/upcoming` vs move to `/dashboard`

**Decision**: Move to `/dashboard`. The page's purpose is expanding beyond upcoming tasks, and the URL should reflect that.

**Rationale**: Keeping `/upcoming` while the tab says "Dashboard" creates a mismatch. Since this is a single-user app with no external links to worry about, no redirect is needed.

### 3. Chart library: d3 (existing) vs lightweight alternative

**Decision**: Use d3 for chart rendering, since it's already in the bundle for the Graph page.

**Alternatives considered**:
- Chart.js — simpler API for standard charts but adds a new dependency (~60KB gzipped)
- Lightweight SVG helpers — less abstraction but more manual work

**Rationale**: d3 is already loaded. Simple bar charts with d3 are straightforward. Keeps the dependency tree flat.

### 4. Backend aggregation approach: single endpoint vs per-chart endpoints

**Decision**: One endpoint `GET /api/dashboard/trends/` that returns all three metrics in a single response.

**Alternatives considered**:
- Separate endpoints per chart (`/api/stats/interactions-weekly/`, etc.) — more RESTful but means 3 round trips on tab load
- GraphQL-style query — over-engineered for 3 fixed metrics

**Rationale**: The Trends tab always shows all three charts. One request is simpler and faster. The payload is small (12 weeks × 2 series + 1 compliance stat).

### 5. Follow-ups due endpoint: new endpoint vs extend existing people API

**Decision**: New endpoint `GET /api/dashboard/follow-ups-due/` that returns people overdue for follow-up, sorted by days overdue descending.

**Rationale**: The People API already has follow-up status data, but it returns all people with full detail. The dashboard needs a focused, pre-filtered, pre-sorted list. A dedicated endpoint avoids over-fetching and keeps the query optimized.

### 6. Follow-ups placement in Upcoming sub-tab

**Decision**: Render "Follow-ups Due" as a card/group above the task time-horizon groups, visually distinct (different styling to differentiate CRM items from tasks).

**Rationale**: Follow-ups are a different entity type than tasks. Placing them above (rather than interleaved with) the task groups keeps the mental model clean — "people to contact" then "tasks to do." The visual distinction prevents confusion about what's a task vs a follow-up.

## Risks / Trade-offs

- **[Performance] Live aggregation on every page load** → For a single-user app with modest data volumes, the queries are cheap (indexed `date` and `completed_at` fields). If data grows significantly, could add server-side caching or materialized views later.

- **[UX] Dashboard page doing two things (triage + trends)** → Mitigated by sub-tabs keeping each view focused. The tab state persists via URL param, so users land on whichever tab they last used if bookmarked.

- **[Complexity] d3 for simple bar charts** → d3's API is verbose for basic charts compared to Chart.js. Mitigated by keeping chart components self-contained. Could extract a simple bar chart helper if the pattern repeats.

## Open Questions

- Should the Trends tab auto-refresh or only load on tab switch? (Leaning toward load-on-switch for simplicity.)
- Should follow-up rows in the Upcoming tab link somewhere? (Likely to the People page filtered to that person.)
