## ADDED Requirements

### Requirement: Pinned task rows display a completion checkbox
Each pinned task row in the PinnedSection on the Tasks page SHALL display an unchecked checkbox to the left of the task title.

#### Scenario: Checkbox is visible on pinned task rows
- **WHEN** the Tasks page displays pinned tasks in the PinnedSection
- **THEN** each pinned task row SHALL display an unchecked checkbox before the task title

### Requirement: Clicking the checkbox completes the pinned task
Clicking the checkbox on a pinned task row SHALL mark the task as completed via the API and remove it from the pinned section.

#### Scenario: Complete a non-recurring pinned task
- **WHEN** user clicks the checkbox on a non-recurring pinned task
- **THEN** the task SHALL be marked as completed via the API
- **THEN** the task SHALL be removed from the pinned section

#### Scenario: Complete a recurring pinned task
- **WHEN** user clicks the checkbox on a recurring pinned task
- **THEN** the task SHALL be marked as completed via the API
- **THEN** the completed task SHALL be removed from the pinned section
- **THEN** a next-occurrence toast SHALL appear (existing recurrence behavior)

#### Scenario: API failure on completion
- **WHEN** user clicks the checkbox and the API call fails
- **THEN** the task SHALL remain visible in the pinned section

### Requirement: Checkbox click does not trigger jump-to-task navigation
Clicking the checkbox area SHALL NOT trigger the jump-to-task scroll and selection behavior. Only clicking the task title or other row content SHALL jump to the task.

#### Scenario: Click checkbox without jumping
- **WHEN** user clicks the checkbox on a pinned task row
- **THEN** the browser SHALL NOT scroll to the task in its section
- **THEN** the task SHALL NOT be selected in the task detail panel
- **THEN** the task SHALL be completed as described above
