### Requirement: Network navigation in Svelte UI
The system SHALL provide Svelte routes and navigation entries for People, Organizations, Interactions, Relationships, and Graph.

#### Scenario: Navigate to People view
- **WHEN** a user selects People from the main navigation
- **THEN** the People view loads in the Svelte app without full-page reload

### Requirement: Network list and detail views
The system SHALL provide list and detail views for people, organizations, and interactions in the Svelte UI. Each detail view SHALL include a "Linked Tasks" section showing tasks associated with the entity. Entity selection fields in create and edit forms SHALL use typeahead inputs instead of native dropdown selects. Type typeaheads on Organizations and Interactions pages SHALL support inline creation of new types via the TypeaheadSelect `onCreate` callback. The People list view SHALL include a sort control bar between the create form and the list, allowing the user to choose a sort field and toggle sort direction. The People list sort bar SHALL include a "Follow-up status" sort option in addition to the existing name and cadence sort fields. Each person in the People list SHALL display a follow-up status indicator when the person has a follow-up cadence set, showing the days since last interaction and cadence value with color-coded urgency (overdue, due soon, on track). The People detail panel SHALL display the most recent interaction date and type when available. The People detail panel SHALL display an overdue warning when the person is past their follow-up cadence. The People detail panel SHALL include a quick-log interaction form below the last-interaction summary.

Each person row in the people list SHALL display the person's tags inline. The people list SHALL include a tag filter control that allows the user to filter displayed people by tag. The person detail view SHALL display tags near the top of the panel (after contact fields, before notes) and provide a TypeaheadSelect for adding tags with inline creation support via `onCreate` callback. Each displayed tag SHALL have a remove control to unlink it from the person.

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

#### Scenario: View person detail with linked tasks
- **WHEN** a user selects a person from the list
- **THEN** the detail panel shows the person data, related interactions, and a "Linked Tasks" section listing tasks linked to that person

#### Scenario: View organization detail with linked tasks
- **WHEN** a user selects an organization from the list
- **THEN** the detail panel shows the organization data and a "Linked Tasks" section listing tasks linked to that organization

#### Scenario: View interaction detail with linked tasks
- **WHEN** a user selects an interaction from the list
- **THEN** the detail panel shows the interaction data and a "Linked Tasks" section listing tasks linked to that interaction

#### Scenario: Linked tasks section supports add and remove
- **WHEN** a person, organization, or interaction detail view is displayed
- **THEN** the "Linked Tasks" section provides a typeahead input to search and link new tasks and a remove button on each linked task to unlink it

#### Scenario: Person detail displays tags near top
- **WHEN** a user selects a person with tags
- **THEN** the detail panel displays tags after contact fields and before notes, with remove controls on each tag

#### Scenario: Person detail tag typeahead with inline creation
- **WHEN** a user types a name into the tag typeahead on the person detail that doesn't match any existing person tag
- **THEN** a "Create [typed name]" option appears, and selecting it creates the tag and adds it to the person

#### Scenario: Person list rows show tags inline
- **WHEN** the people list loads and a person has tags
- **THEN** the person's row displays the tag names inline

#### Scenario: People list tag filter
- **WHEN** the user selects a tag from the tag filter control on the people list
- **THEN** the list reloads showing only people with that tag

#### Scenario: Clear people list tag filter
- **WHEN** the user clears the tag filter
- **THEN** the list reloads showing all people

#### Scenario: Create org type inline via typeahead on Organizations page
- **WHEN** a user types a name into the org type typeahead (in the create or edit form) that does not match any existing org type
- **THEN** a "Create [typed name]" option appears, and selecting it creates the org type via the API, adds it to the local type list, and selects it in the typeahead

#### Scenario: Create interaction type inline via typeahead on Interactions page
- **WHEN** a user types a name into the interaction type typeahead (in the create or edit form) that does not match any existing interaction type
- **THEN** a "Create [typed name]" option appears, and selecting it creates the interaction type via the API, adds it to the local type list, and selects it in the typeahead

