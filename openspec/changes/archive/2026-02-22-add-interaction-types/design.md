## Context

The Interactions page (`frontend/src/routes/interactions/+page.svelte`) allows creating interactions with an existing interaction type selected from a dropdown, but provides no way to create new interaction types. The Organizations page already has this pattern: an inline form with a text input and "+ Type" button that calls `api.orgTypes.create()`.

The backend already exposes full CRUD at `/api/interaction-types/` (GET, POST, PUT, DELETE). The frontend API client only has `getAll()` — no `create` method.

## Goals / Non-Goals

**Goals:**
- Add a `create` method to the frontend `interactionTypes` API client, mirroring `orgTypes.create`
- Add an inline type creation form on the Interactions page, matching the org type creation UX
- Newly created types appear immediately in the interaction type dropdown

**Non-Goals:**
- Update/delete interaction types from the UI
- Backend API changes (endpoints already exist)
- Model or migration changes

## Decisions

**1. Mirror the orgTypes.create pattern exactly**

The `orgTypes` client uses `apiRequest<OrgType>('/org-types/', { method: 'POST', body: JSON.stringify(payload) })`. The interaction types endpoint follows the same convention (`/interaction-types/`), so the implementation is a direct copy with the appropriate type and URL.

Alternative: A generic "type management" abstraction — rejected as over-engineering for two simple one-liner methods.

**2. Place the type creation form above the interaction creation form**

This matches the Organizations page layout where the type form (`createOrgType`) sits above the entity form (`createOrganization`). The form is a single-line input + button using the existing `.create-form` CSS class.

Alternative: A modal or separate page — rejected as inconsistent with the established pattern.

**3. Auto-select newly created type in the interaction form**

After creating a new type, if no type is currently selected in the "new interaction" form, auto-select the just-created type. This mirrors `createOrgType` which sets `newOrgTypeId = created.id` when no type is selected.

## Risks / Trade-offs

- [Minimal scope] Only creation is added, not update/delete. Users who need to rename or remove a type must use the admin. → Acceptable for now; update/delete can be added in a follow-up.
- [No validation beyond empty check] The form only checks for non-empty input, matching the org type pattern. Duplicate names are allowed by the backend. → Consistent with existing behavior.
