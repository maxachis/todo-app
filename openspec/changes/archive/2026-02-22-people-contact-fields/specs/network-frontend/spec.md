## ADDED Requirements

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
