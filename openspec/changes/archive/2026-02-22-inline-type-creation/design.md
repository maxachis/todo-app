## Context

Both the Organizations and Interactions pages have a two-step pattern for type management: a standalone "Create Type" form (input + button) at the top of the list panel, separate from the entity creation/edit forms that use `TypeaheadSelect` for type selection. When a needed type doesn't exist, the user must leave their current form context, create the type separately, then return. This change merges type creation into the typeahead itself and removes the standalone forms.

**Current state:**
- `TypeaheadSelect` is a generic reusable component with no creation capability — it only filters and selects from existing options.
- Organizations page has a `createOrgType` form (`newTypeName` input + `+ Type` button) and a separate `createOrganization` form with a TypeaheadSelect for org type.
- Interactions page has a `createInteractionType` form (`newTypeName` input + `+ Type` button) and a separate `createInteraction` form with a TypeaheadSelect for interaction type.
- Backend endpoints `POST /org-types/` and `POST /interaction-types/` already accept `{ name }` and return `{ id, name }`.

## Goals / Non-Goals

**Goals:**
- Add an optional `onCreate` callback to `TypeaheadSelect` that enables inline creation of new entries
- Show a "Create [typed text]" option in the dropdown when the user's input doesn't exactly match any existing option and `onCreate` is provided
- Wire this up for Org Type and Interaction Type typeaheads on both pages (create and edit forms)
- Remove the standalone type creation forms from both pages

**Non-Goals:**
- Inline creation for Person typeaheads (persons require multiple fields)
- Inline creation for task-link typeaheads
- Any backend API changes

## Decisions

### 1. `onCreate` callback signature: `(name: string) => Promise<{ id: number; label: string }>`

The callback receives the trimmed input text and returns a promise resolving to the new option. This keeps TypeaheadSelect agnostic about what API to call — the parent page handles the API call and list update, then returns the new option so the typeahead can select it.

**Alternative considered:** Having TypeaheadSelect accept an API endpoint URL directly. Rejected because it couples the component to API shape and reduces reusability.

### 2. Show "Create [text]" item only when no exact match exists

The create option appears at the bottom of the dropdown when `onCreate` is provided AND the trimmed input text does not exactly match (case-insensitive) any existing option's label. This prevents creating duplicates. If the input is empty, no create option is shown.

**Alternative considered:** Always showing the create option when `onCreate` is provided. Rejected because it would offer to create types that already exist.

### 3. The create option is keyboard-navigable like any other option

The "Create [text]" item participates in the same ArrowDown/ArrowUp/Enter cycle as regular options. It's appended to the filtered list as a virtual entry, so the existing keyboard navigation logic works without special-casing.

### 4. Async creation with inline feedback

When the user selects the create option, `onCreate` is called and awaited. During this time, the input shows the typed text. After the promise resolves, the new option is selected (bound value updated or onSelect fired), same as selecting an existing option.

### 5. Remove standalone type creation forms entirely

The `createOrgType` form and `createInteractionType` form (with their `newTypeName` state variables) are removed from both pages. The `onCreate` handler on each type typeahead replaces this functionality. The handler calls the same API (`api.orgTypes.create` / `api.interactionTypes.create`), updates the local type array, and returns the new option.

## Risks / Trade-offs

- **Discoverability**: Users familiar with the old "Create Type" form need to discover the new inline pattern. Mitigated by the clear "Create [text]" label in the dropdown — it's visible as soon as they type a non-matching name.
- **Error handling**: If the API call fails when creating a type inline, the typeahead needs to handle it gracefully. Mitigation: catch errors in the `onCreate` handler, show a toast or alert, and leave the typeahead input as-is so the user can retry.
- **Race condition**: If the user quickly types and hits Enter before the create resolves, the typeahead should not double-create. Mitigation: disable interaction during the async create call.
