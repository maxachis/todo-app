## 1. Adjacency Map & Focus State

- [x] 1.1 Build adjacency map from links array after graph init — `Map<string, Set<string>>` mapping each node ID to its direct neighbor IDs. File: `frontend/src/routes/network/graph/+page.svelte`
- [x] 1.2 Add focus state variables: `focusedNodeId` (string | null), `focusDepth` (1 | 2). Add a `getNeighborhood(nodeId, depth)` function that returns the Set of node IDs in the neighborhood using the adjacency map. File: `frontend/src/routes/network/graph/+page.svelte`

## 2. Focus Mode UI Controls

- [x] 2.1 Update `renderDetails` to include a "Focus" / "Unfocus" button in the Details card when a node is displayed. Wire the button to set/clear `focusedNodeId`. File: `frontend/src/routes/network/graph/+page.svelte`
- [x] 2.2 Add a depth toggle (1-hop / 2-hop) that appears below the Focus button when focus mode is active. Wire it to update `focusDepth` and refresh opacity. File: `frontend/src/routes/network/graph/+page.svelte`
- [x] 2.3 Add canvas click handler on the SVG background to exit focus mode — clear `focusedNodeId` when clicking empty canvas (not on a node or edge). File: `frontend/src/routes/network/graph/+page.svelte`

## 3. Focus Mode Opacity

- [x] 3.1 Create `applyFocusOpacity()` function: when `focusedNodeId` is set, compute neighborhood via `getNeighborhood()`, then set node circles, labels, edges, and edge labels to ~0.08 opacity if not in the neighborhood, full opacity if in it. Edges are fully opaque only if both endpoints are in the neighborhood. When `focusedNodeId` is null, reset all to full opacity. File: `frontend/src/routes/network/graph/+page.svelte`
- [x] 3.2 Call `applyFocusOpacity()` from the Focus/Unfocus button handler, depth toggle handler, and canvas click handler. Ensure it respects existing filter visibility (hidden nodes stay hidden). File: `frontend/src/routes/network/graph/+page.svelte`

## 4. Organization Cluster Hulls

- [x] 4.1 Build org-cluster data structure after graph init: for each organization node, collect the org node + all people connected via org-person edges into a `Map<string, string[]>` (org ID → array of member node IDs including the org itself). File: `frontend/src/routes/network/graph/+page.svelte`
- [x] 4.2 Add a `<g class="hulls">` SVG group inserted before the links group in `zoomLayer`. For each org cluster with 3+ members, compute `d3.polygonHull()` from padded node positions and render as `<path>` with accent color fill at 10% opacity and 1px border at 20% opacity. File: `frontend/src/routes/network/graph/+page.svelte`
- [x] 4.3 Update the simulation tick handler to recompute and redraw hull paths on each tick so hulls follow node movement. File: `frontend/src/routes/network/graph/+page.svelte`

## 5. Hull Controls & Integration

- [x] 5.1 Add "Show org clusters" checkbox to the Filters card (default checked). Bind it to show/hide the hulls group. Wire it through the existing `attachInput` pattern. File: `frontend/src/routes/network/graph/+page.svelte`
- [x] 5.2 Integrate hulls with focus mode: in `applyFocusOpacity()`, also set hull opacity — hulls whose org node is in the focused neighborhood stay at full opacity, others fade to ~0.08. File: `frontend/src/routes/network/graph/+page.svelte`

## 6. Verification

- [ ] 6.1 Manual test: verify focus mode activates/deactivates via Focus button, Unfocus button, and canvas click. Verify 1-hop shows only direct connections and 2-hop expands correctly.
- [ ] 6.2 Manual test: verify org cluster hulls render around orgs with 3+ people, no hull for small clusters, overlapping hulls for shared members, and hulls follow node drag.
- [ ] 6.3 Manual test: verify hull toggle hides/shows hulls, and focus mode correctly fades non-neighborhood hulls. Verify dark/light theme colors are correct.
