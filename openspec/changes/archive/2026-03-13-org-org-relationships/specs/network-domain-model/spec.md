## ADDED Requirements

### Requirement: Organization-organization relationship entity
The system SHALL include `RelationshipOrganizationOrganization` and `OrgOrgRelationshipType` models within the network domain. The `RelationshipOrganizationOrganization` model SHALL have an optional ForeignKey to `OrgOrgRelationshipType` (`relationship_type`, null=True, blank=True, on_delete=SET_NULL), following the same pattern as person-person and org-person relationships.

#### Scenario: Org-org relationship persists in unified database
- **WHEN** an org-org relationship is created
- **THEN** the record is stored in the unified database alongside other network entities

#### Scenario: Org-org relationship with type
- **WHEN** an org-org relationship is created with `relationship_type` set to an `OrgOrgRelationshipType` record
- **THEN** the relationship is persisted with the type FK set

#### Scenario: Deleting an org-org relationship type nullifies references
- **WHEN** an `OrgOrgRelationshipType` is deleted and relationships reference it
- **THEN** those relationships have their `relationship_type` field set to null
