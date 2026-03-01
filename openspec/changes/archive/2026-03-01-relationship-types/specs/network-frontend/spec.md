## MODIFIED Requirements

### Requirement: Network list and detail views
The system SHALL provide list and detail views for people, organizations, and interactions in the Svelte UI. Each detail view SHALL include a "Linked Tasks" section showing tasks associated with the entity. Entity selection fields in create and edit forms SHALL use typeahead inputs instead of native dropdown selects. Type typeaheads on Organizations and Interactions pages SHALL support inline creation of new types via the TypeaheadSelect `onCreate` callback. The People list view SHALL include a sort control bar between the create form and the list, allowing the user to choose a sort field and toggle sort direction. The People list sort bar SHALL include a "Follow-up status" sort option in addition to the existing name and cadence sort fields. Each person in the People list SHALL display a follow-up status indicator when the person has a follow-up cadence set, showing the days since last interaction and cadence value with color-coded urgency (overdue, due soon, on track). The People detail panel SHALL display the most recent interaction date and type when available. The People detail panel SHALL display an overdue warning when the person is past their follow-up cadence. The People detail panel SHALL include a quick-log interaction form below the last-interaction summary.

Each person row in the people list SHALL display the person's tags inline. The people list SHALL include a tag filter control that allows the user to filter displayed people by tag. The person detail view SHALL display tags near the top of the panel (after contact fields, before notes) and provide a TypeaheadSelect for adding tags with inline creation support via `onCreate` callback. Each displayed tag SHALL have a remove control to unlink it from the person.

The Interactions page create and edit forms SHALL use a multi-person selection UI instead of a single-person typeahead. The multi-person selection SHALL use the TypeaheadSelect component in onSelect callback mode to add people one at a time, displaying selected people as removable chips. The Interactions list view SHALL display all attendee names for each interaction, truncating to the first 2 names with a "+N more" indicator when there are more than 3 people.

The Relationships page SHALL include filter controls in both the Person ↔ Person and Organization → Person panels. Each filter SHALL be a TypeaheadSelect placed between the create form and the relationship list, allowing users to filter the displayed relationships by a specific person or organization. The filter SHALL auto-sync from the create form's primary field (Person A or Organization) and SHALL be independently editable. The secondary dropdown in each create form (Person B or Person) SHALL exclude entities that already have a relationship with the selected primary entity.

The Relationships page create forms SHALL include a TypeaheadSelect for relationship type, placed after the entity selectors and before the notes field. The person-person create form SHALL use person-person relationship types. The org-person create form SHALL use org-person relationship types. Both type selectors SHALL support inline creation via the `onCreate` callback, following the same pattern as org type and interaction type typeaheads. Each relationship row in the list SHALL display its relationship type name as a label when set. Existing relationships SHALL support inline editing of the relationship type via a TypeaheadSelect, following the same pattern as inline notes editing.

#### Scenario: Relationships page shows filter controls
- **WHEN** the user navigates to the Relationships page
- **THEN** each panel SHALL display a filter TypeaheadSelect between the create form and the relationship list

#### Scenario: Person-person filter auto-syncs from Person A
- **WHEN** the user selects a person in the Person A field of the create form
- **THEN** the filter control SHALL update to that person and the list SHALL filter accordingly

#### Scenario: Person B dropdown excludes existing connections
- **WHEN** Person A is selected and has existing relationships
- **THEN** the Person B dropdown SHALL only show people not yet connected to Person A

#### Scenario: Person-person create form includes relationship type selector
- **WHEN** the user is filling in the person-person create form
- **THEN** a TypeaheadSelect for person-person relationship type is present after the person selectors and before notes

#### Scenario: Org-person create form includes relationship type selector
- **WHEN** the user is filling in the org-person create form
- **THEN** a TypeaheadSelect for org-person relationship type is present after the entity selectors and before notes

#### Scenario: Create relationship type inline via typeahead
- **WHEN** a user types a name into the relationship type typeahead that does not match any existing type
- **THEN** a "Create [typed name]" option appears, and selecting it creates the type via the API, adds it to the local type list, and selects it in the typeahead

#### Scenario: Relationship list row displays type label
- **WHEN** a relationship has a type set
- **THEN** the list row displays the type name as a label

