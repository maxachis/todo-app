## MODIFIED Requirements

### Requirement: Person detail view includes notebook mentions
The person detail view SHALL include a collapsible "Notebook Mentions" section showing pages that mention this person. The section SHALL fetch data from `GET /api/notebook/mentions/person/{id}/` and display each entry as a clickable row with page title, type badge (daily/wiki), and content snippet. The section SHALL be hidden when there are no mentions.

#### Scenario: Person with notebook mentions
- **WHEN** the user views a person who is mentioned in 3 notebook pages
- **THEN** a "Notebook Mentions" section displays with 3 entries showing page title and snippet

#### Scenario: Person with no notebook mentions
- **WHEN** the user views a person with no notebook mentions
- **THEN** the "Notebook Mentions" section is not displayed

#### Scenario: Click mention navigates to notebook page
- **WHEN** the user clicks a mention entry in the person detail view
- **THEN** the app navigates to `/notebook/{slug}`

### Requirement: Organization detail view includes notebook mentions
The organization detail view SHALL include a collapsible "Notebook Mentions" section with the same behavior as the person detail view, fetching from `GET /api/notebook/mentions/organization/{id}/`.

#### Scenario: Organization with notebook mentions
- **WHEN** the user views an organization mentioned in notebook pages
- **THEN** a "Notebook Mentions" section displays with clickable entries

#### Scenario: Organization with no notebook mentions
- **WHEN** the user views an organization with no notebook mentions
- **THEN** the "Notebook Mentions" section is not displayed
