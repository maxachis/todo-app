## ADDED Requirements

### Requirement: Layout slider values persist across sessions
The system SHALL save graph layout slider values (spacing, repulsion, centering, label size) to localStorage whenever a slider value changes, and SHALL restore saved values when the graph page loads.

#### Scenario: Slider values are saved on change
- **WHEN** the user adjusts any layout slider (spacing, repulsion, centering, or label size)
- **THEN** the current values of all layout sliders are saved to localStorage under the key `graph-layout-settings`

#### Scenario: Slider values are restored on page load
- **WHEN** the graph page loads and localStorage contains saved layout slider values
- **THEN** each slider is initialized to its saved value instead of the hardcoded default

#### Scenario: Default values used when no saved state exists
- **WHEN** the graph page loads and localStorage does not contain saved layout settings
- **THEN** sliders use their default values (spacing: 140, repulsion: 500, centering: 60, label size: 11)

### Requirement: Filter checkbox states persist across sessions
The system SHALL save graph filter checkbox states to localStorage whenever a checkbox is toggled, and SHALL restore saved states when the graph page loads.

#### Scenario: Checkbox states are saved on change
- **WHEN** the user toggles any filter checkbox (People, Organizations, Person-Person, Org-Person, Hide isolated, Show relationship notes, Scale by connections, Show org clusters)
- **THEN** the current states of all filter checkboxes are saved to localStorage under the key `graph-layout-settings`

#### Scenario: Checkbox states are restored on page load
- **WHEN** the graph page loads and localStorage contains saved filter checkbox states
- **THEN** each checkbox is initialized to its saved checked/unchecked state

#### Scenario: Default checkbox states used when no saved state exists
- **WHEN** the graph page loads and localStorage does not contain saved filter states
- **THEN** checkboxes use their default states (People: checked, Organizations: checked, Person-Person: checked, Org-Person: checked, Hide isolated: unchecked, Show relationship notes: unchecked, Scale by connections: unchecked, Show org clusters: checked)

### Requirement: Graceful fallback when localStorage is unavailable
The system SHALL fall back to default values without errors when localStorage is unavailable or contains invalid data.

#### Scenario: localStorage read fails
- **WHEN** the graph page loads and localStorage throws an error on read
- **THEN** all sliders and checkboxes use their default values and no error is shown to the user

#### Scenario: localStorage contains corrupt data
- **WHEN** the graph page loads and the `graph-layout-settings` key contains unparseable JSON
- **THEN** all sliders and checkboxes use their default values and no error is shown to the user
