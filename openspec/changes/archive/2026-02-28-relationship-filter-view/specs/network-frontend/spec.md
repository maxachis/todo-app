## MODIFIED Requirements

### Requirement: Network list and detail views
The system SHALL provide list and detail views for people, organizations, and interactions in the Svelte UI. Each detail view SHALL include a "Linked Tasks" section showing tasks associated with the entity. Entity selection fields in create and edit forms SHALL use typeahead inputs instead of native dropdown selects. Type typeaheads on Organizations and Interactions pages SHALL support inline creation of new types via the TypeaheadSelect `onCreate` callback. The People list view SHALL include a sort control bar between the create form and the list, allowing the user to choose a sort field and toggle sort direction. The People list sort bar SHALL include a "Follow-up status" sort option in addition to the existing name and cadence sort fields. Each person in the People list SHALL display a follow-up status indicator when the person has a follow-up cadence set, showing the days since last interaction and cadence value with color-coded urgency (overdue, due soon, on track). The People detail panel SHALL display the most recent interaction date and type when available. The People detail panel SHALL display an overdue warning when the person is past their follow-up cadence. The People detail panel SHALL include a quick-log interaction form below the last-interaction summary.

The Interactions page create and edit forms SHALL use a multi-person selection UI instead of a single-person typeahead. The multi-person selection SHALL use the TypeaheadSelect component in onSelect callback mode to add people one at a time, displaying selected people as removable chips. The Interactions list view SHALL display all attendee names for each interaction, truncating to the first 2 names with a "+N more" indicator when there are more than 3 people.

The Relationships page SHALL include filter controls in both the Person ↔ Person and Organization → Person panels. Each filter SHALL be a TypeaheadSelect placed between the create form and the relationship list, allowing users to filter the displayed relationships by a specific person or organization. The filter SHALL auto-sync from the create form's primary field (Person A or Organization) and SHALL be independently editable. The secondary dropdown in each create form (Person B or Person) SHALL exclude entities that already have a relationship with the selected primary entity.

#### Scenario: Relationships page shows filter controls
- **WHEN** the user navigates to the Relationships page
- **THEN** each panel SHALL display a filter TypeaheadSelect between the create form and the relationship list

#### Scenario: Person-person filter auto-syncs from Person A
- **WHEN** the user selects a person in the Person A field of the create form
- **THEN** the filter control SHALL update to that person and the list SHALL filter accordingly

#### Scenario: Person B dropdown excludes existing connections
- **WHEN** Person A is selected and has existing relationships
- **THEN** the Person B dropdown SHALL only show people not yet connected to Person A
