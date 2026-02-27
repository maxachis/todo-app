## Why

When using a TypeaheadSelect without an `onCreate` callback (e.g., selecting an organization for a person in the leads or linked-entities flow), typing a name that doesn't match any existing option silently hides the dropdown and discards the typed text on blur. The user gets no feedback — their input just vanishes. This is confusing and makes it unclear whether the item doesn't exist or the component malfunctioned. The dropdown should instead show a "not found" message telling the user the item must be added first.

## What Changes

- When a TypeaheadSelect has no `onCreate` callback and the typed text matches no options, the dropdown stays open and displays a non-selectable message (e.g., "No match found — add it first") instead of silently closing.
- The typed text is preserved in the input while the "not found" message is visible, so the user doesn't lose what they typed.
- TypeaheadSelects that have an `onCreate` callback are unaffected — they continue to show the "Create [text]" option as before.

## Non-goals

- Adding inline creation (`onCreate`) to TypeaheadSelects that don't currently have it — this change only improves feedback, not capability.
- Changing the behavior when options *do* match the typed text.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `typeahead-selector`: The "no matches found without onCreate" behavior changes from hiding the dropdown to showing a non-selectable "not found" message. Modifies the scenario at spec lines 16-18 (FR: "No matches found without onCreate").

## Impact

- **Frontend**: `TypeaheadSelect.svelte` — filtering/dropdown-open logic and template to render the "not found" item.
- **No backend changes** — purely a UI feedback improvement.
- **All consumers** of TypeaheadSelect without `onCreate` gain this behavior automatically (LinkedEntities for people/orgs, people page quick-log interaction type selector, etc.).