#### Scenario: Relationship list row without type
- **WHEN** a relationship has no type set
- **THEN** the list row does not display a type label

#### Scenario: Edit relationship type inline
- **WHEN** the user clicks on a relationship's type area in the list
- **THEN** a TypeaheadSelect appears allowing the user to change or set the relationship type, and the change is saved via the API on selection

#### Scenario: View person detail with linked tasks
- **WHEN** a user selects a person from the list
- **THEN** the detail panel shows the person data, related interactions, and a "Linked Tasks" section listing tasks linked to that person

#### Scenario: View organization detail with linked tasks
- **WHEN** a user selects an organization from the list
- **THEN** the detail panel shows the organization data and a "Linked Tasks" section listing tasks linked to that organization

#### Scenario: View interaction detail with linked tasks
- **WHEN** a user selects an interaction from the list
- **THEN** the detail panel shows the interaction data and a "Linked Tasks" section listing tasks linked to that interaction

#### Scenario: Create org type inline via typeahead on Organizations page
- **WHEN** a user types a name into the org type typeahead (in the create or edit form) that does not match any existing org type
- **THEN** a "Create [typed name]" option appears, and selecting it creates the org type via the API, adds it to the local type list, and selects it in the typeahead

#### Scenario: Create interaction type inline via typeahead on Interactions page
- **WHEN** a user types a name into the interaction type typeahead (in the create or edit form) that does not match any existing interaction type
- **THEN** a "Create [typed name]" option appears, and selecting it creates the interaction type via the API, adds it to the local type list, and selects it in the typeahead

### Requirement: API client methods for relationship types
The system SHALL provide typed API client methods for listing and creating person-person and org-person relationship types. The relationship type client methods SHALL follow the same pattern as `api.orgTypes` and `api.interactionTypes`.

#### Scenario: List person-person relationship types
- **WHEN** the client calls `api.relationshipTypes.people.getAll()`
- **THEN** a GET request is sent to `/relationship-types/people/` and the response is typed as `PersonPersonRelationshipType[]`

#### Scenario: Create person-person relationship type
- **WHEN** the client calls `api.relationshipTypes.people.create({ name: "Coworker" })`
- **THEN** a POST request is sent to `/relationship-types/people/` and the response is typed as `PersonPersonRelationshipType`

#### Scenario: List org-person relationship types
- **WHEN** the client calls `api.relationshipTypes.organizations.getAll()`
- **THEN** a GET request is sent to `/relationship-types/organizations/` and the response is typed as `OrgPersonRelationshipType[]`

#### Scenario: Create org-person relationship type
- **WHEN** the client calls `api.relationshipTypes.organizations.create({ name: "CEO" })`
- **THEN** a POST request is sent to `/relationship-types/organizations/` and the response is typed as `OrgPersonRelationshipType`

### Requirement: API client update methods for relationships
The system SHALL provide typed API client methods for updating existing person-to-person and organization-to-person relationships. The update payloads SHALL accept an optional `relationship_type_id` field.

#### Scenario: Update person-to-person relationship
- **WHEN** the client calls `api.relationships.people.update(id, { notes, relationship_type_id })`
- **THEN** a PUT request is sent to `/relationships/people/{id}/` with the payload and the response is typed as `RelationshipPersonPerson`

#### Scenario: Update organization-to-person relationship
- **WHEN** the client calls `api.relationships.organizations.update(id, { notes, relationship_type_id })`
- **THEN** a PUT request is sent to `/relationships/organizations/{id}/` with the payload and the response is typed as `RelationshipOrganizationPerson`

### Requirement: Relationship create payloads include type
The relationship create API client methods SHALL accept an optional `relationship_type_id` field in their payloads.

#### Scenario: Create person-person relationship with type via client
- **WHEN** the client calls `api.relationships.people.create({ person_1_id, person_2_id, relationship_type_id })`
- **THEN** a POST request is sent to `/relationships/people/` including the `relationship_type_id` field

#### Scenario: Create org-person relationship with type via client
- **WHEN** the client calls `api.relationships.organizations.create({ organization_id, person_id, relationship_type_id })`
- **THEN** a POST request is sent to `/relationships/organizations/` including the `relationship_type_id` field
