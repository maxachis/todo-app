## Context

Relationships (`RelationshipPersonPerson` and `RelationshipOrganizationPerson`) currently store only FK references and a `notes` text field. Other entity associations in the app (organizations, interactions) have dedicated type models (`OrgType`, `InteractionType`, `InteractionMedium`) — simple `name`-only models with full CRUD APIs and frontend TypeaheadSelect with inline creation. Relationships lack this categorization.

## Goals / Non-Goals

**Goals:**
- Add typed categorization to both person-person and org-person relationships
- Follow the established type pattern exactly (model, API, frontend TypeaheadSelect with `onCreate`)
- Keep relationship types optional (nullable FK) so existing data is unaffected

**Non-Goals:**
- Directional/asymmetric type labels (e.g., "A manages B" / "B reports to A")
- Dedicated type management pages (types are managed inline via TypeaheadSelect)
- Making types required or adding validation beyond the existing blank-name rejection

## Decisions

### 1. Two separate type models vs one shared model

**Decision:** Two separate models — `PersonPersonRelationshipType` and `OrgPersonRelationshipType`.

**Rationale:** Person-to-person relationship types ("Coworker", "Friend", "Mentor") are semantically different from org-to-person types ("CEO", "Board Member", "Advisor"). Separate models keep the type lists clean and contextually relevant. This matches how `OrgType` and `InteractionType` are distinct models even though they have identical structure.

**Alternative considered:** A single `RelationshipType` with a `category` enum field. Rejected because it would mix unrelated type lists in the TypeaheadSelect dropdowns and add filtering complexity.

### 2. Nullable FK on relationship models

**Decision:** Add `relationship_type` as a nullable ForeignKey with `on_delete=SET_NULL` on both relationship models.

**Rationale:** Matches the existing pattern (`InteractionMedium` on `Interaction` uses `SET_NULL`). Preserves all existing relationships without requiring a data migration to backfill types. Deleting a type nullifies the reference rather than cascading deletes to relationships.

### 3. API structure: dedicated router vs extending relationships router

**Decision:** Add a new `relationship_types.py` router with endpoints under `/relationship-types/people/` and `/relationship-types/organizations/`, registered alongside the existing type routers.

**Rationale:** Follows the pattern of `org_types.py` and `interaction_types.py` as standalone routers. Keeps the relationships router focused on relationship CRUD. The sub-path `/people/` and `/organizations/` disambiguates the two type categories under a shared prefix.

### 4. Frontend: TypeaheadSelect placement in relationship forms

**Decision:** Add a TypeaheadSelect for relationship type in each create form (person-person and org-person), placed after the entity selectors and before notes. Display the type label in list rows. Support inline editing of type on existing relationships.

**Rationale:** Consistent with how org type and interaction type selectors work on their respective pages. The `onCreate` callback enables inline creation without leaving the form.

## Risks / Trade-offs

- **Migration on existing tables** → Non-breaking: nullable FK columns with default NULL. No data loss or backfill needed.
- **Two type tables with identical structure** → Minimal overhead. Could be consolidated later if requirements change, but separate tables are simpler now.
- **No type uniqueness constraint** → Matches existing type models (`OrgType`, `InteractionType` also lack `unique=True` on `name`). Inline creation via TypeaheadSelect naturally avoids duplicates since users see existing options first.
