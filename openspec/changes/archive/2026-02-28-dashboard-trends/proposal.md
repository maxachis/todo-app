## Why

The app tracks interactions, relationships, tasks, and follow-up cadences, but there's no single view that answers "am I staying engaged with my network?" or "what's slipping through the cracks?" The Upcoming page only shows tasks with due dates. Adding a Dashboard with trends and follow-up intelligence gives both habit visibility (am I consistently investing?) and actionable alerts (who's overdue?).

## What Changes

- Rename the "Upcoming" nav tab and route to "Dashboard" (URL stays at `/upcoming` or moves to `/dashboard`)
- Add sub-tab navigation within the Dashboard page: **Upcoming** (existing task triage) and **Trends** (analytics charts)
- Integrate follow-up intelligence into the Upcoming sub-tab: a "Follow-ups Due" group alongside Overdue/Today/Tomorrow/This Week/Later, showing people past their `follow_up_cadence_days` threshold
- Add three charts to the Trends sub-tab:
  1. **Interactions per week** — bar chart, last 12 weeks
  2. **Tasks completed per week** — bar chart, last 12 weeks
  3. **Follow-up compliance** — summary stat ("X of Y contacts on track") with current score
- Add backend API endpoints for aggregated trend data and follow-up due list

## Non-goals

- Historical trend storage or snapshots — all metrics are computed live from existing data
- Customizable date ranges or chart types — fixed 12-week window to start
- Notifications or email reminders for overdue follow-ups
- Modifying the existing Graph (network visualization) page

## Capabilities

### New Capabilities
- `dashboard-trends`: Analytics charts (interactions/week, tasks completed/week, follow-up compliance) with backend aggregation endpoints and frontend chart rendering
- `dashboard-follow-ups`: Follow-up due list integrated into the Upcoming sub-tab, showing people past their interaction cadence, with backend endpoint

### Modified Capabilities
- `upcoming-dashboard`: Route/nav rename from "Upcoming" to "Dashboard", addition of sub-tab navigation, page structure change to accommodate multiple views

## Impact

- **Frontend**: `frontend/src/routes/upcoming/+page.svelte` restructured with sub-tab UI; new chart components using d3 (already a dependency); new store for trends data; layout nav tab renamed
- **Backend**: New API endpoints in `network/api/` for follow-up due list and trend aggregations; new endpoint in `tasks/api/` for task completion stats
- **API types**: New TypeScript types for trend data and follow-up due responses
- **Navigation**: Tab label changes from "Upcoming" to "Dashboard" in `+layout.svelte`
- **Dependencies**: No new dependencies (d3 already available)
