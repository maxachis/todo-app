## Context

The network graph currently renders all edges with the same `--border` CSS variable color. Relationship types already exist in the data model (`PersonPersonRelationshipType`, `OrgPersonRelationshipType`) and are assigned to relationships, but the graph API does not include type information on edges. Users have no way to visually distinguish different relationship types in the graph.

## Goals / Non-Goals

**Goals:**
- Enable per-relationship-type edge coloring in the graph visualization
- Provide a simple color picker UI in the graph controls panel
- Persist color assignments across sessions via localStorage
- Include type information in graph edge API data

**Non-Goals:**
- Backend storage of color preferences (client-side only)
- Changing node colors or edge thickness/style
- Color picker for edges without a relationship type (they keep the default)

## Decisions

### 1. Add relationship type info to graph edge API data

**Decision**: Extend the graph API response to include `relationship_type_id` and `relationship_type_name` on each edge.

**Rationale**: The frontend needs to know which type each edge belongs to in order to look up its assigned color. The type ID serves as the localStorage key, and the type name is displayed in the color picker UI.

**Alternative considered**: Fetch relationship types separately and join client-side. Rejected because the graph endpoint already has the relationships loaded with their types; adding two fields is simpler than an extra API call and client-side join.

**Implementation**: Add `select_related("relationship_type")` to both relationship querysets in `graph.py` and include the fields in the edge data dict.

### 2. localStorage for color persistence

**Decision**: Store a JSON map of `{ [typeKey]: hexColor }` in localStorage under the key `'graph-edge-colors'`, where `typeKey` is `"pp-{id}"` for person-person types and `"op-{id}"` for org-person types.

**Rationale**: Follows the established pattern (theme, panel widths, completion sound) — simple, no backend changes, immediate persistence. The type-prefixed key prevents ID collisions between the two type tables.

**Alternative considered**: Backend model for user color preferences. Rejected as over-engineering for a single-user app with an established localStorage pattern.

### 3. Native HTML color input

**Decision**: Use `<input type="color">` for the color picker.

**Rationale**: Zero dependencies, works in all modern browsers, provides a familiar OS-native color picker dialog. Consistent with the app's minimal-dependency approach.

**Alternative considered**: Third-party color picker library (e.g., svelte-color-picker). Rejected to avoid adding a dependency for a simple feature.

### 4. Color picker placement in graph controls

**Decision**: Add an "Edge Colors" collapsible section in the existing left sidebar controls panel, below the layout sliders. Each relationship type gets a row with its name and a color swatch/input. A "Reset" button clears all custom colors.

**Rationale**: Keeps all graph controls in one place. The collapsible section avoids cluttering the panel when the feature isn't actively being used.

### 5. Edge color application with fallback

**Decision**: When rendering edges, look up the edge's `relationship_type_id` in the color map. If found, use that color. If not found (no type assigned, or no color set for that type), fall back to the theme's `--border` color.

**Rationale**: Graceful degradation — edges without types or without custom colors behave exactly as before.

## Risks / Trade-offs

- **[Risk: Type deletion]** If a relationship type is deleted, its color entry becomes orphaned in localStorage. → Mitigation: Harmless — orphaned entries are tiny and ignored. The "Reset" button clears them all.
- **[Risk: Many relationship types]** With many types, the color picker section could get long. → Mitigation: The section is collapsible, and in practice a single user is unlikely to have more than ~10-15 relationship types.
- **[Trade-off: No edge legend]** We don't add a color legend overlay on the graph itself. → The color picker section in the sidebar already shows the type-to-color mapping and serves as the legend.
