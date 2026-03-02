# Notebook Collapsible Sidebar

## Purpose

Toggle to collapse/expand the notebook page sidebar, with localStorage persistence and keyboard shortcut, allowing users to maximize editor space.

## Requirements

### Requirement: Sidebar collapse toggle button
The notebook view SHALL display a toggle button that collapses and expands the page sidebar. When the sidebar is expanded, the button SHALL display a left-pointing chevron. When collapsed, a slim vertical strip (~32px wide) SHALL remain visible with a right-pointing chevron button to re-expand the sidebar.

#### Scenario: Collapse the sidebar
- **WHEN** the user clicks the collapse button while the sidebar is expanded
- **THEN** the sidebar collapses to a slim strip with only the expand button, and the editor area expands to fill the available width

#### Scenario: Expand the sidebar
- **WHEN** the user clicks the expand button on the collapsed sidebar strip
- **THEN** the sidebar expands to its full 220px width showing page navigation

#### Scenario: Smooth transition animation
- **WHEN** the sidebar is toggled between collapsed and expanded states
- **THEN** the transition SHALL animate smoothly over approximately 200ms

### Requirement: Sidebar collapse state persists in localStorage
The sidebar collapsed/expanded state SHALL be persisted in localStorage under the key `notebook-sidebar-collapsed`. On page load, the sidebar SHALL initialize to the persisted state. If no persisted state exists, the sidebar SHALL default to expanded.

#### Scenario: State persists across page reloads
- **WHEN** the user collapses the sidebar and reloads the page
- **THEN** the sidebar loads in the collapsed state

#### Scenario: Default state is expanded
- **WHEN** the user visits the notebook for the first time (no localStorage entry)
- **THEN** the sidebar is expanded

### Requirement: Keyboard shortcut to toggle sidebar
The notebook view SHALL support `Cmd+\` (macOS) / `Ctrl+\` (other platforms) as a keyboard shortcut to toggle the sidebar collapsed state. The shortcut SHALL work regardless of focus position within the notebook view.

#### Scenario: Toggle sidebar with keyboard shortcut
- **WHEN** the user presses `Cmd+\` (macOS) or `Ctrl+\` (other platforms) while on the notebook page
- **THEN** the sidebar toggles between collapsed and expanded states

#### Scenario: Shortcut does not fire during text input in other contexts
- **WHEN** the user presses the shortcut while a typeahead dropdown is open
- **THEN** the shortcut SHALL still toggle the sidebar (typeahead does not capture this key combination)
