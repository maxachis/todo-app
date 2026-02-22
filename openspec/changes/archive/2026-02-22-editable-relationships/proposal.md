## Why

The Relationships page currently only supports creating and deleting relationships. Users cannot edit the notes on an existing relationship — they must delete and re-create it. The backend already provides PUT endpoints for updating relationship notes, but the frontend has no API client methods or UI to use them.

## What Changes

- Add `update` methods to `api.relationships.people` and `api.relationships.organizations` in the frontend API client
- Make relationship list items on the Relationships page editable: clicking a relationship opens an inline edit mode where the user can modify the notes and save
- Show a visual affordance (e.g., click-to-edit or an edit button) on each relationship item

## Non-goals

- Changing which people/organizations are linked in an existing relationship (delete and re-create instead)
- Adding relationship editing from the People, Organizations, or Interactions detail views
- Backend API changes (PUT endpoints already exist)

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `network-frontend`: Add requirement for editable relationship notes on the Relationships page, and add API client update methods for relationships

## Impact

- `frontend/src/lib/api/index.ts` — add `update` methods to `relationships.people` and `relationships.organizations`
- `frontend/src/routes/relationships/+page.svelte` — add inline edit UI for relationship notes
- No backend changes required (PUT endpoints already exist)
- No migration needed
