## Why

The network graph currently renders all 50-70+ nodes equally in a single force-directed layout. As the network grows, it becomes harder to see structural patterns (which people cluster around which organizations) and to explore a specific person's connections without visual noise from the rest of the graph. Two lightweight structural features — ego focus and org cluster hulls — would make the graph significantly more useful for exploring connections and seeing the shape of the network.

## What Changes

- **Ego/neighborhood focus mode**: Clicking a node and pressing "Focus" in the detail sidebar fades all non-neighbor nodes/edges to low opacity, leaving the focused node and its direct connections vivid. A toggle switches between 1-hop (default) and 2-hop neighborhoods. Clicking "Focus" again or clicking empty canvas exits focus mode. Layout does not re-simulate — only opacity changes, preserving spatial context.
- **Organization cluster hulls**: For each organization, a convex hull is drawn around the org node and all people connected to it via org-person relationships. Hulls render as low-opacity filled regions with subtle borders behind the nodes. Overlapping hulls (people in multiple orgs) are expected and informative. A toggle checkbox in the controls panel shows/hides cluster hulls.

## Non-goals

- Community detection algorithms (e.g., Louvain) — this uses only explicit org-person edges, not computed clusters
- Path finding between nodes
- Re-layout or subgraph extraction — focus mode only changes opacity, not layout
- Interaction or temporal overlays
- Person tag-based clustering

## Capabilities

### New Capabilities
- `graph-focus-mode`: Ego/neighborhood focus mode — fade non-neighbors to explore a node's local network at 1-hop or 2-hop depth
- `graph-org-clusters`: Organization cluster visualization — convex hull overlays around org-person groupings

### Modified Capabilities
- `network-frontend`: Graph visualization parity requirement updated to include focus mode controls in detail sidebar and cluster hull toggle in graph controls

## Impact

- **Frontend only** — no API changes required. All data needed (nodes, edges, org-person relationships) is already returned by the graph API.
- **Files**: `frontend/src/routes/network/graph/+page.svelte` (main graph component where all rendering logic lives)
- **Dependencies**: D3's `d3.polygonHull()` for convex hull computation (already available via d3 dependency)
