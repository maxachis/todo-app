## Why

Adding relationships requires clicking the "+ Relationship" button, breaking keyboard flow. The interaction screen already supports Enter-to-submit on its create form — the relationship screen should behave consistently.

## What Changes

- Both relationship create forms (person-person and org-person) submit when the user presses Enter in the notes textarea
- Shift+Enter inserts a newline in the notes field (preserves multi-line input)
- Enter-to-submit only applies to the create forms, not to inline editing of existing relationships

## Non-goals

- No changes to TypeaheadSelect behavior (Enter within an open dropdown still selects the option)
- No changes to the API or backend
- No changes to the edit/detail flow for existing relationships

## Capabilities

### New Capabilities
- `relationship-form-submit`: Enter key submits the relationship create forms (both person-person and org-person) from the notes textarea, consistent with interaction-form-submit behavior

### Modified Capabilities

## Impact

- `frontend/src/routes/relationships/+page.svelte` — add keydown handler on notes textareas for both forms
