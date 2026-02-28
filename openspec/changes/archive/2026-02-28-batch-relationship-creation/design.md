## Context

The Relationships page currently uses a single `bind:value` TypeaheadSelect for Person B (person panel) and Person (org panel), creating one relationship per submission. The Interactions page already implements a multi-person chip pattern using TypeaheadSelect in `onSelect` callback mode with removable chips. The relationship-filter-view feature (just shipped) provides auto-filter and dropdown exclusion that already works per-person and will integrate naturally with batch creation.

## Goals / Non-Goals

**Goals:**
- Allow selecting multiple people as Person B (or People in org panel) before submitting
- Create relationships in parallel on submit with shared notes
- Handle partial failures gracefully — remove successful chips, keep failed ones
- Reuse the existing chip pattern from the Interactions page

**Non-Goals:**
- No batch API endpoint — each relationship is a separate API call
- No changes to the relationship data model
- No "group relationship" concept — relationships remain pairwise

## Decisions

### 1. Switch Person B from bind:value to onSelect chip pattern

**Decision**: Replace the single `bind:value` TypeaheadSelect for Person B with an `onSelect` callback TypeaheadSelect that adds person IDs to an array (`newPersonBIds: number[]`). Selected people render as removable chips above/below the typeahead. Same pattern for org-person panel (`newOrgPersonIds: number[]`).

**Rationale**: This is the exact pattern already used on the Interactions page for multi-person selection. Consistent UX, proven implementation, and the TypeaheadSelect component already supports both modes.

**Alternative considered**: A separate "add row" approach with multiple independent Person B fields. Rejected — more complex UI, more state to manage, and inconsistent with existing multi-select patterns in the app.

### 2. Parallel submission with per-result handling

**Decision**: On submit, fire all API calls with `Promise.allSettled()`. For each result:
- Fulfilled: remove the chip from the array, add the relationship to the local list
- Rejected: keep the chip, show a toast error

After all calls resolve, check if any chips remain. If none: clear Person A, notes, and filter. If some remain: keep Person A, notes, and filter (partial failure state).

**Rationale**: `Promise.allSettled()` (vs `Promise.all()`) ensures all calls complete regardless of individual failures. Per-chip removal gives clear feedback on what succeeded. Preserving form state on partial failure lets the user retry without re-entering data.

### 3. Notes lifecycle tied to chip presence

**Decision**: Notes field clears when all chips are removed — either by successful submission (all succeed) or by manually removing all chips. Notes persist as long as at least one chip exists.

**Rationale**: Notes represent the shared context for this batch ("met at retreat"). As long as the batch is in progress (chips exist), the context should persist. When the batch is complete or abandoned (no chips), the context should clear.

Implementation: an `$effect` that clears notes when `newPersonBIds.length === 0` (and similarly for org panel). This covers both manual removal and post-submission cleanup.

### 4. Submit button shows count

**Decision**: The submit button text dynamically reflects the number of selected people: "+ Add 1 Relationship", "+ Add 3 Relationships". Disabled when no people are selected.

**Rationale**: Makes the batch nature explicit. The user knows exactly how many relationships will be created before pressing the button.

### 5. Dropdown exclusion extends to chip selections

**Decision**: The existing `availablePersonBOptions` derived computation (from relationship-filter-view) already excludes people connected to Person A. It also needs to exclude people currently selected as chips (pending but not yet submitted). This is the same `filter((p) => !newPersonBIds.includes(p.id))` pattern used on the Interactions page.

**Rationale**: Prevents selecting the same person twice in one batch, and keeps the exclusion logic consistent.

## Risks / Trade-offs

- **[Race condition on rapid submit]** → Mitigated by disabling the submit button during submission (set a `submitting` flag). Prevents double-submission of the same batch.
- **[Chip styling consistency]** → Reuse the `.chip`, `.chip-remove` CSS from the Interactions page. Could extract to a shared component later, but for now copying the styles is simpler and avoids scope creep.
- **[Notes clearing on chip removal may surprise users]** → Only clears when ALL chips are removed, not on individual chip removal. This matches the mental model of "I'm done with this batch."
