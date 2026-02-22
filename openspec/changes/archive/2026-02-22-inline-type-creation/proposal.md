## Why

When creating or editing Organizations and Interactions, users must switch context to the separate "Create Type" form at the top of the page if the type they want doesn't exist yet. This breaks the flow — the user is mid-form, realizes the type is missing, scrolls up to create it, then returns to continue. The typeahead should let users create a new type inline when no match is found, keeping them in flow.

## What Changes

- Enhance the `TypeaheadSelect` component to accept an optional `onCreate` callback. When provided and the user's typed text doesn't match any existing option, a "Create [typed text]" item appears at the bottom of the dropdown.
- Selecting the "Create..." item calls `onCreate` with the typed text, which creates the type via API and returns the new option (id + label) so the typeahead can select it.
- Wire up `onCreate` on the Organizations page for the Org Type typeahead (both create and edit forms).
- Wire up `onCreate` on the Interactions page for the Interaction Type typeahead (both create and edit forms).
- Remove the standalone "Create Type" input+button forms from both the Organizations and Interactions pages, since inline creation via the typeahead replaces them.

## Non-goals

- Inline creation for Person typeaheads on the Interactions page (persons have more fields than just a name).
- Adding inline creation to task-link typeaheads or any other typeahead usage.

## Capabilities

### New Capabilities

_(none — this extends existing capabilities)_

### Modified Capabilities

- `typeahead-selector`: Add optional `onCreate` prop and "Create [text]" dropdown item when no exact match exists and `onCreate` is provided.
- `network-frontend`: Wire `onCreate` on Org Type and Interaction Type typeaheads to create types inline via API. Remove standalone type creation forms.

## Impact

- **Frontend component**: `TypeaheadSelect.svelte` gains new optional prop and conditional UI for the create option.
- **Frontend pages**: `organizations/+page.svelte` and `interactions/+page.svelte` pass `onCreate` handlers to type typeaheads.
- **Backend**: No API changes needed — `POST /org-types/` and `POST /interaction-types/` already exist.
