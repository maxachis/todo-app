## Why

Interactions currently support only a single person, but real-world meetings, calls, and group events often involve multiple people. There is no way to record "I met with Alice, Bob, and Carol" as a single interaction — you must create three separate records, losing the shared context (same date, same notes, same meeting). Adding multi-person support lets you log a meeting once and tag everyone who attended.

## What Changes

- Add a many-to-many relationship between interactions and people, replacing the single `person` ForeignKey
- **BREAKING**: The `person_id` field on Interaction is removed; replaced by a `people` (M2M) association
- Update the create/edit interaction forms to accept multiple people via a multi-select typeahead
- Update the interaction list display to show all attendee names
- Update API schemas: create/update accept a list of `person_ids`; response includes `person_ids` list
- Migrate existing data: each existing interaction's `person_id` becomes the sole entry in its new M2M set

## Non-goals

- Adding a separate "Meeting" model or entity — meetings are just interactions with multiple people
- Calendar integration or scheduling
- Changing interaction types — the existing type system (Meeting, Call, Email, etc.) is sufficient
- Group/team concept — this is just about tagging multiple individuals on one interaction

## Capabilities

### New Capabilities

- `multi-person-interactions`: Interactions support a many-to-many relationship with people, allowing multiple attendees per interaction. Covers the data model change, API schema changes, frontend multi-select, list display, and data migration.

### Modified Capabilities

- `network-api`: API create/update/response schemas change from single `person_id` to a `person_ids` list
- `network-domain-model`: Interaction model changes from ForeignKey(Person) to ManyToManyField(Person)
- `network-frontend`: Interaction forms switch from single-person typeahead to multi-person select; list items show all attendee names

## Impact

- **Backend model**: `network/models/interaction.py` — replace `person` FK with M2M `people` field
- **Migration**: Data migration to move existing `person_id` values into the new M2M table
- **API**: `network/api/interactions.py` and `network/api/schemas.py` — updated schemas and serialization
- **Frontend**: `frontend/src/routes/interactions/+page.svelte` — multi-select person picker in create/edit forms, updated list item display
- **API client types**: `frontend/src/lib/api/types.ts` and `frontend/src/lib/api/client.ts` — updated Interaction type
- **People API**: `network/api/people.py` — `last_interaction_date`/`last_interaction_type` annotation queries need updating since the FK relationship changes to M2M
- **Existing specs affected**: network-api, network-domain-model, network-frontend
