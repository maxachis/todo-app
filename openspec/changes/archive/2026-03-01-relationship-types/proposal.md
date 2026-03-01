## Why

Relationships between people (and between people and organizations) currently have no categorization beyond free-text notes. Adding typed relationships — e.g., "Coworker", "Manager", "Friend" for person-to-person, or "CEO", "Board Member", "Advisor" for organization-to-person — enables filtering, grouping, and at-a-glance understanding of how entities are connected. This mirrors the existing type patterns used for organizations (`OrgType`) and interactions (`InteractionType`).

## What Changes

- Introduce two new type models: `PersonPersonRelationshipType` and `OrgPersonRelationshipType`, each with a `name` field following the existing type pattern (`OrgType`, `InteractionType`).
- Add an optional `relationship_type` foreign key to both `RelationshipPersonPerson` and `RelationshipOrganizationPerson`.
- Expose full CRUD API endpoints for both relationship type resources, mirroring the existing `/org-types/` and `/interaction-types/` routers.
- Add the relationship type field to the relationship create/edit forms on the frontend, using the `TypeaheadSelect` component with inline creation (`onCreate`) — consistent with how org types and interaction types work.
- Display the relationship type as a label in the relationship list rows.

## Non-goals

- Making relationship types required — they remain optional to preserve existing data and workflow flexibility.
- Adding relationship type management UI (dedicated list/edit page) — types are created inline via TypeaheadSelect, same as other types.
- Relationship directionality labels (e.g., "A manages B" vs "B reports to A") — the type applies symmetrically to the relationship for now.

## Capabilities

### New Capabilities
- `relationship-type-management`: CRUD API and models for person-person and org-person relationship types, following the existing type pattern.

### Modified Capabilities
- `network-domain-model`: Adding `relationship_type` FK to both relationship models.
- `network-api`: Adding relationship type endpoints and updating relationship create/update schemas to include `relationship_type_id`.
- `network-frontend`: Adding TypeaheadSelect for relationship types in the relationships page create/edit forms.

## Impact

- **Backend models**: New `PersonPersonRelationshipType` and `OrgPersonRelationshipType` models in `network/models/relationship/`; migration adding FK columns to existing relationship tables.
- **API**: New router for relationship types; updated relationship schemas and endpoints.
- **Frontend**: Updated relationships page with type selectors; new API client methods for relationship types; updated TypeScript types.
- **Database**: New tables + nullable FK columns on existing tables (non-breaking migration).
