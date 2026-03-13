## Context

The People page (`/crm/people`) includes a "Quick Log Interaction" form in the person detail panel. Currently it captures interaction type, date, and notes. The `Interaction` model already has an optional `medium` foreign key, and the API's `InteractionCreateInput` already accepts `interaction_medium_id`. The full Interactions page already loads mediums and uses a TypeaheadSelect with inline creation — this pattern just needs to be replicated in the quick log form.

## Goals / Non-Goals

**Goals:**
- Add an interaction medium selector to the quick log form on the People page
- Support inline creation of new mediums (matching Interactions page behavior)
- Keep the form compact — medium is optional, placed after type

**Non-Goals:**
- No backend or API changes needed
- No changes to the full Interactions page
- No changes to how mediums display in the interaction history

## Decisions

**Reuse existing TypeaheadSelect pattern**: The Interactions page already loads `interactionMediums` via `api.interactionMediums.getAll()` and uses `TypeaheadSelect` with `onCreate` for inline creation. The People page will follow the same pattern — load mediums on mount, add a TypeaheadSelect between the type selector and the date input.

**Medium is optional**: The TypeaheadSelect will allow clearing (no `required` attribute). The `interaction_medium_id` will be passed as `null` when unset, matching the existing API contract.

## Risks / Trade-offs

- **Form height increases slightly** → Acceptable; the medium selector is compact and the detail panel scrolls.
