## 1. Backend Model & Migrations

- [x] 1.1 Add `people` ManyToManyField(Person, blank=True) to Interaction model in `network/models/interaction.py`, keeping the existing `person` FK temporarily
- [x] 1.2 Run `makemigrations` to generate the schema migration adding the M2M field
- [x] 1.3 Create a data migration that copies each interaction's `person_id` into its `people` M2M set
- [x] 1.4 Remove the `person` ForeignKey from the Interaction model
- [x] 1.5 Run `makemigrations` to generate the schema migration removing the FK
- [x] 1.6 Run `migrate` and verify all migrations apply cleanly

## 2. Backend API Schemas

- [x] 2.1 Update `InteractionSchema` in `network/api/schemas.py`: replace `person_id: int` with `person_ids: list[int]`
- [x] 2.2 Update `InteractionCreateInput`: replace `person_id: int` with `person_ids: list[int]` (required, min 1)
- [x] 2.3 Update `InteractionUpdateInput`: replace `person_id: Optional[int]` with `person_ids: Optional[list[int]]`

## 3. Backend API Router

- [x] 3.1 Update `_serialize_interaction` in `network/api/interactions.py` to return `person_ids` from the M2M set
- [x] 3.2 Update `create_interaction` to accept `person_ids` list, validate all person IDs exist, create interaction, then set M2M people
- [x] 3.3 Update `update_interaction` to handle optional `person_ids` — when provided, call `interaction.people.set(person_ids)`
- [x] 3.4 Update `list_interactions` to prefetch `people` for performance

## 4. People API Annotation Fix

- [x] 4.1 Update `_annotate_people` in `network/api/people.py` to derive `last_interaction_date` and `last_interaction_type` via the M2M reverse relationship instead of the old FK

## 5. Frontend Types & API Client

- [x] 5.1 Update `Interaction` interface in `frontend/src/lib/api/types.ts`: replace `person_id: number` with `person_ids: number[]`
- [x] 5.2 Update `CreateInteractionInput`: replace `person_id: number` with `person_ids: number[]`
- [x] 5.3 Update `UpdateInteractionInput`: replace `person_id?: number` with `person_ids?: number[]`

## 6. Frontend Interaction Page

- [x] 6.1 Update create form in `frontend/src/routes/interactions/+page.svelte`: replace single `newPersonId` state with `newPersonIds: number[]` array; use TypeaheadSelect in `onSelect` mode to add people; render selected people as removable chips
- [x] 6.2 Update edit form: replace single `editPersonId` with `editPersonIds: number[]` array; load from `selected.person_ids`; same chip UI as create form
- [x] 6.3 Update `createInteraction` handler to send `person_ids` array
- [x] 6.4 Update `saveInteraction` handler to send `person_ids` array
- [x] 6.5 Update `selectInteraction` to populate `editPersonIds` from `selected.person_ids`
- [x] 6.6 Update interaction list item display: show all attendee names, truncate to first 2 with "+N more" when >3 people
- [x] 6.7 Update detail header to show all attendee names instead of single person

## 7. Testing

- [x] 7.1 Add/update API tests in `tasks/tests/` for interaction CRUD with `person_ids` (create with multiple, update, response format)
- [x] 7.2 Verify `last_interaction_date`/`last_interaction_type` annotations work correctly with M2M (person appears in interaction with multiple attendees)
- [x] 7.3 Run `npm run check` in frontend to verify no type errors
