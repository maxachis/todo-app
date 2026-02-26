## MODIFIED Requirements

### Requirement: Network entities are first-class in the unified schema
The system SHALL include models for people, organizations, organization types, interaction types, interactions, relationships, and leads within the unified database.

#### Scenario: Network entities persist in unified database
- **WHEN** a person, organization, interaction, or lead is created
- **THEN** the record is stored in the unified database alongside task data

## ADDED Requirements

### Requirement: Tasks can link to leads
The system SHALL provide an explicit link table to associate tasks with leads, following the same pattern as task-person and task-organization links.

#### Scenario: Task linked to lead
- **WHEN** a task is linked to a lead
- **THEN** the link is persisted and retrievable from both the task and lead context
