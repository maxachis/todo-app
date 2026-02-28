## 1. Backend Model & Migration

- [x] 1.1 Create `InteractionMedium` model in `network/models/` (id, name CharField max 255) with `__str__` returning name
- [x] 1.2 Add optional `medium` ForeignKey on `Interaction` model (null=True, blank=True, on_delete=SET_NULL, to InteractionMedium)
- [x] 1.3 Register InteractionMedium in `network/models/__init__.py` exports
- [x] 1.4 Run `makemigrations` and `migrate`

## 2. Backend API

- [x] 2.1 Add `InteractionMediumSchema`, `InteractionMediumCreateInput`, `InteractionMediumUpdateInput` to `network/api/schemas.py`
- [x] 2.2 Create `network/api/interaction_mediums.py` with CRUD router at `/api/interaction-mediums/` (list, create, update, delete) following `interaction_types.py` pattern
- [x] 2.3 Register the interaction mediums router in `network/api/__init__.py`
- [x] 2.4 Extend `InteractionSchema` with `interaction_medium_id: int | None`
- [x] 2.5 Extend `InteractionCreateInput` and `InteractionUpdateInput` with optional `interaction_medium_id`
- [x] 2.6 Update `_serialize_interaction()` in `network/api/interactions.py` to include `interaction_medium_id`
- [x] 2.7 Update `create_interaction()` and `update_interaction()` to handle the optional medium FK

## 3. Frontend API Client

- [x] 3.1 Add `InteractionMedium` type to `frontend/src/lib/api/types.ts`
- [x] 3.2 Add `interaction_medium_id: number | null` to `Interaction`, `CreateInteractionInput`, and `UpdateInteractionInput` types
- [x] 3.3 Add `interactionMediums` resource (getAll, create, update, remove) to `frontend/src/lib/api/client.ts`
- [x] 3.4 Export `InteractionMedium` from `frontend/src/lib/api/index.ts`

## 4. Frontend Interactions Page

- [x] 4.1 Add medium state variables (`interactionMediums`, `newMediumId`, `editMediumId`) and load mediums in `loadData()` in `frontend/src/routes/interactions/+page.svelte`
- [x] 4.2 Add `handleCreateInteractionMedium` function following the `handleCreateInteractionType` pattern
- [x] 4.3 Add medium TypeaheadSelect (with onCreate, placeholder "Medium") to the create form, after the type selector
- [x] 4.4 Add medium TypeaheadSelect to the detail/edit panel, after the type field
- [x] 4.5 Wire medium into `createInteraction()` and `saveInteraction()` — pass `interaction_medium_id` (null if not selected)
- [x] 4.6 Wire medium into `selectInteraction()` — populate `editMediumId` from selected interaction
- [x] 4.7 Update list item metadata line to show medium between type and date when present

## 5. Verification

- [x] 5.1 Run `frontend/npm run check` — no type errors
- [x] 5.2 Run backend API tests — no regressions
- [ ] 5.3 Manual test: create medium inline, create interaction with/without medium, edit medium on existing interaction, verify list display