#### Scenario: Add multiple people in interaction create form
- **WHEN** a user selects "Alice" then "Bob" from the person typeahead in the interaction create form
- **THEN** both appear as removable chips and both person IDs are included when the form is submitted

#### Scenario: Remove a person from interaction create form
- **WHEN** the user clicks the remove control on a person chip in the interaction create form
- **THEN** that person is removed from the selection

#### Scenario: Edit interaction loads existing people as chips
- **WHEN** the user selects an interaction that has multiple people
- **THEN** the edit form shows all associated people as removable chips in the person selection area

#### Scenario: Interaction list shows multiple attendee names
- **WHEN** an interaction with people "Doe, Jane" and "Smith, Bob" appears in the list
- **THEN** the list item title shows both names

#### Scenario: Interaction list truncates many attendees
- **WHEN** an interaction with 5 people appears in the list
- **THEN** the list item title shows the first 2 names followed by "+3 more"

#### Scenario: Select interaction type via typeahead in interaction create form
- **WHEN** a user types into the interaction type field of the interaction create form
- **THEN** a filtered list of interaction types appears matching the typed text, and selecting one sets the type for the new interaction

#### Scenario: Select interaction type via typeahead in interaction edit form
- **WHEN** a user types into the interaction type field of the interaction edit form
- **THEN** a filtered list of interaction types appears matching the typed text, and selecting one updates the type for the interaction

#### Scenario: Select org type via typeahead in organization create form
- **WHEN** a user types into the org type field of the organization create form
- **THEN** a filtered list of org types appears matching the typed text, and selecting one sets the org type for the new organization

#### Scenario: Select org type via typeahead in organization edit form
- **WHEN** a user types into the org type field of the organization edit form
- **THEN** a filtered list of org types appears matching the typed text, and selecting one updates the org type for the organization

#### Scenario: People list includes sort controls
- **WHEN** the People page loads
- **THEN** a sort control bar is visible between the create form and the people list, showing the active sort field and direction

#### Scenario: People list includes follow-up status sort option
- **WHEN** the user opens the sort field dropdown on the People page
- **THEN** "Follow-up status" appears as a sort option alongside existing name and cadence options

#### Scenario: People list items show follow-up status
- **WHEN** the People page loads and a person has a follow-up cadence set
- **THEN** the list item displays a color-coded status indicator with days-since and cadence values

#### Scenario: People detail shows last interaction
- **WHEN** a user selects a person who has recorded interactions
- **THEN** the detail panel displays the date and type of their most recent interaction

#### Scenario: People detail shows overdue warning
- **WHEN** a user selects a person who is overdue for follow-up
- **THEN** the detail panel displays a visual overdue warning

#### Scenario: People detail includes quick-log interaction form
- **WHEN** a user selects a person from the list
- **THEN** the detail panel includes an inline form to log a new interaction with type selector and date field defaulting to today

### Requirement: Editable relationship notes on the Relationships page
The system SHALL allow users to edit the notes field on existing person-to-person and organization-to-person relationships directly from the Relationships page.

#### Scenario: Edit person-to-person relationship notes via inline edit
- **WHEN** the user clicks on a person-to-person relationship's notes area (or edit button)
- **THEN** the notes area switches to an editable textarea pre-filled with the current notes text

#### Scenario: Save edited notes on blur
- **WHEN** the user edits relationship notes and blurs the textarea
- **THEN** the updated notes are saved via PUT to `/relationships/people/{id}/` (or `/relationships/organizations/{id}/`) and the display updates immediately

#### Scenario: Cancel edit with Escape
- **WHEN** the user presses Escape while editing relationship notes
- **THEN** the edit is cancelled, the textarea reverts to the display view, and no API call is made

#### Scenario: Edit organization-to-person relationship notes
- **WHEN** the user clicks on an organization-to-person relationship's notes area (or edit button)
- **THEN** the notes area switches to an editable textarea, and saving works the same as for person-to-person relationships

#### Scenario: Add notes to a relationship with no existing notes
- **WHEN** a relationship has no notes and the user clicks the edit affordance
- **THEN** an empty textarea appears for entering notes, and saving persists the new notes

