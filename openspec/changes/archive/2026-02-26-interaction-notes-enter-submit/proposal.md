## Why

When adding interactions, the notes textarea does not respond to the Enter key for submission. Users expect pressing Enter in a single-line-style form to submit it, but the textarea swallows Enter as a newline. This creates friction when rapidly logging multiple interactions — the user must reach for the mouse to click the "+ Interaction" button.

## What Changes

- Add keyboard handling to the interaction create form's notes textarea so that pressing **Enter** (without modifier keys) submits the form
- **Shift+Enter** will continue to insert a newline, preserving multi-line note entry
- This matches the enter-to-submit pattern already used elsewhere in the app (e.g., project name editing)

## Non-goals

- No changes to the interaction edit/detail form (right panel) — that form auto-saves on blur
- No changes to the "Quick Log Interaction" form on the People detail page (can be addressed separately)
- No markdown support for the notes field — it remains a plain textarea

## Capabilities

### New Capabilities

- `interaction-form-submit`: Keyboard submission behavior for the interaction create form, specifically Enter-to-submit on the notes textarea with Shift+Enter for newlines

### Modified Capabilities

_None_ — no existing spec-level requirements are changing. The interaction form's core data flow and validation remain the same.

## Impact

- **Frontend only**: `frontend/src/routes/interactions/+page.svelte` — keydown handler on the notes textarea
- No API changes, no backend changes, no new dependencies
