### Requirement: Enter key submits interaction create form
The interaction create form's notes textarea SHALL submit the form when the user presses the Enter key without any modifier keys held.

#### Scenario: Enter key submits form with valid data
- **WHEN** the user has filled in Person, Interaction type, and Date fields, and presses Enter in the notes textarea
- **THEN** the form SHALL be submitted and the new interaction SHALL appear in the list

#### Scenario: Enter key with empty required fields
- **WHEN** the user presses Enter in the notes textarea but required fields (Person, Interaction type, or Date) are not filled
- **THEN** the form SHALL not submit and no interaction SHALL be created

#### Scenario: Enter key clears form after submission
- **WHEN** the user presses Enter in the notes textarea and the form submits successfully
- **THEN** all form fields (Person, Interaction type, Date, Notes) SHALL be reset to empty/default values

### Requirement: Shift+Enter inserts newline in notes
The notes textarea SHALL allow multi-line input via the Shift+Enter key combination.

#### Scenario: Shift+Enter inserts a newline
- **WHEN** the user presses Shift+Enter in the notes textarea
- **THEN** a newline character SHALL be inserted into the notes text and the form SHALL NOT be submitted

### Requirement: Enter-to-submit scoped to create form only
The Enter-to-submit behavior SHALL apply only to the interaction create form's notes textarea, not to the edit/detail form in the right panel.

#### Scenario: Edit form notes textarea allows normal Enter
- **WHEN** the user presses Enter in the edit/detail panel's notes textarea
- **THEN** a newline character SHALL be inserted and no form submission SHALL occur
