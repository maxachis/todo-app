### Requirement: Graph API includes relationship type on edges
The graph API endpoint (`GET /api/graph/`) SHALL include `relationship_type_id` (integer or null) and `relationship_type_name` (string or null) fields on each edge in the response. Person-person edges SHALL use the person-person relationship type. Organization-person edges SHALL use the org-person relationship type.

#### Scenario: Edge with relationship type
- **WHEN** a relationship has a type assigned
- **THEN** the graph edge data SHALL include `relationship_type_id` set to the type's ID and `relationship_type_name` set to the type's name

#### Scenario: Edge without relationship type
- **WHEN** a relationship has no type assigned
- **THEN** the graph edge data SHALL include `relationship_type_id` as null and `relationship_type_name` as null

### Requirement: Edge color picker in graph controls
The graph view SHALL display an "Edge Colors" section in the left sidebar controls panel, below the layout sliders. The section SHALL list all relationship types that appear in the current graph data (both person-person and org-person types, deduplicated by type category and ID). Each type row SHALL display the type name and an `<input type="color">` element showing the currently assigned color or the default `--border` color.

#### Scenario: View edge color controls with types present
- **WHEN** the graph loads and relationships have types assigned
- **THEN** the Edge Colors section SHALL list each distinct relationship type with a color picker

#### Scenario: View edge color controls with no typed relationships
- **WHEN** the graph loads and no relationships have types assigned
- **THEN** the Edge Colors section SHALL display a message indicating no relationship types are available

#### Scenario: Pick a color for a relationship type
- **WHEN** the user selects a color from a type's color input
- **THEN** all edges of that relationship type SHALL immediately update to the selected color

### Requirement: Edge color persistence via localStorage
The system SHALL persist edge color assignments in localStorage under the key `'graph-edge-colors'`. The stored value SHALL be a JSON object mapping type keys (format `"pp-{id}"` for person-person types, `"op-{id}"` for org-person types) to hex color strings. Color assignments SHALL be loaded on graph mount and applied to edges.

#### Scenario: Color persists across page reloads
- **WHEN** the user assigns a color to a relationship type and reloads the page
- **THEN** the graph SHALL render edges of that type with the previously assigned color

#### Scenario: localStorage unavailable or corrupted
- **WHEN** localStorage is unavailable or the stored value cannot be parsed
- **THEN** the system SHALL fall back to default `--border` color for all edges

### Requirement: Reset edge colors
The Edge Colors section SHALL include a "Reset" button. Clicking the button SHALL clear all custom color assignments from localStorage and revert all edges to the default `--border` color.

#### Scenario: Reset all edge colors
- **WHEN** the user clicks the "Reset" button
- **THEN** all edges SHALL revert to the default `--border` color and the localStorage entry SHALL be removed

#### Scenario: Reset when no custom colors are set
- **WHEN** no custom colors have been assigned and the user clicks "Reset"
- **THEN** nothing changes visually and no errors occur

### Requirement: Edge color rendering with fallback
Graph edges SHALL be colored based on their relationship type's assigned color. Edges with a type that has an assigned color SHALL use that color. Edges with a type that has no assigned color, or edges with no type at all, SHALL fall back to the theme's `--border` CSS variable color.

#### Scenario: Edge with custom color
- **WHEN** an edge's relationship type has a custom color assigned
- **THEN** the edge line SHALL render in the assigned color

#### Scenario: Edge with type but no custom color
- **WHEN** an edge has a relationship type but no color has been assigned to that type
- **THEN** the edge line SHALL render in the `--border` color

#### Scenario: Edge without relationship type
- **WHEN** an edge has no relationship type assigned
- **THEN** the edge line SHALL render in the `--border` color

#### Scenario: Theme change preserves custom colors
- **WHEN** the user toggles between light and dark themes while custom edge colors are set
- **THEN** edges with custom colors SHALL keep their assigned colors, and edges without custom colors SHALL update to the new theme's `--border` color
