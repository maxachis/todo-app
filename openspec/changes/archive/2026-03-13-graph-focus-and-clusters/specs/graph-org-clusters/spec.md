## ADDED Requirements

### Requirement: Organization cluster hull visualization
The graph view SHALL draw convex hull overlays around each organization and the people connected to it via org-person relationships. Hulls SHALL render as SVG paths behind all nodes and edges. Hulls SHALL use a low-opacity fill (~10%) with a subtle border (~20% opacity), derived from the organization node's accent color. Hull paths SHALL include padding (~15px) around node positions so the hull visually encompasses nodes rather than passing through their centers.

#### Scenario: Organization with 3+ connected people
- **WHEN** an organization has 3 or more people connected via org-person relationships
- **THEN** a convex hull SHALL be drawn encompassing the organization node and all connected people nodes

#### Scenario: Organization with fewer than 3 connected people
- **WHEN** an organization has fewer than 3 people connected (0, 1, or 2 people — so fewer than 3 total points including the org, or collinear points)
- **THEN** no hull SHALL be drawn for that organization

#### Scenario: Person in multiple organizations
- **WHEN** a person has org-person relationships with multiple organizations
- **THEN** the person's node SHALL appear inside multiple overlapping hulls

#### Scenario: Unaffiliated people
- **WHEN** a person has no org-person relationships (only person-person connections or isolated)
- **THEN** the person SHALL not be enclosed in any hull

#### Scenario: Hull positions update during simulation
- **WHEN** the force simulation is running or a node is being dragged
- **THEN** hull paths SHALL recompute and update on each simulation tick to follow node movement

### Requirement: Cluster hull visibility toggle
The graph view SHALL provide a "Show org clusters" checkbox in the Filters card to toggle hull visibility. The checkbox SHALL default to checked (hulls visible).

#### Scenario: Toggle hulls off
- **WHEN** the user unchecks "Show org clusters"
- **THEN** all hull overlays SHALL be hidden

#### Scenario: Toggle hulls on
- **WHEN** the user checks "Show org clusters"
- **THEN** all hull overlays SHALL be displayed

### Requirement: Cluster hulls interact with focus mode
When focus mode is active, hull overlays SHALL fade along with their constituent nodes. A hull SHALL remain at full opacity only if its organization node is part of the focused neighborhood.

#### Scenario: Hull for focused organization
- **WHEN** focus mode is active and the focused node or a neighbor is an organization with a hull
- **THEN** that hull SHALL remain at full opacity

#### Scenario: Hull for non-focused organization
- **WHEN** focus mode is active and an organization is not in the focused neighborhood
- **THEN** that organization's hull SHALL fade to match the faded opacity (~10%)
