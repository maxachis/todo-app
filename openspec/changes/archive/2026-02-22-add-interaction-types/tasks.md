## 1. Frontend API Client

- [x] 1.1 Add `create` method to `interactionTypes` in `frontend/src/lib/api/index.ts` — POST to `/interaction-types/` with `{ name: string }` payload, returning `InteractionType`

## 2. Interactions Page UI

- [x] 2.1 Add `newTypeName` state variable to `frontend/src/routes/interactions/+page.svelte`
- [x] 2.2 Add `createInteractionType` handler that calls `api.interactionTypes.create()`, appends to `interactionTypes` array (sorted alphabetically), clears input, and auto-selects the new type in `newTypeId` if no type is currently selected
- [x] 2.3 Add inline type creation form (input + "+ Type" button) above the existing interaction creation form, using the `.create-form` CSS class

## 3. Verification

- [x] 3.1 Run `cd frontend && npm run check` to verify no type errors
- [x] 3.2 Manual test: create a new interaction type, confirm it appears in dropdown and can be used to create an interaction
