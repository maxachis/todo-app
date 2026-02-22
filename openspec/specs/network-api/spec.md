### Requirement: Network API endpoints for people
The system SHALL expose JSON API endpoints to create, read, update, and delete people under the `/api/` prefix.

#### Scenario: Create a person
- **WHEN** a client sends POST to `/api/people/` with person fields
- **THEN** the server creates the person and responds with status 201 and the person object

### Requirement: Network API endpoints for organizations and types
The system SHALL expose JSON API endpoints to create, read, update, and delete organizations, org types, and interaction types.

#### Scenario: Create an organization
- **WHEN** a client sends POST to `/api/organizations/` with organization fields and an org type
- **THEN** the server creates the organization and responds with status 201 and the organization object

### Requirement: Network API endpoints for interactions and relationships
The system SHALL expose JSON API endpoints to create, read, update, and delete interactions and relationship records.

#### Scenario: Create an interaction
- **WHEN** a client sends POST to `/api/interactions/` with person, type, date, and notes
- **THEN** the server creates the interaction and responds with status 201 and the interaction object

### Requirement: Network API endpoints for task links
The system SHALL expose JSON API endpoints to create and remove links between tasks and people, organizations, and interactions.

#### Scenario: Link a task to a person
- **WHEN** a client sends POST to `/api/tasks/:id/people/` with a person id
- **THEN** the server creates the link and responds with status 201
