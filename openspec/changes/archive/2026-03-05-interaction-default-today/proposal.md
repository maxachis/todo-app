## Why

When creating an interaction, the date field starts empty, requiring the user to manually pick today's date every time. Since most interactions are logged on the day they happen, defaulting to today reduces friction.

## What Changes

- Default the interaction creation form's date field to today's date
- After form submission and reset, re-default to today's date (not empty)

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `interaction-form-submit`: Change post-submit date reset from empty to today's date

## Impact

- Frontend: `frontend/src/routes/crm/interactions/+page.svelte` — initialize and reset `newDate` to today
- No backend changes (model already defaults `date` to `timezone.now`)

## Non-goals

- Changing the backend default (already defaults to today)
- Changing the edit form behavior
