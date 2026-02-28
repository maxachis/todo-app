## Why

Interactions currently only associate with people, but many interactions involve organizations (e.g., a meeting with a company, a call about a deal with a firm). Being able to tag organizations on interactions creates richer context and makes it easier to track engagement with organizations over time.

## What Changes

- Add a many-to-many `organizations` field on the `Interaction` model, mirroring the existing `people` M2M pattern
- Extend the interaction API to accept and return `organization_ids` alongside `person_ids`
- Add organization multi-select UI to both the interaction create form and the edit/detail panel
- Display tagged organization names in the interaction list view

## Capabilities

### New Capabilities

- `interaction-organization-link`: Organizations can be tagged on interactions via a M2M relationship, with full API and UI support for add/remove

### Modified Capabilities

- `network-domain-model`: Interaction model gains an `organizations` M2M field
- `multi-person-interactions`: API and UI patterns extended to also handle organization IDs

## Non-goals

- Organization-to-organization links on interactions (only direct org tagging)
- Making organizations a required field (organizations are fully optional, unlike the current person requirement)
- Filtering/searching interactions by organization (can be added later)

## Impact

- **Backend model**: `network/models/interaction.py` — add `organizations` M2M field + migration
- **API**: `network/api/interactions.py` — extend schemas, serializer, create/update endpoints
- **Frontend types**: `frontend/src/lib/api/types.ts` — add `organization_ids` to Interaction types
- **Frontend UI**: `frontend/src/routes/interactions/+page.svelte` — add organization TypeaheadSelect to create and edit forms, display org names in list
