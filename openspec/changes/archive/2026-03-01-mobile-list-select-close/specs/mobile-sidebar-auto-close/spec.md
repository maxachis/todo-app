## ADDED Requirements

### Requirement: Sidebar closes on list selection (mobile)
When a user selects a list on a mobile viewport, the sidebar overlay SHALL close automatically so that the center panel with the selected list's tasks is immediately visible.

#### Scenario: Selecting a list closes sidebar on mobile
- **WHEN** the user taps a list item in the sidebar overlay on a mobile viewport (≤1023px)
- **THEN** the sidebar overlay closes and the center panel displays the selected list's tasks

#### Scenario: Selecting a list on desktop has no visible effect on sidebar
- **WHEN** the user clicks a list item on a desktop viewport (>1023px)
- **THEN** the sidebar remains visible as part of the three-panel grid layout (no change in behavior)

#### Scenario: Creating a new list closes sidebar on mobile
- **WHEN** the user creates a new list via the sidebar form on a mobile viewport
- **THEN** the sidebar overlay closes and the center panel displays the new list's tasks
