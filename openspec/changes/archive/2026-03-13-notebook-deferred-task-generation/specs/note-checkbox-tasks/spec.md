## MODIFIED Requirements

### Requirement: Checkbox syntax creates tasks in Inbox on save
The system SHALL detect lines matching the pattern `- [ ] <text>` in notebook page content during the save flow (within `reconcile_mentions`). For each matching line where `<text>` does NOT already contain `[[task:`, the system SHALL create a new task in the Inbox list's section with the extracted text as the title. After creation, the system SHALL rewrite the line in the page content to `- [ ] [[task:ID|Title]]`, where ID is the newly created task's ID and Title is the task title.

The page update API SHALL accept an optional `process_checkboxes` parameter (default `true`). When `false`, the save SHALL persist content and reconcile mentions/links but SHALL NOT run checkbox-to-task creation or content rewriting. The frontend SHALL pass `process_checkboxes: false` on debounced auto-saves during typing, and `process_checkboxes: true` on blur saves and when the user presses Enter after a checkbox line.

#### Scenario: Single checkbox creates a task
- **WHEN** a page is saved with content containing `- [ ] Call the dentist` and `process_checkboxes` is `true`
- **THEN** a task titled "Call the dentist" is created in the Inbox section, and the content is rewritten to `- [ ] [[task:42|Call the dentist]]`

#### Scenario: Multiple checkboxes create multiple tasks
- **WHEN** a page is saved with content containing two lines: `- [ ] Buy milk` and `- [ ] Send invoice` and `process_checkboxes` is `true`
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
- **WHEN** a page is saved with `- [ ] New task` and `process_checkboxes` is `true`
- **THEN** the task is created, content is rewritten with the link, and the subsequent mention reconciliation detects the `[[task:ID|...]]` pattern and creates the corresponding `PageEntityMention` record

#### Scenario: Debounced save skips task generation
- **WHEN** a page is saved with `process_checkboxes: false` and content contains `- [ ] New task`
- **THEN** the content is persisted as-is, no task is created, and no content rewriting occurs

#### Scenario: Blur save triggers task generation
- **WHEN** the user blurs the editor and the page is saved with `process_checkboxes: true`
- **THEN** all unlinked checkbox lines have tasks created and content is rewritten

#### Scenario: Enter after checkbox line triggers task generation
- **WHEN** the user presses Enter while the cursor is on a line matching `- [ ] <text>` (without `[[task:`)
- **THEN** an immediate save with `process_checkboxes: true` is triggered, creating the task for that line
