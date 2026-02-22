## Why

The People page currently displays names in a fixed order (last name, then first name). Users cannot change the sort field or direction, making it harder to find contacts when thinking in terms of first name or follow-up urgency. Adding interactive sort controls gives the user flexibility to view their contact list in the way that's most useful for the task at hand.

## What Changes

- Add a sort control to the People list panel that lets the user select a sort field and toggle sort direction (ascending/descending).
- Supported sort fields: **First Name**, **Last Name**, **Follow Up Days** (`follow_up_cadence_days`).
- Sort is applied client-side on the already-fetched people array.
- Default sort remains Last Name ascending (current behavior).
- The sort icon/button visually indicates the active sort field and direction.
- After creating a new person, the list re-sorts using the active sort setting rather than the hardcoded last-name sort.

## Non-goals

- Server-side / API-level sort parameters — the people list is small enough for client-side sorting.
- Persisting the sort preference across page reloads or sessions.
- Sorting on other fields (e.g., created date, notes).
- Sorting on the Organizations or Interactions pages (separate change if desired).

## Capabilities

### New Capabilities

- `people-list-sort`: Client-side sort controls for the People list — sort field selection (first name, last name, follow-up days) and ascending/descending toggle with visual indicator.

### Modified Capabilities

- `network-frontend`: The People list view gains an interactive sort control that replaces the hardcoded sort-by-last-name behavior.

## Impact

- **Frontend**: `frontend/src/routes/people/+page.svelte` — add sort state, sort UI control, and sort logic replacing the hardcoded `.sort()` call.
- **Backend**: No changes needed — the API already returns all people and the sort will be applied client-side.
- **Tests**: E2E tests for the People page may need updating if they assert on list order.
