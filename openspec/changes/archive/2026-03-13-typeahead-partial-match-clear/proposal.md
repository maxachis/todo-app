## Why

In bound-value mode TypeaheadSelect fields that have `onCreate` (e.g., interaction types, org types), typing text that exactly matches an existing option and then continuing to type (e.g., "LinkedIn" → "LinkedIn Connection") causes the input to erase. This makes it impossible to create new options whose names start with an existing option's name.

## What Changes

- Fix the `hasExactMatch` derived state in TypeaheadSelect to compare the **untrimmed** input text against option labels, so that "LinkedIn " (with trailing characters) is not treated as an exact match for "LinkedIn".
- This prevents `showCreateOption` from being incorrectly suppressed when the user is still typing beyond an existing match, which in turn prevents the dropdown from closing and the `$effect` from overwriting `displayText`.

## Capabilities

### New Capabilities

_None_

### Modified Capabilities

- `typeahead-selector`: Fix `hasExactMatch` so that partial typing beyond an existing option name does not suppress the "Create" option or close the dropdown prematurely.

## Impact

- **Code**: `frontend/src/lib/components/shared/TypeaheadSelect.svelte` — single-line change in `hasExactMatch` derived state.
- **Behavior**: Affects all TypeaheadSelect instances in bound-value mode with `onCreate` (interaction type fields, org type fields, relationship type fields). No impact on action mode or bound-value mode without `onCreate`.

## Non-goals

- Changing blur behavior (blur-with-trimmed-text auto-select is intentional and correct).
- Modifying the `$effect` that syncs `displayText` with `selectedLabel` when the dropdown closes — the root cause is the dropdown closing prematurely, not the effect itself.
