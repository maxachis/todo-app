## Why

When the people list grows, there's no way to quickly check whether a person has already been added without scrolling through the entire list. A simple name filter lets the user narrow the list inline to verify before creating a duplicate.

## What Changes

- Add a text input to the People list panel's sort bar that filters the displayed people list by first name and last name (client-side, case-insensitive substring match).
- The filter persists while browsing — selecting a person does not clear the filter.
- The filter composes with the existing sort: filter first, then sort the filtered results.

## Non-goals

- Filtering by email, notes, or other fields.
- Server-side search or API changes.
- Debouncing (the list is small enough that instant filtering is fine).
- Persisting the filter value across page navigations.

## Capabilities

### New Capabilities
- `people-name-filter`: Client-side text filter on the People list panel, matching against first and last name.

### Modified Capabilities
- `people-list-sort`: The sort now operates on the filtered subset rather than the full list. No requirement-level change to sort behavior itself.

## Impact

- `frontend/src/routes/people/+page.svelte` — add filter input to the sort bar, wire reactive filtering into the existing `$derived.by()` sort pipeline.
- No backend changes, no new dependencies, no API changes.
