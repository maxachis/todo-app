## Context

The relationships page (`frontend/src/routes/relationships/+page.svelte`) has two create forms — one for person-person relationships and one for org-person relationships. Each form has two TypeaheadSelect fields and a notes textarea. Currently, submission requires clicking the "+ Relationship" button. The interaction screen already implements enter-to-submit on its create form via a keydown handler on the notes textarea.

## Goals / Non-Goals

**Goals:**
- Pressing Enter in either relationship form's notes textarea submits the form (when required fields are filled)
- Shift+Enter inserts a newline in the notes textarea
- Consistent behavior with the interaction create form

**Non-Goals:**
- Changing TypeaheadSelect Enter behavior (dropdown selection stays as-is)
- Backend/API changes
- Modifying edit behavior on existing relationships

## Decisions

### Keydown handler on notes textarea (same pattern as interactions)

Add an `onkeydown` handler directly on each notes `<textarea>` that intercepts Enter (without Shift) and programmatically submits the parent form.

**Why this over form-level keydown:** The TypeaheadSelect components already capture Enter for dropdown selection. A textarea-level handler avoids conflicting with that behavior and matches the established interaction-form-submit pattern exactly.

**Why not a shared action/component:** Only two textareas need this. A Svelte action or shared component would be over-engineering for a two-line handler that's already proven in the interactions page.

## Risks / Trade-offs

- [Users wanting multi-line notes] → Shift+Enter provides newline insertion, matching standard UX conventions (Slack, Discord, etc.)
- [Accidental submission with empty selects] → Handler checks that required IDs are populated before calling submit; if not, Enter is a no-op
