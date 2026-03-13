## Context

Timesheet entries have create (POST) and delete (DELETE) endpoints but no update (PUT). The description field is displayed as static text in entry rows. Users need to delete and re-create entries to fix descriptions.

## Goals / Non-Goals

**Goals:**
- Add a PUT endpoint to update description on existing time entries
- Make description editable inline in the timesheet entry rows

**Non-Goals:**
- Editing project, date, or linked tasks after creation
- Rich text or markdown in descriptions

## Decisions

- **PUT endpoint at `/timesheet/{entry_id}/`**: Accepts `UpdateTimeEntryInput` with optional `description` field. Returns the updated `TimeEntrySchema`. Matches the existing pattern used by other resources.
- **Inline edit via input field**: Clicking the description text (or an empty description area) turns it into an input field. On blur, the update is saved via API. This matches the auto-save-on-blur pattern used in task detail and lead editing.
- **Optimistic UI**: Update the local store entry immediately, roll back on API failure (matching the pattern in other stores).

## Risks / Trade-offs

- Inline editing in a compact row can be fiddly on mobile. Acceptable since timesheet is primarily a desktop feature and the input only activates on click.
