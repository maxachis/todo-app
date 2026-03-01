### Requirement: Network entities are first-class in the unified schema
The system SHALL include models for people, organizations, organization types, interaction types, interaction mediums, interactions, relationships, and leads within the unified database. The Interaction model SHALL associate with people via a ManyToManyField (`people`) instead of a single ForeignKey. The Interaction model SHALL also associate with organizations via a ManyToManyField (`organizations`, blank=True). The Interaction model SHALL have an optional ForeignKey to InteractionMedium (`medium`, null=True, blank=True, on_delete=SET_NULL). The `RelationshipPersonPerson` model SHALL have an optional ForeignKey to `PersonPersonRelationshipType` (`relationship_type`, null=True, blank=True, on_delete=SET_NULL). The `RelationshipOrganizationPerson` model SHALL have an optional ForeignKey to `OrgPersonRelationshipType` (`relationship_type`, null=True, blank=True, on_delete=SET_NULL).

#### Scenario: Network entities persist in unified database
- **WHEN** a person, organization, interaction, or lead is created
- **THEN** the record is stored in the unified database alongside task data

#### Scenario: Interaction associates with multiple people
- **WHEN** an interaction is created and associated with multiple people
- **THEN** all person associations are stored via the M2M relationship and retrievable from the interaction

#### Scenario: Interaction associates with organizations
- **WHEN** an interaction is created and associated with one or more organizations
- **THEN** all organization associations are stored via the M2M relationship and retrievable from the interaction

#### Scenario: Interaction has optional medium
- **WHEN** an interaction is created without specifying a medium
- **THEN** the interaction is persisted with `medium` set to null

#### Scenario: Interaction with medium set
- **WHEN** an interaction is created with a medium of "Email"
- **THEN** the interaction is persisted with the `medium` FK pointing to the InteractionMedium record

#### Scenario: Deleting a medium nullifies interaction references
- **WHEN** an InteractionMedium is deleted and interactions reference it
- **THEN** those interactions have their `medium` field set to null

#### Scenario: Person-person relationship with type
- **WHEN** a person-person relationship is created with `relationship_type` set to a `PersonPersonRelationshipType` record
- **THEN** the relationship is persisted with the type FK set

#### Scenario: Person-person relationship without type
- **WHEN** a person-person relationship is created without specifying a relationship type
- **THEN** the relationship is persisted with `relationship_type` set to null

#### Scenario: Deleting a person-person relationship type nullifies references
- **WHEN** a `PersonPersonRelationshipType` is deleted and relationships reference it
- **THEN** those relationships have their `relationship_type` field set to null

#### Scenario: Org-person relationship with type
- **WHEN** an org-person relationship is created with `relationship_type` set to an `OrgPersonRelationshipType` record
- **THEN** the relationship is persisted with the type FK set

#### Scenario: Org-person relationship without type
- **WHEN** an org-person relationship is created without specifying a relationship type
- **THEN** the relationship is persisted with `relationship_type` set to null

#### Scenario: Deleting an org-person relationship type nullifies references
- **WHEN** an `OrgPersonRelationshipType` is deleted and relationships reference it
- **THEN** those relationships have their `relationship_type` field set to null

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

### Requirement: Person has tags via PersonTag
The Person model SHALL include a ManyToManyField to PersonTag (`tags`, blank=True, related_name="people"). PersonTag SHALL be a separate model in the network domain with a unique `name` field (CharField, max 100).

#### Scenario: Person with tags
- **WHEN** a person is created and associated with PersonTag records
- **THEN** the tags are retrievable via the person's `tags` M2M field

### Requirement: Tasks can link to leads
The system SHALL provide an explicit link table to associate tasks with leads, following the same pattern as task-person and task-organization links.

#### Scenario: Task linked to lead
- **WHEN** a task is linked to a lead
- **THEN** the link is persisted and retrievable from both the task and lead context
