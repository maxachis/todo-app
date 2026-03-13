## 1. Load Interaction Mediums

- [x] 1.1 Import `InteractionMedium` type and add `interactionMediums` state array in `frontend/src/routes/crm/people/+page.svelte`
- [x] 1.2 Fetch interaction mediums via `api.interactionMediums.getAll()` on mount (alongside existing `interactionTypes` fetch)

## 2. Quick Log Form State

- [x] 2.1 Add `quickLogMediumId` state variable (`number | null`, default `null`) in `frontend/src/routes/crm/people/+page.svelte`
- [x] 2.2 Reset `quickLogMediumId` to `null` when selecting a new person and after successful form submission

## 3. Quick Log Form UI

- [x] 3.1 Add TypeaheadSelect for medium between the type selector and date input in the quick log form, with `onCreate` callback for inline creation
- [x] 3.2 Add `handleCreateInteractionMedium` function (create via API, update local list, return `{id, label}`)

## 4. API Integration

- [x] 4.1 Pass `interaction_medium_id: quickLogMediumId` in the `api.interactions.create()` call within `quickLogInteraction()`

## 5. Verification

- [x] 5.1 Run `npm run check` in `frontend/` to verify no type errors
