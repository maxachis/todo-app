## ADDED Requirements

### Requirement: Validation toast on missing required fields

When a user submits a create form with one or more required fields empty, the system SHALL display an error toast listing the missing fields instead of silently aborting.

#### Scenario: Single missing field on person create

- **WHEN** the user submits the create-person form with first name filled but last name empty
- **THEN** the system SHALL display an error toast with message "Required: Last name"
- **AND** the form SHALL NOT be submitted to the API

#### Scenario: Multiple missing fields on person create

- **WHEN** the user submits the create-person form with both first name and last name empty
- **THEN** the system SHALL display an error toast with message "Required: First name, Last name"
- **AND** the form SHALL NOT be submitted to the API

#### Scenario: Missing dropdown selection on organization create

- **WHEN** the user submits the create-organization form with name filled but no org type selected
- **THEN** the system SHALL display an error toast with message "Required: Organization type"

#### Scenario: Missing people on interaction create

- **WHEN** the user submits the create-interaction form with no people selected
- **THEN** the system SHALL display an error toast listing "People" as a required field

#### Scenario: All required fields filled

- **WHEN** the user submits any create form with all required fields filled
- **THEN** the system SHALL proceed with the API call as normal and SHALL NOT display a validation toast

### Requirement: Shared validation helper

The system SHALL provide a reusable `validateRequired` function that accepts a record of field labels to values and returns a boolean indicating validity.

#### Scenario: Helper returns false for missing fields

- **WHEN** `validateRequired` is called with `{ 'Name': '' }`
- **THEN** it SHALL return `false` and call `addToast` with type `error`

#### Scenario: Helper returns true for complete fields

- **WHEN** `validateRequired` is called with `{ 'Name': 'Alice' }`
- **THEN** it SHALL return `true` and SHALL NOT call `addToast`

#### Scenario: Helper handles null and empty arrays

- **WHEN** `validateRequired` is called with `{ 'Project': null, 'People': [] }`
- **THEN** it SHALL return `false` with a toast message listing both "Project" and "People"

### Requirement: All create forms use validation feedback

Every create-form submit handler in the application SHALL use the shared validation helper to provide toast feedback for missing required fields. The covered forms are:

- Create person (required: first name, last name)
- Create organization (required: name, organization type)
- Create interaction (required: people, type, date)
- Create lead (required: title, person or organization)
- Create person-person relationship (required: person A, person B)
- Create org-person relationship (required: organization, people)
- Create project (required: name)
- Add project link (required: label, URL)
- Create time entry (required: project)
- Create task (required: title)
- Create list (required: name)
- Quick-log interaction on person (required: type, date)

#### Scenario: Consistent feedback across all forms

- **WHEN** any of the listed create forms is submitted with missing required fields
- **THEN** the system SHALL display an error toast with the same "Required: field1, field2" format

#### Scenario: Toast auto-dismisses

- **WHEN** a validation error toast is displayed
- **THEN** it SHALL auto-dismiss after the default timeout (5 seconds)
