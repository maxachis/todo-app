## MODIFIED Requirements

### Requirement: Graph visualization parity
The system SHALL present the network graph in Svelte with equivalent behavior to the existing network app visualization. Graph node, edge, and label colors SHALL be derived from the app's CSS variable theme system rather than hardcoded hex values. Organization nodes SHALL use the `--accent` color. Person nodes SHALL use the `--text-tertiary` color. Edge lines SHALL use per-relationship-type custom colors when assigned, falling back to the `--border` color for edges without a custom color or without a relationship type. Edge note labels SHALL use the `--text-tertiary` color. Node text labels SHALL use the `--text-primary` color. Graph colors SHALL update automatically when the user toggles between light and dark themes; edges with custom colors SHALL retain their assigned colors during theme changes.

#### Scenario: View graph
- **WHEN** a user opens the Graph view
- **THEN** the graph renders with the same data and interactions as the legacy network app

#### Scenario: Graph node colors match theme
- **WHEN** the graph renders in the current theme
- **THEN** organization nodes SHALL use the `--accent` color and person nodes SHALL use the `--text-tertiary` color

#### Scenario: Graph edge colors use per-type custom colors
- **WHEN** the graph renders and relationship types have custom colors assigned
- **THEN** edge lines for those types SHALL use the assigned custom color instead of `--border`

#### Scenario: Graph edge colors fall back to theme default
- **WHEN** the graph renders and an edge has no custom color assigned (or no relationship type)
- **THEN** the edge line SHALL use the `--border` color

#### Scenario: Graph label colors match theme
- **WHEN** the graph renders in the current theme
- **THEN** node text labels SHALL use the `--text-primary` color

#### Scenario: Graph colors update on theme toggle
- **WHEN** the user switches between light and dark mode while viewing the graph
- **THEN** all graph node and label colors SHALL update to reflect the new theme's CSS variable values without losing the current graph layout or zoom state, while edges with custom colors SHALL retain their assigned colors
