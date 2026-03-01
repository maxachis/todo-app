## ADDED Requirements

### Requirement: Ego/neighborhood focus mode
The graph view SHALL provide an ego/neighborhood focus mode that highlights a selected node and its direct connections while fading all other elements to low opacity. Focus mode SHALL preserve the existing graph layout (no re-simulation or re-layout). Focus mode opacity fading SHALL be applied on top of existing filter visibility — hidden nodes remain hidden, visible non-neighbor nodes get faded.

#### Scenario: Enter focus mode via detail sidebar
- **WHEN** a node's details are displayed in the sidebar and the user clicks the "Focus" button
- **THEN** the selected node and all nodes directly connected to it (1-hop neighbors) SHALL remain at full opacity, and all other visible nodes, edges, and labels SHALL fade to approximately 10% opacity

#### Scenario: Exit focus mode via unfocus button
- **WHEN** focus mode is active and the user clicks the "Unfocus" button in the sidebar
- **THEN** all nodes, edges, and labels SHALL return to their normal opacity based on current filter settings

#### Scenario: Exit focus mode via canvas click
- **WHEN** focus mode is active and the user clicks on empty canvas area (not on a node or edge)
- **THEN** focus mode SHALL deactivate and all elements SHALL return to normal opacity

#### Scenario: Edges in focus mode
- **WHEN** focus mode is active for a node
- **THEN** only edges where both endpoints are in the focused neighborhood SHALL remain at full opacity; all other edges SHALL fade

#### Scenario: Labels in focus mode
- **WHEN** focus mode is active
- **THEN** labels for faded nodes SHALL also fade to match their node's opacity

### Requirement: Two-hop neighborhood toggle
The graph view SHALL provide a depth toggle when focus mode is active, allowing the user to switch between 1-hop (default) and 2-hop neighborhood depth.

#### Scenario: Default focus depth is 1-hop
- **WHEN** the user enters focus mode
- **THEN** the neighborhood depth SHALL default to 1-hop (only direct connections)

#### Scenario: Switch to 2-hop depth
- **WHEN** focus mode is active and the user toggles the depth to 2-hop
- **THEN** the focused neighborhood SHALL expand to include the selected node, its direct connections, and their direct connections (friends of friends)

#### Scenario: Switch back to 1-hop depth
- **WHEN** focus mode is active at 2-hop depth and the user toggles back to 1-hop
- **THEN** the focused neighborhood SHALL contract to include only the selected node and its direct connections
