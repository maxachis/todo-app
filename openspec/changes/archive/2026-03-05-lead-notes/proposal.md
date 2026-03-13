## Why

The lead creation form lacks a notes field, even though the backend model, API, and frontend types all support notes. Users can only add notes after creating a lead by selecting it and editing in the detail panel. Adding notes at creation time streamlines data capture.

## What Changes

- Add a notes textarea to the lead creation form in the list panel
- Reset notes field on successful creation (alongside existing field resets)

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `leads`: Add notes textarea to the lead creation form (Scenario: Create new lead from list panel)

## Impact

- Frontend: `frontend/src/routes/crm/leads/+page.svelte` — add textarea and wire `notes` into the create API call
- No backend changes needed (model, API, and schemas already support notes on create)

## Non-goals

- Markdown rendering or rich text editing for notes
- Notes preview in the lead list items
