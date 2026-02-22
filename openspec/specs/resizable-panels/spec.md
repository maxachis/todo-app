### Requirement: Draggable resize handles between panels
The system SHALL render a draggable resize handle between the sidebar and center panel, and another between the center panel and detail panel. The handles SHALL only be active on the Tasks route when the three-panel layout is visible (viewport wider than 1024px).

#### Scenario: Resize handles are visible on desktop Tasks route
- **WHEN** the user is on the Tasks route with a viewport wider than 1024px
- **THEN** a vertical resize handle is rendered between the sidebar and center panel, and another between the center panel and detail panel

#### Scenario: Resize handles are hidden on mobile
- **WHEN** the viewport is narrower than 1024px
- **THEN** no resize handles are rendered

#### Scenario: Resize handles are hidden on non-Tasks routes
- **WHEN** the user navigates to a non-Tasks route (Projects, Timesheet, Import, etc.)
- **THEN** no resize handles are rendered

#### Scenario: Drag left handle resizes sidebar
- **WHEN** the user drags the left resize handle horizontally
- **THEN** the sidebar width increases or decreases to follow the pointer position, and the center panel adjusts to fill remaining space

#### Scenario: Drag right handle resizes detail panel
- **WHEN** the user drags the right resize handle horizontally
- **THEN** the detail panel width increases or decreases to follow the pointer position, and the center panel adjusts to fill remaining space

#### Scenario: Cursor changes on handle hover
- **WHEN** the user hovers over a resize handle
- **THEN** the cursor changes to `col-resize`

#### Scenario: Handle highlights during drag
- **WHEN** the user is actively dragging a resize handle
- **THEN** the handle displays a visible accent-colored indicator line

### Requirement: Panel minimum width constraints
The system SHALL enforce minimum widths during resize so that panels remain usable. The sidebar SHALL have a minimum width of 180px. The detail panel SHALL have a minimum width of 220px. The center panel SHALL have an implicit minimum width of 200px.

#### Scenario: Sidebar cannot shrink below minimum
- **WHEN** the user drags the left handle to shrink the sidebar below 180px
- **THEN** the sidebar width is clamped at 180px and the handle stops moving

#### Scenario: Detail panel cannot shrink below minimum
- **WHEN** the user drags the right handle to shrink the detail panel below 220px
- **THEN** the detail panel width is clamped at 220px and the handle stops moving

#### Scenario: Center panel minimum is enforced
- **WHEN** the user drags either handle such that the center panel would shrink below 200px
- **THEN** the drag is clamped so the center panel remains at least 200px wide

### Requirement: Panel width persistence
The system SHALL persist user-chosen panel widths in localStorage and restore them on page load. Widths SHALL be written to localStorage when a drag operation ends, not during dragging.

#### Scenario: Widths persist across page reloads
- **WHEN** the user resizes panels and reloads the page
- **THEN** the panels restore to the previously set widths

#### Scenario: Default widths used when no saved state exists
- **WHEN** no panel width data exists in localStorage
- **THEN** the sidebar defaults to 300px and the detail panel defaults to 320px

#### Scenario: Saved widths are clamped on smaller viewport
- **WHEN** saved panel widths exceed the available viewport width
- **THEN** the widths are clamped to fit within the viewport while respecting minimum constraints

#### Scenario: Widths are saved on drag end only
- **WHEN** the user is actively dragging a resize handle
- **THEN** localStorage is NOT updated until the drag operation ends (pointerup)
