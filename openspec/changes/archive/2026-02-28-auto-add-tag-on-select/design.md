## Context

The task detail panel in `TaskDetail.svelte` currently uses a plain `<input>` with an HTML `<datalist>` for tag suggestions, wrapped in a `<form>` with a "+" submit button. Adding a tag requires typing a name and then explicitly submitting (Enter or click "+").

Meanwhile, the app already has a `TypeaheadSelect` component used extensively for entity linking (people, organizations, interaction types, org types) in both bound-value mode (form fields) and action mode (fire-and-forget). The `LinkedEntities` component demonstrates the exact pattern needed: action-mode TypeaheadSelect with `onSelect` callback for immediate add-on-select.

## Goals / Non-Goals

**Goals:**
- Replace the datalist + form tag input with TypeaheadSelect in action mode
- Tags are added immediately on selection from the dropdown (no submit step)
- New tags can be created inline via the `onCreate` callback
- Consistent UX with other typeahead-driven selections in the app

**Non-Goals:**
- Changing backend tag API endpoints
- Modifying the TypeaheadSelect component itself
- Changing how tags are displayed or removed
- Tag management features (rename, delete, merge)

## Decisions

### Use TypeaheadSelect in action mode with onCreate

**Choice**: Use `TypeaheadSelect` with `onSelect` callback (action mode) and `onCreate` callback, matching the pattern in `LinkedEntities`.

**Rationale**: Action mode clears the input after selection, which is the desired behavior for adding tags — the user selects a tag, it's added, the input resets for the next tag. The `onCreate` callback enables creating new tags inline without a separate flow.

**Alternative considered**: Keeping the `<input>` + `<datalist>` and adding an `onchange` event listener. Rejected because the native datalist has inconsistent behavior across browsers and doesn't support the "Create …" option pattern.

### Map available tags to TypeaheadSelect options format

**Choice**: Transform the `availableTags` array (`Tag[]` with `{id, name}`) to TypeaheadSelect's `{id, label}` format inline.

**Rationale**: Simple mapping (`{ id: tag.id, label: tag.name }`), no adapter layer needed.

### Keep existing tag display and remove UI unchanged

**Choice**: Only replace the input/form portion; the existing tag chips with "✕" buttons remain as-is.

**Rationale**: The tag display works well and isn't part of the problem. Minimizing scope reduces risk.

## Risks / Trade-offs

- **[Minor UX shift]** → Users accustomed to typing + Enter will still work (TypeaheadSelect supports Enter to select the highlighted option). The "+" button goes away, but the workflow is strictly faster.
- **[Available tags refresh]** → After adding a tag via `onSelect`, the available tags list needs to be refreshed so the just-added tag no longer appears in suggestions. The existing `loadAvailableTags` call after `refreshTask` handles this. → Ensure `onSelect` triggers both the API call and the tag list refresh.
