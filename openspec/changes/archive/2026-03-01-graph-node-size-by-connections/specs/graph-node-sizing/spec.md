## ADDED Requirements

### Requirement: Toggle for connection-weighted node sizing
The graph controls panel SHALL include a "Scale nodes by connections" checkbox in the Filters card. The checkbox SHALL default to unchecked. When unchecked, nodes SHALL render at their fixed type-based sizes (organization: 9px radius, person: 7px radius).

#### Scenario: Toggle is visible and unchecked by default
- **WHEN** the user navigates to the Graph page
- **THEN** a "Scale nodes by connections" checkbox is displayed in the Filters card, unchecked

#### Scenario: Toggle does not affect default node rendering
- **WHEN** the "Scale nodes by connections" checkbox is unchecked
- **THEN** all nodes render at their fixed type-based radii (9px for organizations, 7px for people)

### Requirement: Node radius scales by connection count when enabled
When "Scale nodes by connections" is enabled, the system SHALL compute the connection count for each node from the currently visible edges and scale node radii linearly between a minimum radius (5px) and maximum radius (20px). The node with the highest connection count SHALL have the maximum radius. Nodes with zero visible connections SHALL have the minimum radius.

#### Scenario: High-degree node is larger than low-degree node
- **WHEN** "Scale nodes by connections" is enabled and node A has 10 connections and node B has 2 connections
- **THEN** node A's radius is larger than node B's radius

#### Scenario: Node with zero connections gets minimum radius
- **WHEN** "Scale nodes by connections" is enabled and a node has no visible connections
- **THEN** the node renders at the minimum radius (5px)

#### Scenario: Node with most connections gets maximum radius
- **WHEN** "Scale nodes by connections" is enabled and a node has the highest connection count among all visible nodes
- **THEN** the node renders at the maximum radius (20px)

#### Scenario: All nodes have equal connections
- **WHEN** "Scale nodes by connections" is enabled and all visible nodes have the same number of connections
- **THEN** all nodes render at the maximum radius (20px)

### Requirement: Connection counts respect active filters
The connection count for each node SHALL be computed from the currently visible edges only. Toggling edge type filters (Person ↔ Person, Organization → Person) SHALL update node sizes when connection-weighted sizing is enabled.

#### Scenario: Disabling an edge type filter reduces connection counts
- **WHEN** "Scale nodes by connections" is enabled and the user unchecks "Person ↔ Person"
- **THEN** person-person edges are excluded from connection counts and node sizes update accordingly

#### Scenario: Re-enabling an edge type filter restores connection counts
- **WHEN** "Scale nodes by connections" is enabled and the user re-checks a previously unchecked edge type filter
- **THEN** those edges are included in connection counts and node sizes update accordingly

### Requirement: Collision force adjusts to dynamic node sizes
When connection-weighted sizing is enabled, the D3 collision force SHALL use each node's current computed radius (plus padding) to prevent node overlap. When sizing is disabled, the collision force SHALL revert to the fixed collision radius.

#### Scenario: Large nodes do not overlap
- **WHEN** "Scale nodes by connections" is enabled and two high-degree nodes are near each other
- **THEN** the collision force keeps them separated based on their actual rendered radii

#### Scenario: Collision reverts when sizing is disabled
- **WHEN** the user unchecks "Scale nodes by connections"
- **THEN** the collision force reverts to the fixed collision radius (18px)
