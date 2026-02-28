## 1. Backend API — Trends Endpoint

- [x] 1.1 Create `tasks/api/dashboard.py` with `GET /api/dashboard/trends/` endpoint returning `interactions_per_week`, `tasks_completed_per_week`, and `follow_up_compliance` aggregations
- [x] 1.2 Add response schema to `tasks/api/schemas.py` (or a new `dashboard_schemas.py`) for `TrendsResponse`, `WeeklyCount`, and `FollowUpCompliance`
- [x] 1.3 Register the dashboard router in `tasks/api/__init__.py`

## 2. Backend API — Follow-ups Due Endpoint

- [x] 2.1 Create `GET /api/dashboard/follow-ups-due/` endpoint in `tasks/api/dashboard.py` (or `network/api/dashboard.py`) returning people overdue for follow-up sorted by days overdue descending
- [x] 2.2 Add response schema `FollowUpDueItem` with `person_id`, `first_name`, `last_name`, `follow_up_cadence_days`, `last_interaction_date`, `days_overdue`

## 3. Frontend — Route & Navigation Changes

- [x] 3.1 Rename `frontend/src/routes/upcoming/` directory to `frontend/src/routes/dashboard/`
- [x] 3.2 Update `+layout.svelte` nav tab from `{ href: '/upcoming', label: 'Upcoming' }` to `{ href: '/dashboard', label: 'Dashboard' }`
- [x] 3.3 Add sub-tab bar component to the Dashboard page with "Upcoming" and "Trends" tabs, reading/writing the `tab` query parameter via `$page.url.searchParams`

## 4. Frontend — API Client & Types

- [x] 4.1 Add TypeScript types in `frontend/src/lib/api/types.ts`: `TrendsData`, `WeeklyCount`, `FollowUpCompliance`, `FollowUpDueItem`
- [x] 4.2 Add API methods in `frontend/src/lib/api/index.ts`: `api.dashboard.trends()` and `api.dashboard.followUpsDue()`

## 5. Frontend — Upcoming Sub-tab Enhancements

- [x] 5.1 Fetch follow-ups due data on Upcoming sub-tab mount
- [x] 5.2 Render "Follow-ups Due" group above task groups when overdue follow-ups exist, with person name, days since last interaction, cadence, and days overdue
- [x] 5.3 Make follow-up rows clickable, navigating to `/people?person={person_id}`
- [x] 5.4 Style follow-up rows to be visually distinct from task rows (different icon/color treatment)

## 6. Frontend — Trends Sub-tab

- [x] 6.1 Create Trends sub-tab component that fetches `/api/dashboard/trends/` on mount
- [x] 6.2 Render "Interactions per Week" bar chart using d3 with theme-aware colors
- [x] 6.3 Render "Tasks Completed per Week" bar chart using d3 with theme-aware colors
- [x] 6.4 Render follow-up compliance summary ("X of Y contacts on track") with visual indicator
- [x] 6.5 Wire up theme change listener so charts update colors on dark mode toggle

## 7. Testing

- [x] 7.1 Add backend tests for `GET /api/dashboard/trends/` — verify weekly aggregation logic, zero-fill for empty weeks, compliance score computation
- [x] 7.2 Add backend tests for `GET /api/dashboard/follow-ups-due/` — verify filtering, sorting, edge cases (no interactions, no cadence)
- [x] 7.3 Verify frontend build passes (`npm run check` and `npm run build`)
