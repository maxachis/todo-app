## Context

The network graph page (`/network/graph`) uses D3.js to render a force-directed graph of people and organizations. Nodes are currently rendered with fixed radii: 9px for organizations and 7px for people. The graph API returns nodes and edges, from which connection counts per node can be trivially computed client-side by counting edge references.

The controls panel already has Filters, Search, and Layout sections with real-time slider controls. Adding a node sizing toggle fits naturally into this pattern.

## Goals / Non-Goals

**Goals:**
- Let users toggle connection-weighted node sizing to visually identify network hubs
- Compute connection counts client-side from existing edge data (no API changes)
- Scale nodes smoothly between a minimum and maximum radius
- Keep the collision force in sync with dynamic node sizes to prevent overlap

**Non-Goals:**
- Backend changes or new API fields for connection counts
- Persisting the toggle state across sessions
- Changing node colors based on connection count
- Logarithmic or other non-linear scaling (linear is sufficient for typical network sizes)

## Decisions

### 1. Client-side connection counting
**Decision**: Count connections per node by iterating the filtered edge list after applying visibility filters.

**Rationale**: The graph endpoint already returns all edges. Computing counts client-side avoids API changes and ensures counts reflect the currently visible edges (respecting filter toggles for person-person vs org-person edges).

**Alternative considered**: Adding a `connection_count` field to the graph API response — rejected because it would not respect client-side filter state and adds unnecessary backend coupling.

### 2. Linear radius scaling with clamped range
**Decision**: Scale radius linearly from a base minimum (5px) to a maximum (20px) based on connection count relative to the max connection count in the current graph.

```
radius = minRadius + (connectionCount / maxConnectionCount) * (maxRadius - minRadius)
```

Nodes with zero connections get `minRadius`. The node with the most connections gets `maxRadius`.

**Rationale**: Linear scaling is simple, predictable, and effective for the typical network sizes in a personal CRM (tens to low hundreds of nodes). The clamped range prevents nodes from being too small to interact with or too large to fit.

**Alternative considered**: Logarithmic scaling — better for power-law distributions with very high-degree nodes, but over-engineers for this use case.

### 3. Toggle in Filters card
**Decision**: Add a "Scale nodes by connections" checkbox in the existing Filters card, alongside the other visibility toggles.

**Rationale**: It's a visual display option that conceptually groups with the filter controls. Adding a new card would be unnecessary for a single checkbox.

### 4. Dynamic collision force radius
**Decision**: Update the D3 `forceCollide` radius function to use each node's computed radius (plus padding) when sizing is enabled.

**Rationale**: Without adjusting collision, larger nodes would overlap. D3's `forceCollide` accepts a per-node radius function, making this straightforward.

## Risks / Trade-offs

- **[Performance with large graphs]** → Connection counting is O(edges), which is negligible. Re-running the force simulation on toggle is the existing pattern for other controls, so no new concern.
- **[Visual clutter with many high-degree nodes]** → The clamped max radius (20px) prevents any single node from dominating. The existing repulsion and spacing controls give users further adjustment.
- **[Filtered edges change counts]** → Toggling person-person or org-person edge visibility will change connection counts and node sizes when sizing is enabled. This is correct behavior — sizes should reflect the visible network.
