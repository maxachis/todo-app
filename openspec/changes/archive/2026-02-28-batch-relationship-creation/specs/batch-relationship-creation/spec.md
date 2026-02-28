## ADDED Requirements

### Requirement: Multi-person selection for person-person relationship creation
The person-person create form SHALL replace the single Person B TypeaheadSelect with a multi-person chip selector. The TypeaheadSelect SHALL use `onSelect` callback mode. Selecting a person SHALL add them as a removable chip. The chip list SHALL be displayed below the typeahead. The typeahead SHALL exclude people already selected as chips, in addition to existing exclusions (Person A and already-connected people).

#### Scenario: Select multiple people as Person B
- **WHEN** the user selects "Doe, Jane" then "Brown, Alice" from the Person B typeahead
- **THEN** both SHALL appear as removable chips and the typeahead SHALL clear after each selection

#### Scenario: Remove a person chip
- **WHEN** the user clicks the remove button on a person chip
- **THEN** that person SHALL be removed from the chip list and become available again in the typeahead

#### Scenario: Typeahead excludes selected chips
- **WHEN** "Doe, Jane" is already selected as a chip
- **THEN** the Person B typeahead SHALL NOT include "Doe, Jane" in its dropdown options

### Requirement: Multi-person selection for org-person relationship creation
The org-person create form SHALL replace the single Person TypeaheadSelect with a multi-person chip selector, using the same `onSelect` callback pattern as the person-person form. The typeahead SHALL exclude people already selected as chips and people already linked to the selected organization.

#### Scenario: Select multiple people for an organization
- **WHEN** the user selects "Doe, Jane" then "Brown, Alice" from the Person typeahead in the org panel
- **THEN** both SHALL appear as removable chips

#### Scenario: Typeahead excludes chips and existing org members
- **WHEN** "Acme Corp" is selected, "Green, Tom" is already linked to Acme, and "Doe, Jane" is selected as a chip
- **THEN** the Person typeahead SHALL NOT include "Green, Tom" or "Doe, Jane"

### Requirement: Batch submission creates one relationship per selected person
On form submission, the system SHALL create one relationship per selected person chip. All relationships SHALL share the same notes text. The submit button text SHALL reflect the number of selected people (e.g., "+ Add 3 Relationships"). The submit button SHALL be disabled when no people are selected as chips.

#### Scenario: Submit creates multiple relationships
- **WHEN** Person A is "Smith, John", chips are "Doe, Jane" and "Brown, Alice", notes are "met at retreat", and the user submits
- **THEN** the system SHALL create two relationships: John ↔ Jane and John ↔ Alice, both with notes "met at retreat"

#### Scenario: Submit button shows count
- **WHEN** 3 people are selected as chips
- **THEN** the submit button SHALL display "+ Add 3 Relationships"

#### Scenario: Submit button disabled with no chips
- **WHEN** no people are selected as chips
- **THEN** the submit button SHALL be disabled

#### Scenario: Successful batch clears form
- **WHEN** all relationships in a batch are created successfully
- **THEN** Person A, all chips, and notes SHALL clear

### Requirement: Partial failure handling for batch submission
When some relationships in a batch fail to create, the system SHALL remove chips for successful creates and keep chips for failed creates. Person A and notes SHALL persist as long as any chip remains. A toast error SHALL be shown for each failure.

#### Scenario: Partial failure preserves failed chips
- **WHEN** John ↔ Jane succeeds but John ↔ Alice fails
- **THEN** Jane's chip SHALL be removed, Alice's chip SHALL remain, and a toast error SHALL appear for Alice

#### Scenario: Partial failure preserves Person A and notes
- **WHEN** a batch submission has at least one failure
- **THEN** Person A and notes SHALL remain populated so the user can retry

#### Scenario: Submit button disabled during submission
- **WHEN** a batch submission is in progress
- **THEN** the submit button SHALL be disabled to prevent double-submission

### Requirement: Notes lifecycle tied to chip presence
The notes field SHALL clear when all person chips are removed, whether by successful submission or manual removal. Notes SHALL persist as long as at least one chip is selected.

#### Scenario: Notes clear when last chip is removed manually
- **WHEN** the user removes the last remaining person chip
- **THEN** the notes field SHALL clear

#### Scenario: Notes persist with chips present
- **WHEN** one or more person chips are selected and the user edits the notes field
- **THEN** the notes SHALL persist even if individual chips are added or removed

#### Scenario: Notes clear after fully successful submission
- **WHEN** all relationships in a batch are created successfully and all chips are removed
- **THEN** the notes field SHALL clear along with Person A
