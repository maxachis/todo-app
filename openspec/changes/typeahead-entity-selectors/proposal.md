## Why

Native `<select>` dropdowns for people and organizations don't scale well as the number of entities grows. Users must scroll through an unsorted or alphabetical list to find the entity they want. Replacing these with typeahead (autocomplete) inputs lets users filter by typing, navigate results with keyboard (arrow keys + Enter), and select faster — especially when there are many entries.

## What Changes

- Introduce a reusable **Typeahead** component that replaces native `<select>` elements for entity selection
- The typeahead filters a list of options as the user types, shows a dropdown of matching results, and supports keyboard navigation (Up/Down arrows, Enter to select, Escape to dismiss)
- Replace the `<select>` in **LinkedEntities.svelte** (used in Task Detail for linking people and organizations) with the new typeahead
- Replace the person `<select>` and interaction-type `<select>` in **Interactions page** create/edit forms with typeahead inputs
- Replace the org-type `<select>` in **Organizations page** create/edit forms with a typeahead input
- Already-linked entities continue to be excluded from available options (existing behavior preserved)

## Non-goals

- Server-side search / paginated API results — the app loads all entities upfront and filtering is client-side
- Changing the priority dropdown in Task Detail (it has only 4 fixed options)
- Changing the tag input (already uses `<datalist>` autocomplete)
- Changing the project dropdown selector
- Adding create-on-the-fly ("add new person from typeahead") — entity creation stays in dedicated forms

## Capabilities

### New Capabilities

- `typeahead-selector`: Reusable typeahead/autocomplete component with keyboard navigation, filtering, and dropdown result display. Defines the component API, accessibility, and interaction behavior.

### Modified Capabilities

- `task-link-ui`: Entity selection in the task detail panel changes from `<select>` dropdown to typeahead input (affects add-person and add-organization link scenarios)
- `network-frontend`: Entity selection in Interactions (person, interaction type) and Organizations (org type) forms changes from `<select>` dropdown to typeahead input

## Impact

- **Frontend components**:
  - New: `frontend/src/lib/components/shared/TypeaheadSelect.svelte` (or similar)
  - Modified: `frontend/src/lib/components/shared/LinkedEntities.svelte` — swap `<select>` for typeahead
  - Modified: `frontend/src/routes/interactions/+page.svelte` — swap person and interaction-type `<select>` elements
  - Modified: `frontend/src/routes/organizations/+page.svelte` — swap org-type `<select>` element
- **API**: No backend changes — existing `getAll()` endpoints already return full entity lists used for filtering
- **Tests**: E2E tests that interact with entity dropdowns will need selector updates
