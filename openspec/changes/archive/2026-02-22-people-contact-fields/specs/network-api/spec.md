## MODIFIED Requirements

### Requirement: Network API endpoints for people
The system SHALL expose JSON API endpoints to create, read, update, and delete people under the `/api/` prefix. The create and update schemas SHALL accept optional `email` and `linkedin_url` fields. The response schema SHALL include `email` and `linkedin_url` fields.

#### Scenario: Create a person
- **WHEN** a client sends POST to `/api/people/` with person fields
- **THEN** the server creates the person and responds with status 201 and the person object

#### Scenario: Create a person with contact fields
- **WHEN** a client sends POST to `/api/people/` with `email` and `linkedin_url` in the payload
- **THEN** the server creates the person with those contact fields and includes them in the 201 response

#### Scenario: Update a person's contact fields
- **WHEN** a client sends PUT to `/api/people/{id}/` with `email` or `linkedin_url`
- **THEN** the server updates the specified contact fields and returns the updated person object

#### Scenario: Person response includes contact fields
- **WHEN** a client sends GET to `/api/people/{id}/`
- **THEN** the response includes `email` and `linkedin_url` fields (empty string if not set)
