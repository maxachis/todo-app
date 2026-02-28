## 1. Backend Model & Migration

- [x] 1.1 Add `organizations` ManyToManyField to Interaction model (`network/models/interaction.py`): `organizations = models.ManyToManyField("network.Organization", related_name="interactions", blank=True)`
- [x] 1.2 Generate and apply migration (`python manage.py makemigrations network && python manage.py migrate`)

## 2. Backend API

- [x] 2.1 Update `InteractionSchema` to include `organization_ids: list[int] = []` (`network/api/interactions.py`)
- [x] 2.2 Update `InteractionCreateInput` to include `organization_ids: list[int] = []` (optional, defaults to empty)
- [x] 2.3 Update `InteractionUpdateInput` to include `organization_ids: list[int] | None = None`
- [x] 2.4 Update `_serialize_interaction` to include `organization_ids` from `interaction.organizations.values_list("id", flat=True)`
- [x] 2.5 Update `create_interaction` to set `interaction.organizations.set(...)` when `organization_ids` provided, and prefetch organizations
- [x] 2.6 Update `update_interaction` to set `interaction.organizations.set(...)` when `organization_ids` is not None
- [x] 2.7 Update `list_interactions` and `get_interaction` to prefetch `organizations`

## 3. Backend Tests

- [x] 3.1 Add test: create interaction with `organization_ids` and verify they are returned in response
- [x] 3.2 Add test: create interaction without `organization_ids` and verify empty list in response
- [x] 3.3 Add test: update interaction `organization_ids` and verify replacement
- [x] 3.4 Add test: update interaction without `organization_ids` field and verify organizations unchanged

## 4. Frontend Types

- [x] 4.1 Add `organization_ids: number[]` to `Interaction` interface (`frontend/src/lib/api/types.ts`)
- [x] 4.2 Add `organization_ids?: number[]` to `CreateInteractionInput` interface
- [x] 4.3 Add `organization_ids?: number[]` to `UpdateInteractionInput` interface

## 5. Frontend UI

- [x] 5.1 Load organizations list on mount in interactions page (`frontend/src/routes/interactions/+page.svelte`)
- [x] 5.2 Add organization TypeaheadSelect multi-chip picker to create form (below people selector), bound to `selectedOrganizationIds` state
- [x] 5.3 Include `organization_ids` in create form submission payload
- [x] 5.4 Add organization TypeaheadSelect multi-chip picker to edit/detail panel (below people selector)
- [x] 5.5 Include `organization_ids` in edit form save payload
- [x] 5.6 Display organization names in interaction list items (alongside people names)
- [x] 5.7 Reset organization selection when create form is cleared after submission
