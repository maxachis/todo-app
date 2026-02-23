## MODIFIED Requirements

### Requirement: Task creation form includes optional due date input
The task creation form SHALL include an optional date input field positioned between the title text input and the submit button. The date field SHALL use a native HTML date input (`<input type="date">`). When no date is selected, the form SHALL behave identically to the current title-only creation flow. The date picker SHALL support being pre-filled programmatically by the smart date detection system.

#### Scenario: Create task with a due date
- **WHEN** user enters a title and selects a date in the inline date picker, then submits the form
- **THEN** the task is created with the specified due date and appears in the task list with that date set

#### Scenario: Create task without a due date
- **WHEN** user enters a title without selecting a date and submits the form
- **THEN** the task is created with no due date, identical to current behavior

#### Scenario: Form resets after submission
- **WHEN** a task is submitted (with or without a date)
- **THEN** both the title input and the date input SHALL be cleared to their empty/default state

#### Scenario: Date picker pre-filled by detection system
- **WHEN** the smart date detection system detects a date in the title text
- **THEN** the date picker value SHALL be set programmatically to the detected date
