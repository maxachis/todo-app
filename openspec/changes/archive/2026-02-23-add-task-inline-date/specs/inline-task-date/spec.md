## ADDED Requirements

### Requirement: Task creation form includes optional due date input
The task creation form SHALL include an optional date input field positioned between the title text input and the submit button. The date field SHALL use a native HTML date input (`<input type="date">`). When no date is selected, the form SHALL behave identically to the current title-only creation flow.

#### Scenario: Create task with a due date
- **WHEN** user enters a title and selects a date in the inline date picker, then submits the form
- **THEN** the task is created with the specified due date and appears in the task list with that date set

#### Scenario: Create task without a due date
- **WHEN** user enters a title without selecting a date and submits the form
- **THEN** the task is created with no due date, identical to current behavior

#### Scenario: Form resets after submission
- **WHEN** a task is submitted (with or without a date)
- **THEN** both the title input and the date input SHALL be cleared to their empty/default state

### Requirement: Create task API accepts optional due_date
The `POST /sections/{section_id}/tasks/` endpoint SHALL accept an optional `due_date` field (ISO 8601 date string) in the request payload. When provided, the created task SHALL have its `due_date` field set to the given value. When omitted or null, the task SHALL be created with no due date.

#### Scenario: API creates task with due_date
- **WHEN** a POST request includes `{ "title": "My task", "due_date": "2026-03-01" }`
- **THEN** the response SHALL return status 201 with the task's `due_date` set to `"2026-03-01"`

#### Scenario: API creates task without due_date
- **WHEN** a POST request includes `{ "title": "My task" }` with no `due_date` field
- **THEN** the response SHALL return status 201 with the task's `due_date` set to null

### Requirement: Inline date input is compact and non-intrusive
The date input SHALL be styled to be visually secondary to the title input. The title input SHALL remain the primary element and receive focus when the form is activated. On mobile viewports, the date input SHALL remain usable without causing the form to overflow or wrap awkwardly.

#### Scenario: Title input has focus on form activation
- **WHEN** the task creation form is displayed
- **THEN** the title text input SHALL be the focused element, not the date input

#### Scenario: Form layout on narrow viewport
- **WHEN** the form is rendered on a narrow viewport (mobile)
- **THEN** all three elements (title, date, submit button) SHALL remain accessible without horizontal overflow