### Requirement: API client update methods for relationships
The system SHALL provide typed API client methods for updating existing person-to-person and organization-to-person relationships.

#### Scenario: Update person-to-person relationship
- **WHEN** the client calls `api.relationships.people.update(id, { notes })`
- **THEN** a PUT request is sent to `/relationships/people/{id}/` with the payload and the response is typed as `RelationshipPersonPerson`

#### Scenario: Update organization-to-person relationship
- **WHEN** the client calls `api.relationships.organizations.update(id, { notes })`
- **THEN** a PUT request is sent to `/relationships/organizations/{id}/` with the payload and the response is typed as `RelationshipOrganizationPerson`

### Requirement: People create form includes email and LinkedIn fields
The People page create form SHALL include optional text inputs for email and LinkedIn URL, placed after the name fields and before follow-up cadence.

#### Scenario: Create person with email and LinkedIn
- **WHEN** the user fills in the create form including email and LinkedIn fields and submits
- **THEN** the person is created with those contact fields via the API

#### Scenario: Create person without contact fields
- **WHEN** the user submits the create form with email and LinkedIn fields empty
- **THEN** the person is created without contact information

### Requirement: People edit form includes email and LinkedIn fields
The People page detail/edit panel SHALL include text inputs for email and LinkedIn URL, reflecting the person's current values.

#### Scenario: Edit person email
- **WHEN** the user changes the email field in the edit form and saves
- **THEN** the updated email is sent to the API and persisted

#### Scenario: Edit person LinkedIn URL
- **WHEN** the user changes the LinkedIn URL field in the edit form and saves
- **THEN** the updated LinkedIn URL is sent to the API and persisted

### Requirement: People detail view displays contact fields as clickable links
The People page detail panel SHALL display a non-empty email as a clickable `mailto:` link and a non-empty LinkedIn URL as a clickable external link opening in a new tab.

#### Scenario: Display email as mailto link
- **WHEN** a person has a non-empty email and is selected in the detail panel
- **THEN** the email is rendered as a clickable `mailto:` link

#### Scenario: Display LinkedIn as external link
- **WHEN** a person has a non-empty LinkedIn URL and is selected in the detail panel
- **THEN** the LinkedIn URL is rendered as a clickable link that opens in a new tab

#### Scenario: Empty contact fields are not displayed as links
- **WHEN** a person has empty email and LinkedIn fields
- **THEN** no contact links are shown in the detail panel

### Requirement: Graph visualization parity
The system SHALL present the network graph in Svelte with equivalent behavior to the existing network app visualization. Graph node, edge, and label colors SHALL be derived from the app's CSS variable theme system rather than hardcoded hex values. Organization nodes SHALL use the `--accent` color. Person nodes SHALL use the `--text-tertiary` color. Edge lines SHALL use the `--border` color. Edge note labels SHALL use the `--text-tertiary` color. Node text labels SHALL use the `--text-primary` color. Graph colors SHALL update automatically when the user toggles between light and dark themes.

#### Scenario: View graph
- **WHEN** a user opens the Graph view
- **THEN** the graph renders with the same data and interactions as the legacy network app

#### Scenario: Graph node colors match theme
- **WHEN** the graph renders in the current theme
- **THEN** organization nodes SHALL use the `--accent` color and person nodes SHALL use the `--text-tertiary` color

#### Scenario: Graph edge colors match theme
- **WHEN** the graph renders in the current theme
- **THEN** edge lines SHALL use the `--border` color and edge note labels SHALL use the `--text-tertiary` color

#### Scenario: Graph label colors match theme
- **WHEN** the graph renders in the current theme
- **THEN** node text labels SHALL use the `--text-primary` color

#### Scenario: Graph colors update on theme toggle
- **WHEN** the user switches between light and dark mode while viewing the graph
- **THEN** all graph node, edge, and label colors SHALL update to reflect the new theme's CSS variable values without losing the current graph layout or zoom state
