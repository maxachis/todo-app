## MODIFIED Requirements

### Requirement: Midpoint-based drop determines reorder vs nest
The system SHALL use cursor position relative to the drop target task row's vertical midpoint to determine drop behavior. Dropping above the midpoint SHALL reorder (insert before the target at the target's hierarchy level). Dropping below the midpoint SHALL nest (make the dragged task a subtask of the target). On touch devices, the drag interaction SHALL only begin after the touch-hold delay (defined in the `mobile-touch-hold-drag` capability) has elapsed, after which the existing midpoint-based detection SHALL apply unchanged.

#### Scenario: Drop above midpoint reorders task before target
- **WHEN** the user drags Task A and drops it above the vertical midpoint of Task B
- **THEN** Task A SHALL be placed immediately before Task B at Task B's current hierarchy level (same parent_id as Task B)
- **AND** Task A's position SHALL be set to Task B's sibling index

#### Scenario: Drop below midpoint nests task under target
- **WHEN** the user drags Task A and drops it below the vertical midpoint of Task B
- **THEN** Task A SHALL become a subtask of Task B (parent_id set to Task B's id)
- **AND** Task A SHALL be inserted at position 0 within Task B's subtasks

#### Scenario: Nesting works at any depth
- **WHEN** the user drags Task A and drops it below the midpoint of a subtask (Task C, which is already a child of Task B)
- **THEN** Task A SHALL become a subtask of Task C (a sub-subtask of Task B)
- **AND** Task A SHALL inherit Task C's section_id

#### Scenario: Reorder works at any depth
- **WHEN** the user drags a subtask and drops it above the midpoint of a sibling subtask
- **THEN** the subtask SHALL be repositioned before the sibling within the same parent, preserving its nesting level

#### Scenario: Touch device drag uses hold-then-midpoint detection
- **WHEN** the user touches and holds a task for at least 200ms on a touch device, then drags it over another task
- **THEN** the midpoint-based reorder vs nest detection SHALL apply identically to mouse-based drag
