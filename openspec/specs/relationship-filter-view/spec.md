

### Requirement: Filter person-person relationships by person
The Relationships page Person ↔ Person panel SHALL include a filter control between the create form and the relationship list. The filter SHALL be a TypeaheadSelect populated with all people. When a person is selected in the filter, the relationship list SHALL show only relationships involving that person. When the filter is cleared, the list SHALL show all person-person relationships.

#### Scenario: Filter relationships by selecting a person
- **WHEN** the user selects "Smith, John" in the person-person filter control
- **THEN** the relationship list SHALL show only relationships where Smith, John is person_1 or person_2

#### Scenario: Clear filter shows all relationships
- **WHEN** the user clears the person-person filter (via the × button)
- **THEN** the relationship list SHALL show all person-person relationships

#### Scenario: No matching relationships
- **WHEN** the user selects a person in the filter who has no relationships
- **THEN** the relationship list SHALL be empty

### Requirement: Filter org-person relationships by organization
The Relationships page Organization → Person panel SHALL include a filter control between the create form and the relationship list. The filter SHALL be a TypeaheadSelect populated with all organizations. When an organization is selected in the filter, the relationship list SHALL show only relationships involving that organization. When the filter is cleared, the list SHALL show all org-person relationships.

#### Scenario: Filter relationships by selecting an organization
- **WHEN** the user selects "Acme Corp" in the org-person filter control
- **THEN** the relationship list SHALL show only relationships where the organization is Acme Corp

#### Scenario: Clear filter shows all org relationships
- **WHEN** the user clears the org-person filter (via the × button)
- **THEN** the relationship list SHALL show all org-person relationships

### Requirement: Auto-sync filter from Person A selection
When the user selects a person in the Person A field of the person-person create form, the filter control SHALL automatically update to show that person's existing relationships. When Person A is cleared (including after form submission), the filter SHALL clear as well. Changing the filter independently SHALL NOT affect the Person A form field.

#### Scenario: Selecting Person A auto-sets filter
- **WHEN** the user selects "Smith, John" as Person A in the create form
- **THEN** the filter control SHALL automatically set to "Smith, John" and the list SHALL show only Smith's relationships

#### Scenario: Clearing Person A clears the filter
- **WHEN** the user clears the Person A field in the create form
- **THEN** the filter SHALL clear and the list SHALL show all relationships

#### Scenario: Submitting the form clears the filter
- **WHEN** the user submits the person-person create form (which clears Person A)
- **THEN** the filter SHALL clear and the list SHALL show all relationships

#### Scenario: Changing filter does not affect Person A
- **WHEN** the user manually changes the filter to a different person
- **THEN** the Person A field in the create form SHALL remain unchanged

### Requirement: Auto-sync filter from Organization selection
When the user selects an organization in the Organization field of the org-person create form, the filter control SHALL automatically update to show that organization's existing relationships. When the Organization field is cleared (including after form submission), the filter SHALL clear as well. Changing the filter independently SHALL NOT affect the Organization form field.

#### Scenario: Selecting Organization auto-sets filter
- **WHEN** the user selects "Acme Corp" as the Organization in the create form
- **THEN** the filter control SHALL automatically set to "Acme Corp" and the list SHALL show only Acme Corp's relationships

#### Scenario: Clearing Organization clears the filter
- **WHEN** the user clears the Organization field in the create form
- **THEN** the filter SHALL clear and the list SHALL show all org-person relationships

#### Scenario: Submitting the org form clears the filter
- **WHEN** the user submits the org-person create form (which clears the Organization field)
- **THEN** the filter SHALL clear and the list SHALL show all org-person relationships

### Requirement: Exclude existing connections from Person B dropdown
When Person A is selected in the person-person create form, the Person B TypeaheadSelect SHALL exclude people who already have a relationship with Person A. Person A themselves SHALL also be excluded from the Person B options.

#### Scenario: Person B excludes already-connected people
- **WHEN** "Smith, John" is selected as Person A and Smith already has relationships with "Doe, Jane" and "Brown, Alice"
- **THEN** the Person B dropdown SHALL NOT include Smith, John, Doe, Jane, or Brown, Alice

#### Scenario: Person B shows all when Person A is not selected
- **WHEN** no person is selected as Person A
- **THEN** the Person B dropdown SHALL show all people

#### Scenario: Person B updates after new relationship is created
- **WHEN** the user creates a new relationship between Smith and Garcia
- **THEN** Garcia SHALL no longer appear in the Person B dropdown while Smith is Person A

### Requirement: Exclude existing connections from org-person Person dropdown
When an Organization is selected in the org-person create form, the Person TypeaheadSelect SHALL exclude people who already have a relationship with that organization.

#### Scenario: Person dropdown excludes already-linked people
- **WHEN** "Acme Corp" is selected as the Organization and Acme already has relationships with "Doe, Jane"
- **THEN** the Person dropdown SHALL NOT include Doe, Jane

#### Scenario: Person dropdown shows all when no organization is selected
- **WHEN** no organization is selected
- **THEN** the Person dropdown SHALL show all people

#### Scenario: Person dropdown updates after new org-person relationship is created
- **WHEN** the user creates a new relationship between Acme and Garcia
- **THEN** Garcia SHALL no longer appear in the Person dropdown while Acme is selected
