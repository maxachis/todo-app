## Why

When creating a relationship on the Relationships page, there's no way to see who a person (or organization) is already connected to. Users must scan the full unfiltered list manually to check for existing connections before adding new ones, making it easy to miss duplicates and hard to get context about someone's network.

## What Changes

- Add a filter control (TypeaheadSelect) to each relationship panel that filters the relationship list to show only connections involving the selected person/organization
- When the user selects Person A in the person-person create form (or Organization in the org-person form), the filter auto-populates to show that entity's existing connections
- The filter is also editable independently for browsing without using the create form
- Clearing the form's primary field clears the auto-set filter (back to showing all)
- The Person B dropdown (or Person dropdown in org-person) excludes entities that already have a relationship with the selected primary entity, guiding users toward new connections

## Non-goals

- No changes to the relationship data model or API
- No new API endpoints — filtering is done client-side using already-loaded data
- No changes to the Graph view or other network pages

## Capabilities

### New Capabilities
- `relationship-filter-view`: Filterable relationship list with auto-filter on form selection and exclusion of existing connections from secondary dropdowns

### Modified Capabilities
- `network-frontend`: Adding filter controls and dropdown filtering behavior to the Relationships page

## Impact

- `frontend/src/routes/relationships/+page.svelte` — primary file affected; adds filter state, computed filtering logic, and auto-sync between form and filter
- `TypeaheadSelect` component — no changes needed; existing `options` prop filtering is sufficient
- No backend changes required
