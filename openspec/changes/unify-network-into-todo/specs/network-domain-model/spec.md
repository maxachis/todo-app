## ADDED Requirements

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
