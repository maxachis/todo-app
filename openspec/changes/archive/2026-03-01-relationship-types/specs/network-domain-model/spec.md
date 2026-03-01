## MODIFIED Requirements

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
