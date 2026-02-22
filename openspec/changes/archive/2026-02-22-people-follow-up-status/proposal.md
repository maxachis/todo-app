## Why

The People page shows a flat list of contacts with follow-up cadence values, but gives no indication of who is overdue for contact. With 41 people having cadences set, the user must mentally cross-reference the Interactions page to figure out who needs attention. This makes follow-up triage — the primary CRM workflow — tedious and error-prone.

## What Changes

- The people API (`GET /api/people/`) will return computed `last_interaction_date` and `last_interaction_type` fields per person, derived from the most recent Interaction record.
- The People list will show follow-up status indicators (overdue / due soon / on track) with "days since / cadence" info alongside each person.
- A new "Follow-up status" sort option will be added to the People sort bar, ordering by urgency (most overdue first).
- The People detail panel will display a "Last interaction" summary (date, type) and an overdue warning when applicable.
- The People detail panel will include a "Quick Log Interaction" inline form so the user can log a follow-up without leaving the page.

## Capabilities

### New Capabilities
- `people-follow-up-status`: Follow-up status computation, display, sorting, and quick-log interaction from the People page.

### Modified Capabilities
- `network-api`: The people list/detail endpoints gain computed `last_interaction_date` and `last_interaction_type` response fields.
- `network-frontend`: The People page gains status indicators, a new sort mode, last-interaction display in detail, and a quick-log interaction form.

## Impact

- **Backend**: `network/api/people.py` and `network/api/schemas.py` — annotate people queries with latest interaction data; add computed fields to PersonSchema.
- **Frontend**: `frontend/src/routes/people/+page.svelte` — status indicators in list items, new sort option, detail panel enhancements, quick-log form.
- **Frontend types**: `frontend/src/lib/api/` — update Person type to include new fields.
- **No migrations needed** — the new fields are computed from existing Interaction records, not stored on Person.
