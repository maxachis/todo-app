### Requirement: Enter key submits person-person relationship create form
The person-person relationship create form's notes textarea SHALL submit the form when the user presses the Enter key without any modifier keys held, provided both Person A and Person B are selected.

#### Scenario: Enter key submits form with valid selections
- **WHEN** the user has selected both Person A and Person B, and presses Enter in the notes textarea
- **THEN** the form SHALL be submitted and the new relationship SHALL appear in the list

#### Scenario: Enter key does nothing when required fields are empty
- **WHEN** the user presses Enter in the notes textarea but Person A or Person B is not selected
- **THEN** the form SHALL NOT submit and no relationship SHALL be created

#### Scenario: Enter key clears form after submission
- **WHEN** the user presses Enter in the notes textarea and the form submits successfully
- **THEN** all form fields (Person A, Person B, Notes) SHALL be reset to empty/default values

### Requirement: Enter key submits org-person relationship create form
The org-person relationship create form's notes textarea SHALL submit the form when the user presses the Enter key without any modifier keys held, provided both Organization and Person are selected.

#### Scenario: Enter key submits form with valid selections
- **WHEN** the user has selected both Organization and Person, and presses Enter in the notes textarea
- **THEN** the form SHALL be submitted and the new relationship SHALL appear in the list

#### Scenario: Enter key does nothing when required fields are empty
- **WHEN** the user presses Enter in the notes textarea but Organization or Person is not selected
- **THEN** the form SHALL NOT submit and no relationship SHALL be created

#### Scenario: Enter key clears form after submission
- **WHEN** the user presses Enter in the notes textarea and the form submits successfully
- **THEN** all form fields (Organization, Person, Notes) SHALL be reset to empty/default values

### Requirement: Shift+Enter inserts newline in notes
The notes textarea in both relationship create forms SHALL allow multi-line input via the Shift+Enter key combination.

#### Scenario: Shift+Enter inserts a newline in person-person form
- **WHEN** the user presses Shift+Enter in the person-person notes textarea
- **THEN** a newline character SHALL be inserted into the notes text and the form SHALL NOT be submitted

#### Scenario: Shift+Enter inserts a newline in org-person form
- **WHEN** the user presses Shift+Enter in the org-person notes textarea
- **THEN** a newline character SHALL be inserted into the notes text and the form SHALL NOT be submitted

### Requirement: Enter-to-submit scoped to create forms only
The Enter-to-submit behavior SHALL apply only to the relationship create forms' notes textareas, not to any edit/detail UI for existing relationships.

#### Scenario: Edit notes textarea allows normal Enter
- **WHEN** the user presses Enter in an existing relationship's notes edit field
- **THEN** a newline character SHALL be inserted and no form submission SHALL occur
