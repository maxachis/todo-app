## Why

Same problem as the People page: as the organizations list grows, there's no way to quickly check whether an organization already exists without scrolling through the full list. A name filter lets the user narrow the list to verify before creating a duplicate.

## What Changes

- Add a text input above the organizations list that filters by organization name (client-side, case-insensitive substring match).
- The filter persists while browsing — selecting an organization does not clear the filter.
- Clearing the filter restores the full list.

## Non-goals

- Filtering by org type, notes, or other fields.
- Server-side search or API changes.
- Adding sort controls (the list is already alphabetically sorted on creation).

## Capabilities

### New Capabilities
- `org-name-filter`: Client-side text filter on the Organizations list panel, matching against organization name.

### Modified Capabilities

(none)

## Impact

- `frontend/src/routes/organizations/+page.svelte` — add filter input and reactive filtering of the `organizations` array before rendering.
- No backend changes, no new dependencies, no API changes.
