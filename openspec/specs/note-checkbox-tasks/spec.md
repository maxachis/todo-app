# Note Checkbox Tasks

## Purpose

Automatic task creation from checkbox syntax in notebook pages, enabling quick task capture from notes with one-directional linking back to the Inbox.

## Requirements

### Requirement: Checkbox syntax creates tasks in Inbox on save
The system SHALL detect lines matching the pattern `- [ ] <text>` in notebook page content during the save flow (within `reconcile_mentions`). For each matching line where `<text>` does NOT already contain `[[task:`, the system SHALL create a new task in the Inbox list's section with the extracted text as the title. After creation, the system SHALL rewrite the line in the page content to `- [ ] [[task:ID|Title]]`, where ID is the newly created task's ID and Title is the task title.

#### Scenario: Single checkbox creates a task
- **WHEN** a page is saved with content containing `- [ ] Call the dentist`
- **THEN** a task titled "Call the dentist" is created in the Inbox section, and the content is rewritten to `- [ ] [[task:42|Call the dentist]]`

#### Scenario: Multiple checkboxes create multiple tasks
- **WHEN** a page is saved with content containing two lines: `- [ ] Buy milk` and `- [ ] Send invoice`
- **THEN** two tasks are created in the Inbox section, and both lines are rewritten with their respective task links

#### Scenario: Already-linked checkbox is skipped
- **WHEN** a page is saved with content containing `- [ ] [[task:42|Call the dentist]]`
- **THEN** no new task is created for that line (the existing link is preserved)

#### Scenario: Checked checkbox is skipped
- **WHEN** a page is saved with content containing `- [x] Done item`
- **THEN** no task is created (only unchecked `- [ ]` triggers creation)

#### Scenario: Checkbox without text is skipped
- **WHEN** a page is saved with content containing `- [ ] ` (trailing space, no text)
- **THEN** no task is created

#### Scenario: Task creation and mention reconciliation are atomic
- **WHEN** a page is saved with `- [ ] New task`
- **THEN** the task is created, content is rewritten with the link, and the subsequent mention reconciliation detects the `[[task:ID|...]]` pattern and creates the corresponding `PageEntityMention` record

### Requirement: One-directional task creation
Task creation from checkbox syntax SHALL be one-directional. Checking or unchecking a checkbox in the note (`- [x]` / `- [ ]`) SHALL NOT affect the task's completion status. Completing or uncompleting a task in the task system SHALL NOT modify the note content. The `[[task:ID|Title]]` link serves only as a reference.

#### Scenario: Checking checkbox in note does not complete task
- **WHEN** a user changes `- [ ] [[task:42|Call the dentist]]` to `- [x] [[task:42|Call the dentist]]` in a note and saves
- **THEN** task 42 remains incomplete in the task system

#### Scenario: Completing task does not update note
- **WHEN** a user completes task 42 in the task system
- **THEN** any notebook page containing `[[task:42|Call the dentist]]` is not modified
