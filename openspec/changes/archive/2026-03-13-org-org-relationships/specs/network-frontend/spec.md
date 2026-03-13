## ADDED Requirements

### Requirement: API client methods for org-org relationships and types
The system SHALL provide typed API client methods for org-org relationships (`api.relationships.orgOrg`) with `getAll()`, `create(payload)`, `update(id, payload)`, and `remove(id)` methods. The system SHALL provide typed API client methods for org-org relationship types (`api.relationshipTypes.orgOrg`) with `getAll()` and `create(payload)` methods.

#### Scenario: Fetch org-org relationships
- **WHEN** the client calls `api.relationships.orgOrg.getAll()`
- **THEN** a GET request is sent to `/relationships/org-org/` and the response is typed as `RelationshipOrganizationOrganization[]`

#### Scenario: Create org-org relationship type inline
- **WHEN** the client calls `api.relationshipTypes.orgOrg.create({ name: "Partner" })`
- **THEN** a POST request is sent to `/relationship-types/org-org/` and the response is typed as `OrgOrgRelationshipType`

### Requirement: Org-org relationship management in Relationships UI
The "Org ↔ Org" tab SHALL include a create form with Organization A typeahead, multi-select Organization B typeahead, relationship type typeahead with inline creation, and notes textarea. The tab SHALL include a filter by organization. The list SHALL display relationships as "Org A ↔ Org B" with inline type editing, inline notes editing, and delete button. The Organization B multi-select SHALL exclude organizations already connected to Organization A.

#### Scenario: Org-org create form excludes existing connections
- **WHEN** Organization A is selected and has existing org-org relationships
- **THEN** the Organization B dropdown SHALL only show organizations not yet connected to Organization A

#### Scenario: Org-org filter auto-syncs from Organization A
- **WHEN** the user selects an organization in the Organization A field of the create form
- **THEN** the filter control SHALL update to that organization and the list SHALL filter accordingly

## MODIFIED Requirements

### Requirement: Editable relationship notes on the Relationships page
The system SHALL allow users to edit the notes field on existing person-to-person, organization-to-person, and organization-to-organization relationships directly from the Relationships page.

#### Scenario: Edit person-to-person relationship notes via inline edit
- **WHEN** the user clicks on a person-to-person relationship's notes area (or edit button)
- **THEN** the notes area switches to an editable textarea pre-filled with the current notes text

#### Scenario: Save edited notes on blur
- **WHEN** the user edits relationship notes and blurs the textarea
- **THEN** the updated notes are saved via PUT to the appropriate relationship endpoint and the display updates immediately

#### Scenario: Cancel edit with Escape
- **WHEN** the user presses Escape while editing relationship notes
- **THEN** the edit is cancelled, the textarea reverts to the display view, and no API call is made

#### Scenario: Edit organization-to-person relationship notes
- **WHEN** the user clicks on an organization-to-person relationship's notes area (or edit button)
- **THEN** the notes area switches to an editable textarea, and saving works the same as for person-to-person relationships

#### Scenario: Edit organization-to-organization relationship notes
- **WHEN** the user clicks on an organization-to-organization relationship's notes area
- **THEN** the notes area switches to an editable textarea, and saving works the same as for other relationship types

#### Scenario: Add notes to a relationship with no existing notes
- **WHEN** a relationship has no notes and the user clicks the edit affordance
- **THEN** an empty textarea appears for entering notes, and saving persists the new notes

### Requirement: Network list and detail views
The system SHALL provide list and detail views for people, organizations, and interactions in the Svelte UI. Each detail view SHALL include a "Linked Tasks" section showing tasks associated with the entity. Entity selection fields in create and edit forms SHALL use typeahead inputs instead of native dropdown selects. Type typeaheads on Organizations and Interactions pages SHALL support inline creation of new types via the TypeaheadSelect `onCreate` callback. The People list view SHALL include a sort control bar between the create form and the list, allowing the user to choose a sort field and toggle sort direction. The People list sort bar SHALL include a "Follow-up status" sort option in addition to the existing name and cadence sort fields. Each person in the People list SHALL display a follow-up status indicator when the person has a follow-up cadence set, showing the days since last interaction and cadence value with color-coded urgency (overdue, due soon, on track). The People detail panel SHALL display the most recent interaction date and type when available. The People detail panel SHALL display an overdue warning when the person is past their follow-up cadence. The People detail panel SHALL include a quick-log interaction form below the last-interaction summary. The quick-log interaction form SHALL include a TypeaheadSelect for interaction medium, placed after the interaction type selector and before the date input. The medium selector SHALL support inline creation of new mediums via the `onCreate` callback. The medium field SHALL be optional; when unset, the interaction SHALL be created with `interaction_medium_id: null`.

Each person row in the people list SHALL display the person's tags inline. The people list SHALL include a tag filter control that allows the user to filter displayed people by tag. The person detail view SHALL display tags near the top of the panel (after contact fields, before notes) and provide a TypeaheadSelect for adding tags with inline creation support via `onCreate` callback. Each displayed tag SHALL have a remove control to unlink it from the person.

The Interactions page create and edit forms SHALL use a multi-person selection UI instead of a single-person typeahead. The multi-person selection SHALL use the TypeaheadSelect component in onSelect callback mode to add people one at a time, displaying selected people as removable chips. The Interactions list view SHALL display all attendee names for each interaction, truncating to the first 2 names with a "+N more" indicator when there are more than 3 people.

The Relationships page SHALL use a tabbed layout with tabs for "Person ↔ Person", "Org → Person", and "Org ↔ Org". Each tab SHALL include filter controls: a TypeaheadSelect placed between the create form and the relationship list, allowing users to filter the displayed relationships. The filter SHALL auto-sync from the create form's primary field and SHALL be independently editable. The secondary selector in each create form SHALL exclude entities that already have a relationship with the selected primary entity.

The Relationships page create forms SHALL include a TypeaheadSelect for relationship type, placed after the entity selectors and before the notes field. All three type selectors SHALL support inline creation via the `onCreate` callback. Each relationship row in the list SHALL display its relationship type name as a label when set. Existing relationships SHALL support inline editing of the relationship type via a TypeaheadSelect.

#### Scenario: Relationships page shows tabs
- **WHEN** the user navigates to the Relationships page
- **THEN** three tabs are displayed: "Person ↔ Person", "Org → Person", "Org ↔ Org"

#### Scenario: Relationships page shows filter controls
- **WHEN** the user navigates to the Relationships page
- **THEN** each tab SHALL display a filter TypeaheadSelect between the create form and the relationship list

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

#### Scenario: Org-org create form includes relationship type selector
- **WHEN** the user is filling in the org-org create form
- **THEN** a TypeaheadSelect for org-org relationship type is present after the organization selectors and before notes

#### Scenario: Create relationship type inline via typeahead
- **WHEN** a user types a name into the relationship type typeahead that does not match any existing type
- **THEN** a "Create [typed name]" option appears, and selecting it creates the type via the API, adds it to the local type list, and selects it in the typeahead

#### Scenario: Relationship list row displays type label
- **WHEN** a relationship has a type set
- **THEN** the list row displays the type name as a label

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
