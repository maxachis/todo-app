## Context

The lead creation form currently accepts only title, person, and organization. The backend model, API schemas, and frontend types already support a `notes` field on create. The edit detail panel already has a notes textarea. The gap is purely in the creation form UI.

## Goals / Non-Goals

**Goals:**
- Add a notes textarea to the lead creation form so users can capture notes at creation time

**Non-Goals:**
- Rich text / markdown rendering for notes
- Showing notes preview in the lead list

## Decisions

- **Add textarea after the org typeahead in the create form**: Mirrors the field order in the edit form (title, person, org, notes). Use a simple `<textarea>` with placeholder text, matching the edit form's approach.
- **No backend changes**: The model and API already handle notes on create with `blank=True` default.
- **Reset on submit**: Clear the notes field alongside title, person, and org after successful creation.

## Risks / Trade-offs

- The create form becomes slightly taller with the textarea. Acceptable since it provides clear value and the textarea can be compact (2-3 rows).
