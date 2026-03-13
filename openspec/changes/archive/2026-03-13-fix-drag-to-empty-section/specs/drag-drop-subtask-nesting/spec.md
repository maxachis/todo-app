## MODIFIED Requirements

### Requirement: Tasks can be dragged between sections
The dndzone container for each section SHALL have sufficient minimum height to act as a valid drop target even when the section contains no tasks.

#### Scenario: Drop task into empty section
- **WHEN** a user drags a task from a section with tasks
- **AND** drops it onto a section that has no tasks
- **THEN** the task SHALL be moved into the empty section via the API
- **THEN** the task SHALL appear in the target section
