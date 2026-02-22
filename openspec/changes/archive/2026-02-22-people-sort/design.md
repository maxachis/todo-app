## Context

The People page (`frontend/src/routes/people/+page.svelte`) displays a list of contacts in a two-panel layout. The list is currently hardcoded to sort by `last_name, first_name` — both in the API response and after client-side person creation. There are no sort controls in the UI.

The API (`GET /people/`) returns all people in a single response with no pagination, so the dataset is always fully available client-side.

## Goals / Non-Goals

**Goals:**
- Let users sort the people list by First Name, Last Name, or Follow Up Days
- Let users toggle between ascending and descending order
- Provide a clear visual indicator of the active sort field and direction
- Keep the default sort (Last Name ascending) matching current behavior

**Non-Goals:**
- API-level sort parameters or server-side sorting
- Persisting sort preference across reloads
- Sort controls for Organizations/Interactions pages
- Multi-field sort (e.g., secondary sort key)

## Decisions

### 1. Client-side sorting with reactive state

**Decision**: Sort is applied entirely in the frontend using Svelte 5 reactive state (`$state` for sort field/direction, `$derived` for the sorted list).

**Rationale**: The full people array is already fetched on mount. A derived sorted array avoids duplicating the list and automatically re-sorts when the sort field, direction, or underlying people array changes.

**Alternatives considered**:
- API query params (`?ordering=first_name`) — unnecessary complexity for a small dataset already loaded client-side.

### 2. Sort control placement: above the list, below the create form

**Decision**: Place a compact sort bar between the create form and the people list, containing a `<select>` for field choice and a button to toggle ascending/descending direction.

**Rationale**: This keeps the sort control close to the data it affects without cluttering the create form. A `<select>` is simpler and more accessible than a custom dropdown menu.

### 3. Null handling for follow_up_cadence_days

**Decision**: People with `null` follow-up cadence sort to the end regardless of direction (ascending or descending).

**Rationale**: Null means "no cadence set" — it's neither the smallest nor largest value. Pushing nulls to the end keeps meaningful values together and matches user expectations.

### 4. Replace hardcoded sort in createPerson

**Decision**: After creating a person, re-derive the sorted list using the same active sort state instead of the current hardcoded `localeCompare` on last name.

**Rationale**: The `$derived` sorted array handles this automatically — just append the new person to the `people` array and the derived sort takes effect.

## Risks / Trade-offs

- **[Minimal visual space]** → The sort bar adds a small amount of UI between the form and list. Kept compact with inline layout.
- **[No persistence]** → Users must re-select sort on page reload. Acceptable per proposal non-goals; can be added later with `localStorage` if needed.
