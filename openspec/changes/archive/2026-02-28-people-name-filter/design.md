## Context

The People page displays all people in a scrollable left panel with sort controls. As the list grows, there's no quick way to check if a person already exists. The sort bar currently contains a field selector (`<select>`) and a direction toggle button, sitting between the create form and the list.

The people list is local `$state` loaded on mount, with a `$derived.by()` block that sorts. There is no store — all state is page-local.

## Goals / Non-Goals

**Goals:**
- Add a text input to the existing sort bar that filters the people list by name.
- Filter composes with sort: filter first, then sort the result.
- Filter persists through person selection.

**Non-Goals:**
- Server-side search or API changes.
- Filtering by fields other than first/last name.
- Persisting the filter across page navigations.
- Debouncing (list is small, instant filtering is fine).

## Decisions

**1. Inline text input in the sort bar**
Place a text `<input>` in the `.sort-bar` div alongside the existing sort field selector and direction toggle. This keeps filtering and sorting co-located and avoids adding a separate UI row.

Alternative considered: Separate filter row above the sort bar — rejected because the sort bar already has horizontal space and adding a row compresses the list area.

**2. Extend the existing `$derived.by()` pipeline**
Add a `filterQuery` `$state('')` variable. The existing `sortedPeople` derived block becomes `filteredAndSortedPeople`: filter the `people` array by substring match on `first_name` and `last_name`, then sort the result.

Alternative considered: Separate `$derived` for filtering and sorting — unnecessary indirection for a single pipeline.

**3. Case-insensitive substring match**
Use `.toLowerCase().includes()` on both first and last name. This matches the pattern used by TypeaheadSelect elsewhere in the app.

## Risks / Trade-offs

- [Large lists] Client-side filtering on every keystroke could lag with thousands of entries → Acceptable for a personal CRM; if needed later, add debounce.
- [Sort bar crowding on mobile] Adding an input to the sort bar may not fit on narrow screens → The page already collapses to single-column below 1024px; the input can take full width in the collapsed layout.
