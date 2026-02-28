## 1. Replace single Person B with multi-person chip state

- [x] 1.1 Replace `newPerson2Id: number | null` with `newPersonBIds: number[]` in `frontend/src/routes/relationships/+page.svelte`
- [x] 1.2 Add `addPersonB(id: number)` function that appends to `newPersonBIds`
- [x] 1.3 Add `removePersonB(id: number)` function that removes from `newPersonBIds`
- [x] 1.4 Replace `newOrgPersonId: number | null` with `newOrgPersonIds: number[]`
- [x] 1.5 Add `addOrgPerson(id: number)` and `removeOrgPerson(id: number)` functions

## 2. Update dropdown exclusion logic

- [x] 2.1 Update `availablePersonBOptions` derived to also exclude IDs in `newPersonBIds` (chip selections)
- [x] 2.2 Update `availableOrgPersonOptions` derived to also exclude IDs in `newOrgPersonIds`

## 3. Update form template to chip pattern

- [x] 3.1 Replace Person B `bind:value` TypeaheadSelect with `onSelect={addPersonB}` TypeaheadSelect and chip rendering loop (reference Interactions page pattern)
- [x] 3.2 Replace org-person Person `bind:value` TypeaheadSelect with `onSelect={addOrgPerson}` and chip rendering
- [x] 3.3 Add `.chips`, `.chip`, `.chip-remove` styles (copy from Interactions page)

## 4. Batch submission logic

- [x] 4.1 Update `createPersonRelationship` to loop over `newPersonBIds`, call API for each with `Promise.allSettled()`, remove successful chips, keep failed chips with toast errors
- [x] 4.2 After all calls resolve: if no chips remain, clear Person A, notes, and chips; if chips remain, keep Person A and notes
- [x] 4.3 Add `submittingPerson` boolean state to disable submit button during batch
- [x] 4.4 Update `createOrgRelationship` with the same `Promise.allSettled()` pattern for `newOrgPersonIds`
- [x] 4.5 Add `submittingOrg` boolean state for org panel submit button

## 5. Dynamic submit button

- [x] 5.1 Update person-person submit button text to show count: `+ Add ${n} Relationship${n !== 1 ? 's' : ''}`. Disable when `newPersonBIds.length === 0` or `submittingPerson`
- [x] 5.2 Update org-person submit button with same pattern using `newOrgPersonIds.length` and `submittingOrg`

## 6. Notes lifecycle

- [x] 6.1 Add `$effect` to clear `newPersonNotes` when `newPersonBIds.length` drops to 0
- [x] 6.2 Add `$effect` to clear `newOrgNotes` when `newOrgPersonIds.length` drops to 0

## 7. Verification

- [x] 7.1 Verify: select Person A, add multiple Person B chips, submit — all relationships created, form clears
- [x] 7.2 Verify: partial failure — successful chips removed, failed chips stay, Person A and notes persist
- [x] 7.3 Verify: removing all chips manually clears notes
- [x] 7.4 Verify: chip selections are excluded from typeahead dropdown
- [x] 7.5 Verify: same behavior works in org-person panel
- [x] 7.6 Run `cd frontend && npm run check` to verify no type errors
