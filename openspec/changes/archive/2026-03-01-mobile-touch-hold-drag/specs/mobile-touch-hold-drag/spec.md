## ADDED Requirements

### Requirement: Touch-hold delay before drag activation on touch devices
The system SHALL require a sustained touch of at least 200 milliseconds before initiating a drag-and-drop operation on touch/mobile devices. Touch interactions shorter than 200ms SHALL be ignored by the drag system, allowing normal scrolling and tapping to proceed.

#### Scenario: Short tap does not start drag
- **WHEN** the user touches a task row on a touch device and lifts their finger within 200ms
- **THEN** the drag operation SHALL NOT be initiated
- **AND** the tap or scroll gesture SHALL proceed normally

#### Scenario: Touch-and-hold activates drag after delay
- **WHEN** the user touches a task row on a touch device and maintains contact for at least 200ms
- **THEN** the drag operation SHALL activate, allowing the user to move the item

#### Scenario: Scroll gesture during hold period cancels drag
- **WHEN** the user touches a task row and moves their finger (scrolling) before the 200ms hold period elapses
- **THEN** the drag operation SHALL NOT be initiated
- **AND** the scroll gesture SHALL proceed normally

### Requirement: Desktop mouse drag remains immediate
The system SHALL NOT apply any touch-hold delay to mouse-based drag interactions. Mouse drag SHALL continue to initiate immediately on mousedown, preserving the existing desktop experience.

#### Scenario: Mouse drag starts immediately
- **WHEN** the user clicks and drags a task row with a mouse on a desktop device
- **THEN** the drag operation SHALL begin immediately without any delay

### Requirement: Touch-hold delay applies to all DnD zones
The touch-hold delay SHALL apply uniformly to all drag-and-drop zones in the application: task lists, subtask trees, pinned sections, section lists, and the list sidebar.

#### Scenario: Task list drag requires touch-hold
- **WHEN** the user touches a task in the main task list on a touch device
- **THEN** the 200ms touch-hold requirement SHALL apply before drag activates

#### Scenario: List sidebar drag requires touch-hold
- **WHEN** the user touches a list item in the sidebar on a touch device
- **THEN** the 200ms touch-hold requirement SHALL apply before drag activates

#### Scenario: Section drag requires touch-hold
- **WHEN** the user touches a section drag handle on a touch device
- **THEN** the 200ms touch-hold requirement SHALL apply before drag activates
