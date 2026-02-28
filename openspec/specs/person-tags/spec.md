## Purpose

Person tags allow categorizing and filtering people in the network CRM with user-defined labels (e.g., "investor", "mentor"). Tags are managed via a dedicated PersonTag model separate from the task Tag model.

## Requirements

### Requirement: PersonTag model
The system SHALL provide a `PersonTag` model with a unique `name` field (CharField, max 100). PersonTag SHALL be separate from the task `Tag` model. Person SHALL have a ManyToManyField to PersonTag (`tags`, blank=True).

#### Scenario: Create a person tag
- **WHEN** a PersonTag is created with name "investor"
- **THEN** the tag is persisted with that name

#### Scenario: PersonTag names are unique
- **WHEN** a PersonTag with name "investor" already exists and another is created with the same name
- **THEN** the creation fails with a uniqueness constraint violation

#### Scenario: Person can have multiple tags
- **WHEN** a person is associated with tags "investor" and "mentor"
- **THEN** both tags are retrievable from the person's tags set

#### Scenario: Tag can be associated with multiple people
- **WHEN** the tag "investor" is associated with two different people
- **THEN** both people are retrievable from the tag's person set

### Requirement: Person tag API endpoints
The system SHALL expose API endpoints to list all person tags, add a tag to a person, and remove a tag from a person.

#### Scenario: List all person tags
- **WHEN** a client sends GET to `/api/person-tags/`
- **THEN** the server responds with a list of all PersonTag objects ordered by name

#### Scenario: List person tags excluding a person's existing tags
- **WHEN** a client sends GET to `/api/person-tags/?exclude_person={id}`
- **THEN** the server responds with all PersonTag objects except those already assigned to the specified person

#### Scenario: Add tag to person
- **WHEN** a client sends POST to `/api/people/{id}/tags/` with `{"name": "investor"}`
- **THEN** the server creates the tag if it doesn't exist (get_or_create), associates it with the person, and responds with the person's updated tag list

#### Scenario: Add tag with blank name is rejected
- **WHEN** a client sends POST to `/api/people/{id}/tags/` with `{"name": ""}`
- **THEN** the server responds with status 400

#### Scenario: Remove tag from person
- **WHEN** a client sends DELETE to `/api/people/{id}/tags/{tag_id}/`
- **THEN** the server removes the association and responds with status 204

### Requirement: People list filterable by tag
The system SHALL support filtering the people list by tag name via query parameter.

#### Scenario: Filter people by tag
- **WHEN** a client sends GET to `/api/people/?tag=investor`
- **THEN** the server responds with only people who have the "investor" tag

#### Scenario: Filter with non-existent tag returns empty list
- **WHEN** a client sends GET to `/api/people/?tag=nonexistent`
- **THEN** the server responds with an empty list

### Requirement: Person API response includes tags
The person API response schema SHALL include a `tags` field containing an array of tag objects (id, name).

#### Scenario: Person response includes tags
- **WHEN** a client sends GET to `/api/people/` or `/api/people/{id}/`
- **THEN** each person object includes a `tags` array with objects containing `id` and `name`

#### Scenario: Person with no tags returns empty array
- **WHEN** a client sends GET for a person who has no tags
- **THEN** the `tags` field is an empty array

### Requirement: Person detail view tag management
The person detail view SHALL display tags near the top (after contact fields, before notes) and provide a TypeaheadSelect for adding tags with inline creation support.

#### Scenario: View tags on person detail
- **WHEN** a user selects a person with tags "investor" and "mentor"
- **THEN** the detail panel displays both tags near the top of the detail view

#### Scenario: Add tag via typeahead
- **WHEN** a user types a tag name into the tag typeahead and selects an existing tag
- **THEN** the tag is added to the person via the API and appears in the tag display

#### Scenario: Create new tag inline
- **WHEN** a user types a name that doesn't match any existing person tag
- **THEN** a "Create [typed name]" option appears, and selecting it creates the tag and adds it to the person

#### Scenario: Remove tag from person detail
- **WHEN** a user clicks the remove control on a tag in the person detail view
- **THEN** the tag is removed from the person via the API and disappears from the display

### Requirement: People list displays tags inline
Each person row in the people list SHALL display the person's tags inline.

#### Scenario: Person row shows tags
- **WHEN** the people list loads and a person has tags
- **THEN** the person's row displays the tag names

#### Scenario: Person row with no tags
- **WHEN** the people list loads and a person has no tags
- **THEN** no tag display is shown for that person

### Requirement: People list tag filter UI
The people list SHALL provide a UI control to filter by tag.

#### Scenario: Filter people list by tag
- **WHEN** the user selects a tag from the filter control
- **THEN** the people list reloads showing only people with that tag

#### Scenario: Clear tag filter
- **WHEN** the user clears the tag filter
- **THEN** the people list reloads showing all people
