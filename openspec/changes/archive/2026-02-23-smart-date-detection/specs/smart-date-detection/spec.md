## ADDED Requirements

### Requirement: Date expressions in task title are automatically detected
The task creation form SHALL parse the title text for date expressions on each input event using chrono-node. Supported formats SHALL include natural language ("tomorrow", "next friday", "in 3 days"), numeric ("1/15", "01-15-2026", "2026-01-15"), and month names ("jan 15", "January 15th", "feb 3"). When a date is detected, the system SHALL pre-fill the date picker with the parsed date.

#### Scenario: Natural language date detected
- **WHEN** user types "Buy groceries tomorrow" in the task title input
- **THEN** the date picker SHALL be pre-filled with tomorrow's date

#### Scenario: Numeric date detected
- **WHEN** user types "Dentist appointment 3/15" in the task title input
- **THEN** the date picker SHALL be pre-filled with March 15 of the current or next year

#### Scenario: Month name date detected
- **WHEN** user types "Submit report Jan 20" in the task title input
- **THEN** the date picker SHALL be pre-filled with January 20

#### Scenario: No date in title
- **WHEN** user types "Buy groceries" in the task title input with no date expression
- **THEN** the date picker SHALL remain empty

### Requirement: Detection uses a two-state lifecycle
The detection system SHALL use a boolean detecting/not-detecting lifecycle:
- **Detecting (default)**: Chrono parses title text on each input event. Detected dates pre-fill the picker. If the text changes and chrono finds a new date, the picker updates. If chrono finds no date, the current picker value sticks.
- **Not detecting**: User manually interacted with the date picker. Detection stops. No further parsing until form resets.

Form submission SHALL reset the lifecycle to detecting.

#### Scenario: Date detected while detecting
- **WHEN** detection is active and the user types a title containing a date expression
- **THEN** the date picker SHALL be pre-filled with the detected date

#### Scenario: Date updates while detecting
- **WHEN** detection is active with a date already detected, and the user edits the title to contain a different date expression
- **THEN** the picker SHALL update to reflect the new date

#### Scenario: Date phrase removed while detecting
- **WHEN** detection is active with a date already detected, and the user edits the title so it no longer contains a date expression
- **THEN** the picker value SHALL remain unchanged (date sticks)

#### Scenario: Detection stops on manual picker interaction
- **WHEN** the user manually changes the date picker value (not via detection)
- **THEN** detection SHALL stop and the picker SHALL retain the manually selected value

#### Scenario: Form submission resets lifecycle
- **WHEN** a task is submitted
- **THEN** detection SHALL reset to active for the next task entry

### Requirement: Manual date picker interaction overrides detection
When the user manually changes the date picker value (direct interaction, not programmatic pre-fill), detection SHALL stop for the current input session. The picker SHALL retain the manually selected value.

#### Scenario: User manually picks a date while detection is active
- **WHEN** detection is active and the user manually changes the date picker to a value
- **THEN** detection SHALL stop and the picker SHALL retain the manually selected date

#### Scenario: User clears picker after detection
- **WHEN** a date was detected and pre-filled, and the user manually clears the date picker
- **THEN** detection SHALL stop and the picker SHALL remain empty

### Requirement: Title text is preserved as-is
The task title SHALL be stored exactly as typed, including any date expressions. The detection system SHALL NOT modify, strip, or alter the title text.

#### Scenario: Title with date phrase is preserved
- **WHEN** user types "Buy groceries tomorrow" and submits
- **THEN** the created task's title SHALL be "Buy groceries tomorrow" (not "Buy groceries")
