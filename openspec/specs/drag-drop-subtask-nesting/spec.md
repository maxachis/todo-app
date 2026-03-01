## Purpose

Defines the drag-and-drop subtask nesting behavior, including midpoint-based drop detection for reorder vs nest, visual feedback during drag, frontend circular nesting prevention, self-drop handling, drag lock during API persistence, and completed task exclusion from drop targets.

## Requirements

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

### Requirement: Visual feedback during drag indicates drop mode
The system SHALL display distinct visual indicators on the drop target task row during drag to show whether the drop will reorder or nest. Drop-zone container outlines SHALL use the app's accent color (`--accent`) instead of the library default bright yellow.

#### Scenario: Before mode shows horizontal line above target
- **WHEN** the user drags a task and the cursor is above the midpoint of the target task row
- **THEN** the target task row SHALL display a horizontal accent-colored line at its top edge

#### Scenario: Nest mode shows left accent bar with background tint
- **WHEN** the user drags a task and the cursor is below the midpoint of the target task row
- **THEN** the target task row SHALL display a left accent bar and a subtle background tint to indicate nesting intent

#### Scenario: Visual feedback clears on drag leave
- **WHEN** the cursor leaves the target task row during drag
- **THEN** all visual indicators (line, accent bar, background tint) SHALL be removed immediately

#### Scenario: Drop-zone outline uses accent color
- **WHEN** a drag-and-drop zone becomes an active drop target (tasks, sections, lists, or pinned tasks)
- **THEN** the zone's outline SHALL be a warm brown derived from the app's accent color (not bright yellow)
- **AND** the outline SHALL be visible in both light and dark themes

### Requirement: Frontend circular nesting prevention
The system SHALL prevent dropping a task onto its own descendant on the frontend, without waiting for a backend error response.

#### Scenario: Drop onto own descendant is silently prevented
- **WHEN** the user drags Task A and drops it below the midpoint of Task C, where Task C is a descendant of Task A
- **THEN** the drop SHALL be silently ignored (no API call, no error toast, no state change)
- **AND** the visual drop indicators SHALL be cleared

#### Scenario: Drop onto non-descendant proceeds normally
- **WHEN** the user drags Task A and drops it below the midpoint of Task B, where Task B is NOT a descendant of Task A
- **THEN** the nest operation SHALL proceed normally

### Requirement: Drag onto self is ignored
The system SHALL ignore drops where the dragged task is dropped onto itself.

#### Scenario: Self-drop is a no-op
- **WHEN** the user drags Task A and drops it onto Task A
- **THEN** no API call SHALL be made and no state SHALL change

### Requirement: Drag lock prevents concurrent drag operations
The system SHALL prevent a new drag operation from starting while a previous drag's API call is in progress.

#### Scenario: Drag disabled during API persistence
- **WHEN** a task drag drop triggers an API call that is still in progress
- **THEN** starting a new drag SHALL be blocked until the previous operation completes

#### Scenario: Drag re-enabled after API completion
- **WHEN** the API call from a drag operation completes (success or failure)
- **THEN** dragging SHALL be re-enabled after a short debounce period

### Requirement: Completed tasks are not drag targets
The system SHALL not accept drops onto completed tasks.

#### Scenario: Dragging over completed task shows no indicators
- **WHEN** the user drags a task over a completed task row
- **THEN** no drop indicators SHALL be displayed and the drop SHALL not be accepted
