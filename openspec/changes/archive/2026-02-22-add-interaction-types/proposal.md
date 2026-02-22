## Why

The Interactions page allows selecting an interaction type from a dropdown, but there is no way to create new interaction types from the UI. Users must rely on the admin or direct API calls. The Organizations page already lets users create new org types inline — interaction types should work the same way.

## What Changes

- Add a `create` method to the `interactionTypes` API client (mirroring `orgTypes.create`)
- Add an inline form on the Interactions page for creating new interaction types (text input + button, matching the org type creation pattern on the Organizations page)
- Newly created interaction types immediately appear in the type dropdown

## Non-goals

- Update/delete interaction types from the UI (can be added later)
- Changing the backend API (CRUD endpoints already exist at `/api/interaction-types/`)
- Modifying the InteractionType model

## Capabilities

### New Capabilities

- `interaction-type-management`: Frontend UI and API client support for creating interaction types inline on the Interactions page

### Modified Capabilities

- `network-frontend`: The Interactions page gains an interaction type creation form, following the same pattern as org type creation on the Organizations page

## Impact

- **Frontend API client** (`frontend/src/lib/api/index.ts`): Add `create` method to `interactionTypes`
- **Interactions page** (`frontend/src/routes/interactions/+page.svelte`): Add type creation form and handler
- **No backend changes** — existing endpoints already support this
- **No model changes** — `InteractionType` model is already in place
