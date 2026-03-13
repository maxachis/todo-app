## Why

The quick log interaction form on the People page lets you log type, date, and notes — but not the interaction medium (e.g. "Email", "Phone", "In Person"). The `Interaction` model already supports a `medium` field and the full Interactions page uses it, but the quick log shortcut omits it, forcing users to edit the interaction afterward to add the medium.

## What Changes

- Add a medium TypeaheadSelect to the quick log interaction form on the People page
- Pass `interaction_medium_id` in the quick log API call
- Support inline creation of new mediums (matching the Interactions page behavior)

## Non-goals

- No backend changes needed — the API already accepts `interaction_medium_id` on create
- No changes to the full Interactions page — it already has medium support

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `network-frontend`: Adding medium field to the quick log interaction form on the People page.

## Impact

- **Frontend**: `frontend/src/routes/crm/people/+page.svelte` — add medium state, load interaction mediums, add TypeaheadSelect to quick log form
- **API**: No changes — `InteractionCreateInput` already has `interaction_medium_id` as optional
