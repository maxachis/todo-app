### Requirement: Network entities are first-class in the unified schema
The system SHALL include models for people, organizations, organization types, interaction types, interactions, and relationships within the unified database.

#### Scenario: Network entities persist in unified database
- **WHEN** a person, organization, or interaction is created
- **THEN** the record is stored in the unified database alongside task data

### Requirement: Tasks can link to people, organizations, and interactions
The system SHALL provide explicit link tables to associate tasks with people, organizations, and interactions.

#### Scenario: Task linked to person and organization
- **WHEN** a task is linked to both a person and an organization
- **THEN** both links are persisted and retrievable without altering the task or network entity records

### Requirement: Interaction-to-task links are supported
The system SHALL allow interactions to be linked to one or more tasks via a dedicated link table.

#### Scenario: Interaction linked to task
- **WHEN** an interaction is linked to a task
- **THEN** the association is stored and can be retrieved from both the interaction and task context

### Requirement: Person has email and LinkedIn contact fields
The Person model SHALL include an optional `email` field (CharField, max 255, blank) and an optional `linkedin_url` field (CharField, max 500, blank) for storing contact information.

#### Scenario: Create person with email and LinkedIn
- **WHEN** a person is created with `email` set to "jane@example.com" and `linkedin_url` set to "https://linkedin.com/in/jane"
- **THEN** both values are persisted on the person record

#### Scenario: Create person without contact fields
- **WHEN** a person is created without providing `email` or `linkedin_url`
- **THEN** both fields default to empty strings

#### Scenario: Update person contact fields
- **WHEN** a person's `email` or `linkedin_url` is updated
- **THEN** the new values are persisted and the `updated_at` timestamp changes
