## MODIFIED Requirements

### Requirement: Graph visualization parity
The system SHALL present the network graph in Svelte with equivalent behavior to the existing network app visualization. Graph node, edge, and label colors SHALL be derived from the app's CSS variable theme system rather than hardcoded hex values. Organization nodes SHALL use the `--accent` color. Person nodes SHALL use the `--text-tertiary` color. Edge lines SHALL use the `--border` color. Edge note labels SHALL use the `--text-tertiary` color. Node text labels SHALL use the `--text-primary` color. Graph colors SHALL update automatically when the user toggles between light and dark themes. The graph controls panel SHALL include a "Scale nodes by connections" checkbox that, when enabled, scales node radii proportionally to each node's connection count computed from visible edges.

#### Scenario: View graph
- **WHEN** a user opens the Graph view
- **THEN** the graph renders with the same data and interactions as the legacy network app

#### Scenario: Graph node colors match theme
- **WHEN** the graph renders in the current theme
- **THEN** organization nodes SHALL use the `--accent` color and person nodes SHALL use the `--text-tertiary` color

#### Scenario: Graph edge colors match theme
- **WHEN** the graph renders in the current theme
- **THEN** edge lines SHALL use the `--border` color and edge note labels SHALL use the `--text-tertiary` color

#### Scenario: Graph label colors match theme
- **WHEN** the graph renders in the current theme
- **THEN** node text labels SHALL use the `--text-primary` color

#### Scenario: Graph colors update on theme toggle
- **WHEN** the user switches between light and dark mode while viewing the graph
- **THEN** all graph node, edge, and label colors SHALL update to reflect the new theme's CSS variable values without losing the current graph layout or zoom state

#### Scenario: Graph includes node sizing toggle
- **WHEN** a user opens the Graph view
- **THEN** the Filters card includes a "Scale nodes by connections" checkbox that controls connection-weighted node sizing
