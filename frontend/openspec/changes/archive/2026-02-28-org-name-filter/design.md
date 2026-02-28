## Context

The Organizations page has a two-column layout: left panel with a create form and an alphabetically-sorted list, right panel with detail editing. Unlike the People page, there is no sort bar — organizations are sorted on creation via `localeCompare`. The list iterates directly over the `organizations` array.

## Goals / Non-Goals

**Goals:**
- Add a text input between the create form and the list that filters organizations by name.
- Filter persists through organization selection.

**Non-Goals:**
- Adding sort controls.
- Filtering by org type or notes.
- Server-side search or API changes.

## Decisions

**1. Filter input between create form and list**
Add a `filterQuery` `$state('')` and a text `<input>` between the `.create-form` and `.list` divs. This mirrors the placement used on the People page (filter sits above the list).

**2. Derived filtered list**
Add a `filteredOrganizations` `$derived` that filters `organizations` by case-insensitive substring match on `name`, then use that in the `{#each}` block. No separate sort step needed since the array is already maintained in sorted order.

**3. Consistent styling with People page**
Use the same `.filter-input` styling: matching border, radius, padding, and font to existing form inputs.

## Risks / Trade-offs

- [Consistency] People page has a sort bar housing the filter; Organizations doesn't. The filter stands alone above the list — acceptable since there's nothing else to group with.
