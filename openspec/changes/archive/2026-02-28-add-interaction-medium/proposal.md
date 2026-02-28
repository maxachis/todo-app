## Why

Interactions currently capture "what kind" (Meeting, Catch-up, Introduction) via InteractionType, but not "how" (Email, Phone, In-Person, Video). These are independent dimensions — the same kind of interaction can happen over different media, and users may want to filter or report by either axis. Adding a separate medium field enriches interaction metadata without overloading the type field.

## What Changes

- Add a new `InteractionMedium` model (id, name) following the same pattern as `InteractionType`
- Add an optional `medium` ForeignKey on the `Interaction` model pointing to `InteractionMedium`
- Add CRUD API endpoints for `InteractionMedium` at `/api/interaction-mediums/`
- Extend interaction API schemas to include `interaction_medium_id` (optional/nullable)
- Add frontend API client methods for interaction mediums
- Add a TypeaheadSelect for medium (with inline creation via `onCreate`) to both the create form and detail/edit panel on the Interactions page
- Display medium in the interaction list items when present

## Non-goals

- No migration of existing interaction types that encode medium (e.g., "Email Follow-up") — users can reclassify manually if desired
- No filtering/reporting by medium (future enhancement)
- Medium is not required — existing interactions remain valid with null medium

## Capabilities

### New Capabilities
- `interaction-medium`: CRUD management of interaction mediums and their association with interactions

### Modified Capabilities
- `network-domain-model`: Interaction model gains an optional `medium` FK to InteractionMedium
- `interaction-type-management`: No spec changes needed — interaction types remain unchanged, but the interaction form gains a second TypeaheadSelect alongside the existing type selector

## Impact

- **Backend**: New model + migration, new API router, extended interaction schemas and serializer
- **Frontend**: New TypeScript type + API client methods, updated Interaction type/inputs, updated interactions page (create form + detail panel)
- **Database**: New table `network_interactionmedium`, new nullable FK column on `network_interaction`
