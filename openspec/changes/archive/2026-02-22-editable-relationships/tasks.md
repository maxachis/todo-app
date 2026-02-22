## 1. API Client Methods

- [x] 1.1 Add `update(id, payload)` method to `api.relationships.people` in `frontend/src/lib/api/index.ts` — sends PUT to `/relationships/people/{id}/` with `{ notes?: string }` payload, returns `RelationshipPersonPerson`
- [x] 1.2 Add `update(id, payload)` method to `api.relationships.organizations` in `frontend/src/lib/api/index.ts` — sends PUT to `/relationships/organizations/{id}/` with `{ notes?: string }` payload, returns `RelationshipOrganizationPerson`

## 2. Inline Edit UI

- [x] 2.1 In `frontend/src/routes/relationships/+page.svelte`, add `editingId` state to track which relationship is being edited (or `null` for none)
- [x] 2.2 Add an "Edit" button to each relationship list item that sets `editingId` to the relationship's id
- [x] 2.3 When `editingId` matches a relationship, replace the notes display with a `<textarea>` pre-filled with the current notes
- [x] 2.4 On textarea blur, call the appropriate `api.relationships.*.update()` method and update the local array with the response
- [x] 2.5 On Escape keydown in the textarea, cancel editing (revert to display mode, no API call)
- [x] 2.6 Handle the empty-notes case: show "Add notes" placeholder text that activates the edit textarea on click

## 3. Verification

- [x] 3.1 Run `cd frontend && npm run check` and fix any TypeScript errors
