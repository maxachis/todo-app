## MODIFIED Requirements

### Requirement: Network list and detail views
The system SHALL provide list and detail views for people, organizations, and interactions in the Svelte UI. Each detail view SHALL include a "Linked Tasks" section showing tasks associated with the entity. Entity selection fields in create and edit forms SHALL use typeahead inputs instead of native dropdown selects. Type typeaheads on Organizations and Interactions pages SHALL support inline creation of new types via the TypeaheadSelect `onCreate` callback. The People list view SHALL include a sort control bar between the create form and the list, allowing the user to choose a sort field and toggle sort direction. The People list sort bar SHALL include a "Follow-up status" sort option in addition to the existing name and cadence sort fields. Each person in the People list SHALL display a follow-up status indicator when the person has a follow-up cadence set, showing the days since last interaction and cadence value with color-coded urgency (overdue, due soon, on track). The People detail panel SHALL display the most recent interaction date and type when available. The People detail panel SHALL display an overdue warning when the person is past their follow-up cadence. The People detail panel SHALL include a quick-log interaction form below the last-interaction summary. The quick-log interaction form SHALL include a TypeaheadSelect for interaction medium, placed after the interaction type selector and before the date input. The medium selector SHALL support inline creation of new mediums via the `onCreate` callback. The medium field SHALL be optional; when unset, the interaction SHALL be created with `interaction_medium_id: null`.

Each person row in the people list SHALL display the person's tags inline. The people list SHALL include a tag filter control that allows the user to filter displayed people by tag. The person detail view SHALL display tags near the top of the panel (after contact fields, before notes) and provide a TypeaheadSelect for adding tags with inline creation support via `onCreate` callback. Each displayed tag SHALL have a remove control to unlink it from the person.

The Interactions page create and edit forms SHALL use a multi-person selection UI instead of a single-person typeahead. The multi-person selection SHALL use the TypeaheadSelect component in onSelect callback mode to add people one at a time, displaying selected people as removable chips. The Interactions list view SHALL display all attendee names for each interaction, truncating to the first 2 names with a "+N more" indicator when there are more than 3 people.

The Relationships page SHALL include filter controls in both the Person ↔ Person and Organization → Person panels. Each filter SHALL be a TypeaheadSelect placed between the create form and the relationship list, allowing users to filter the displayed relationships by a specific person or organization. The filter SHALL auto-sync from the create form's primary field (Person A or Organization) and SHALL be independently editable. The secondary dropdown in each create form (Person B or Person) SHALL exclude entities that already have a relationship with the selected primary entity.

The Relationships page create forms SHALL include a TypeaheadSelect for relationship type, placed after the entity selectors and before the notes field. The person-person create form SHALL use person-person relationship types. The org-person create form SHALL use org-person relationship types. Both type selectors SHALL support inline creation via the `onCreate` callback, following the same pattern as org type and interaction type typeaheads. Each relationship row in the list SHALL display its relationship type name as a label when set. Existing relationships SHALL support inline editing of the relationship type via a TypeaheadSelect, following the same pattern as inline notes editing.

#### Scenario: Quick log form includes medium selector
- **WHEN** the user views a person's detail panel and sees the Quick Log Interaction form
- **THEN** a TypeaheadSelect for interaction medium SHALL be displayed after the interaction type selector and before the date input

#### Scenario: Quick log with medium selected
- **WHEN** the user selects an interaction type, medium, date, and submits the quick log form
- **THEN** the interaction is created with the selected `interaction_medium_id` via the API

#### Scenario: Quick log without medium
- **WHEN** the user submits the quick log form without selecting a medium
- **THEN** the interaction is created with `interaction_medium_id: null`

#### Scenario: Create medium inline from quick log form
- **WHEN** the user types a name into the medium typeahead that does not match any existing medium
- **THEN** a "Create [typed name]" option appears, and selecting it creates the medium via the API, adds it to the local medium list, and selects it in the typeahead

#### Scenario: Medium resets after successful quick log
- **WHEN** the user successfully submits a quick log interaction
- **THEN** the medium selector SHALL reset to unset along with the other form fields
