## Why

Adding a tag to a task currently requires typing/selecting a tag name and then clicking the "+" button (or pressing Enter). This adds unnecessary friction — selecting from the dropdown should immediately add the tag, matching the instant-action pattern used by TypeaheadSelect elsewhere in the app (e.g., LinkedEntities for people/org linking).

## What Changes

- Replace the HTML `<datalist>` + `<input>` + `<form>` tag-add UI in TaskDetail with the existing `TypeaheadSelect` component
- Selecting an existing tag from the dropdown immediately adds it to the task (no submit button needed)
- Typing a new tag name and selecting the "Create …" option immediately creates and adds it
- Remove the "+" submit button since it's no longer needed

## Capabilities

### New Capabilities

_None — this is a UX refinement using existing components and APIs._

### Modified Capabilities

- `typeahead-selector`: Adding a new usage context (tags in task detail) that uses the `onSelect` callback mode with `onCreate` for inline tag creation.

## Impact

- **Frontend**: `TaskDetail.svelte` — replace tag input form with `TypeaheadSelect`
- **No backend changes**: existing `addTag` / `removeTag` / `list tags` API endpoints are sufficient
- **No new dependencies**: reuses the existing `TypeaheadSelect` component

## Non-goals

- Changing tag styling or display
- Multi-select / bulk tag operations
- Tag management (rename, delete, merge) UI
