## MODIFIED Requirements

### Requirement: Network entities are first-class in the unified schema
The system SHALL include models for people, organizations, organization types, interaction types, interactions, relationships, and leads within the unified database. The Interaction model SHALL associate with people via a ManyToManyField (`people`) instead of a single ForeignKey.

#### Scenario: Network entities persist in unified database
- **WHEN** a person, organization, interaction, or lead is created
- **THEN** the record is stored in the unified database alongside task data

#### Scenario: Interaction associates with multiple people
- **WHEN** an interaction is created and associated with multiple people
- **THEN** all person associations are stored via the M2M relationship and retrievable from the interaction
