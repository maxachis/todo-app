## MODIFIED Requirements

### Requirement: Pin section display
The system SHALL display a "Pinned" section at the top of the list when any tasks are pinned, and provide a pin toggle button on task rows. The pinned section SHALL collect pinned tasks from the entire task tree, including subtasks at any nesting depth — not only top-level tasks. When a pinned subtask appears in the pinned section, it SHALL display with parent context showing the immediate parent task's title as a prefix (e.g. "Parent > Subtask").

#### Scenario: Pinned section displays
- **WHEN** a list has pinned tasks
- **THEN** a "Pinned" section appears at the top showing pinned tasks in compact view

#### Scenario: Pinned section hidden when empty
- **WHEN** no tasks are pinned in the current list
- **THEN** the pinned section is not rendered

#### Scenario: Click pinned task jumps to location
- **WHEN** the user clicks a task in the pinned section
- **THEN** the center panel scrolls to the source task and highlights it briefly

#### Scenario: Pinned order remains stable across source reorders
- **WHEN** pinned tasks are reordered within section/task lists
- **THEN** the pinned section keeps a stable orientation independent of source list position changes

#### Scenario: Reorder pinned tasks inside pinned section
- **WHEN** the user drags pinned tasks within the pinned section
- **THEN** the pinned section order updates to the new arrangement

#### Scenario: Pinned subtask appears in pinned section
- **WHEN** a subtask is pinned and its parent task is not pinned
- **THEN** the subtask SHALL appear in the pinned section

#### Scenario: Pinned subtask shows parent context
- **WHEN** a pinned subtask appears in the pinned section
- **THEN** the pinned entry SHALL display the immediate parent's title as a prefix (e.g. "Parent > Subtask")

#### Scenario: Both parent and subtask pinned
- **WHEN** both a parent task and its subtask are pinned
- **THEN** both SHALL appear as separate entries in the pinned section
- **AND** the subtask entry SHALL show parent context while the parent entry SHALL not

#### Scenario: Deeply nested pinned subtask
- **WHEN** a pinned task is nested two or more levels deep (e.g. grandchild)
- **THEN** only the immediate parent's title SHALL be shown as the prefix, not the full ancestor chain
