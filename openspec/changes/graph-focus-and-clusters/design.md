## Context

The network graph (`frontend/src/routes/network/graph/+page.svelte`) is a D3 force-directed SVG visualization with ~50-70+ nodes (people and organizations) connected by person-person and org-person relationship edges. The graph already supports filtering, search, zoom/pan, drag, edge coloring by relationship type, and configurable layout forces. All graph logic lives in one ~680-line Svelte component.

The graph API returns all nodes and edges in a flat structure. Org-person edges already encode which people belong to which organizations — no additional data is needed.

## Goals / Non-Goals

**Goals:**
- Let users focus on a specific node's local neighborhood (1-hop default, 2-hop toggle) via opacity fade
- Visualize organizational clusters as convex hull overlays behind the graph
- Keep both features lightweight, frontend-only, and consistent with existing graph controls

**Non-Goals:**
- No graph re-layout or subgraph extraction in focus mode
- No algorithmic community detection — clusters are strictly org-person based
- No persistence of focus state or cluster preferences beyond the show/hide toggle
- No new API endpoints or backend changes

## Decisions

### 1. Focus mode via opacity rather than DOM removal

**Decision**: When a node is focused, set non-neighbor elements to `opacity: 0.08` via D3 `.attr('opacity', ...)`. Do not remove or re-layout.

**Why**: Preserves spatial context — the user can still see where the focused node sits in the overall graph. Simpler than re-simulation and avoids layout jumps. Consistent with how existing filter/hide works (display toggling), but using opacity instead since we want the faded nodes to remain in their positions.

**Alternative considered**: Remove non-neighbors and re-simulate a subgraph. Rejected because it loses the "where does this fit in the big picture" context and causes jarring layout changes.

### 2. Adjacency computed client-side from links array

**Decision**: Build an adjacency map from the existing `links` array when the graph initializes. For 1-hop: neighbors = all nodes directly linked. For 2-hop: neighbors = 1-hop neighbors + their neighbors.

**Why**: The links array is already in memory. Building adjacency is O(E) and lookup is O(1) per node. No API call needed.

### 3. Focus entry via button in Details card

**Decision**: Add a "Focus" button to the Details card (sidebar) when a node is hovered/selected. The button toggles focus mode for that node.

**Why**: The Details card already shows node info on hover. Adding a button there is a natural extension. A separate "Focus" button in the card avoids conflicting with node drag/hover interactions on the graph canvas itself.

**Interaction flow**:
1. Hover a node → details appear in sidebar with "Focus" button
2. Click "Focus" → focus mode activates for that node, button text changes to "Unfocus"
3. Click "Unfocus" OR click empty canvas → exit focus mode
4. While focused, a depth toggle (1-hop / 2-hop) appears below the button

### 4. Convex hulls via D3 polygonHull, rendered as SVG paths

**Decision**: For each organization, collect the `[x, y]` coordinates of the org node + all people connected via org-person edges. Pass to `d3.polygonHull()` to get the hull polygon. Render as SVG `<path>` elements in a group layer inserted *before* the links group (so hulls appear behind everything).

**Why**: D3's polygonHull is already available (part of d3 dependency). SVG paths with low fill opacity are simple to render and update on each simulation tick.

**Edge cases**:
- **1 node** (org with no people): No hull drawn (polygonHull needs ≥3 points). Skip silently.
- **2 nodes** (org + 1 person): polygonHull returns null for collinear points. Skip or draw nothing — a hull around 2 points isn't useful.
- **People in multiple orgs**: They appear in multiple hulls. Hulls may overlap — this is correct and informative.

**Hull styling**: Fill using the org node's accent color at ~10% opacity, with a 1px border at ~20% opacity. Add ~15px padding around hull points so the hull visually encompasses the nodes rather than passing through their centers.

### 5. Hull positions update on simulation tick

**Decision**: Recompute hull paths on each D3 simulation tick alongside existing position updates.

**Why**: Nodes move during simulation and during drag. Hulls must follow. The tick handler already updates all positions — adding hull path recomputation there keeps it in sync.

**Performance**: polygonHull is O(n log n) per hull, but n per hull is small (typically 2-10 nodes). With ~10-20 orgs, this is negligible.

### 6. Show/hide toggle for hulls in Filters card

**Decision**: Add a "Show org clusters" checkbox to the existing Filters card, defaulting to checked.

**Why**: Consistent with existing filter controls. Users may want to toggle hulls off when they're visually cluttering the graph.

### 7. Focus mode interacts correctly with existing filters

**Decision**: Focus mode opacity is applied *on top of* existing filter visibility. Hidden nodes (via filter) remain hidden. Visible nodes that aren't in the focused neighborhood get faded.

**Why**: Filters and focus serve different purposes. Filters remove node types entirely; focus highlights a neighborhood within the visible graph.

## Risks / Trade-offs

- **Hull visual noise at high density**: With many overlapping orgs, hull overlays could get busy → Mitigated by the show/hide toggle and low opacity (10%)
- **Focus + hull interaction**: When focusing a node, should hulls outside the neighborhood also fade? → Yes, fade hulls whose org is not in the focused neighborhood, for visual consistency
- **2-hop neighborhoods can be large**: A well-connected node's 2-hop neighborhood might include most of the graph → Acceptable; the toggle defaults to 1-hop, and 2-hop is an explicit user choice
