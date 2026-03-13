## ADDED Requirements

### Requirement: Task detail notes use CodeMirror with live preview
The task detail notes field SHALL use a CodeMirror 6 editor with live markdown preview. The editor SHALL render headings, bold, italic, inline code, links, code blocks, blockquotes, lists (with bullet replacement), horizontal rules, and checkboxes inline while editing. Markdown syntax markers SHALL be hidden on non-active lines and revealed when the cursor is on that line.

#### Scenario: User edits notes with live formatting
- **WHEN** the user types `**hello**` in the notes editor
- **AND** the cursor moves to a different line
- **THEN** "hello" appears bold with the `**` markers hidden

#### Scenario: Checkbox interaction
- **WHEN** the user types `- [ ] Buy milk` in the notes editor
- **AND** the cursor is not on that line
- **THEN** a checkbox widget is displayed
- **AND** clicking the checkbox toggles it to `- [x] Buy milk`

#### Scenario: List continuation
- **WHEN** the user presses Enter at the end of a list item line
- **THEN** a new list item with the same marker is inserted on the next line

### Requirement: Notes editor saves on blur
The notes editor SHALL call the `onSave` callback with the current content when the editor loses focus (focusout event). This integrates with the existing task detail auto-save mechanism.

#### Scenario: Click outside notes area
- **WHEN** the user is editing notes in the CodeMirror editor
- **AND** the user clicks outside the editor area
- **THEN** the editor's `onSave` callback is invoked with the current content
- **AND** the editor remains in its live-preview state (no mode switch needed)

### Requirement: Notes editor syncs with external value changes
The notes editor SHALL update its content when the `value` prop changes externally (e.g., when switching to a different task). The editor SHALL not trigger `onSave` during external content updates.

#### Scenario: User selects a different task
- **WHEN** the selected task changes
- **THEN** the editor content updates to reflect the new task's notes
- **AND** `onSave` is not called
