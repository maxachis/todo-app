## Why

Creating multiple relationships for the same person or organization requires re-selecting the primary entity each time. When logging connections from an event or onboarding new team members, this is tedious — the user wants to set Person A (or Organization) once and add several related people in quick succession.

## What Changes

- Replace the single Person B field with a multi-person chip selector (TypeaheadSelect in `onSelect` mode) in the person-person create form, allowing multiple people to be queued before submission
- Replace the single Person field with a multi-person chip selector in the org-person create form
- On submit, create one relationship per selected person, all sharing the same notes text
- Handle partial failures gracefully: remove chips for successful creates, keep chips for failures with a toast error, preserve Person A and notes as long as any chip remains
- Update the submit button to reflect the count (e.g., "+ Add 3 Relationships")
- Notes clear only when all chips are cleared (manually or after successful submission)

## Non-goals

- No changes to the relationship data model or API — each relationship is still created as a separate API call
- No "group relationship" concept — relationships remain pairwise, just created in batch
- No changes to the filter or dropdown exclusion logic (already works correctly per-person)

## Capabilities

### New Capabilities
- `batch-relationship-creation`: Multi-person selection and batch submission in relationship create forms

### Modified Capabilities
- `relationship-filter-view`: Submitting the form no longer always clears Person A / Organization — it only clears when all relationships succeed (no remaining chips). The filter auto-sync and exclusion logic behavior adjusts accordingly.

## Impact

- `frontend/src/routes/relationships/+page.svelte` — primary file; replaces single Person B / Person bind:value TypeaheadSelect with onSelect chip pattern, updates submit logic to loop and handle partial failure
- Existing multi-person chip pattern from Interactions page (`frontend/src/routes/interactions/+page.svelte`) can be referenced for implementation approach
- No backend changes required
