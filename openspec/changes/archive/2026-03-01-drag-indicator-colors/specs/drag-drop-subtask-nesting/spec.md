## MODIFIED Requirements

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
