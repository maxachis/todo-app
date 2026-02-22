## ADDED Requirements

### Requirement: Network navigation in Svelte UI
The system SHALL provide Svelte routes and navigation entries for People, Organizations, Interactions, Relationships, and Graph.

#### Scenario: Navigate to People view
- **WHEN** a user selects People from the main navigation
- **THEN** the People view loads in the Svelte app without full-page reload

### Requirement: Network list and detail views
The system SHALL provide list and detail views for people, organizations, and interactions in the Svelte UI.

#### Scenario: View person detail
- **WHEN** a user selects a person from the list
- **THEN** the detail panel shows the person data and related interactions

### Requirement: Graph visualization parity
The system SHALL present the network graph in Svelte with equivalent behavior to the existing network app visualization.

#### Scenario: View graph
- **WHEN** a user opens the Graph view
- **THEN** the graph renders with the same data and interactions as the legacy network app
