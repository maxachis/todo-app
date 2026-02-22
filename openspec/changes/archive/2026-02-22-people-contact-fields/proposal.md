## Why

People in the network currently have no contact information fields. Adding email and LinkedIn URL allows quick access to contact details when viewing or managing people, without needing to dig through notes.

## What Changes

- Add `email` and `linkedin_url` fields to the Person model (both optional)
- Include both fields in the create and edit forms on the People page
- Include both fields in the API create/update/response schemas
- Display email as a clickable `mailto:` link and LinkedIn as a clickable URL in the detail panel

## Capabilities

### New Capabilities

None — this extends an existing capability.

### Modified Capabilities

- `network-domain-model`: Add `email` and `linkedin_url` fields to Person
- `network-api`: Include new fields in Person create, update, and response schemas
- `network-frontend`: Add email and LinkedIn inputs to create and edit forms; display as clickable links in detail view

## Impact

- **Database**: New migration adding two nullable text columns to `network_person`
- **Backend**: `network/models/person.py`, `network/api/schemas.py`, `network/api/people.py` updated
- **Frontend**: `frontend/src/routes/people/+page.svelte` updated with new form fields; `frontend/src/lib/api/types.ts` updated with new type fields
- **No new dependencies**
