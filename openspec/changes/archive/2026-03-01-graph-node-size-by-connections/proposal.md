## Why

The network graph currently renders all nodes at a fixed size based on type (person vs organization). This makes highly-connected nodes visually indistinguishable from isolated ones. Scaling node radius by connection count would let users instantly identify key hubs and central figures in their network.

## What Changes

- Add an optional toggle in the graph controls panel to enable connection-weighted node sizing
- When enabled, compute each node's connection count from the edge data and scale the node radius proportionally
- Adjust the D3 collision force radius to match dynamic node sizes so nodes don't overlap
- Default behavior remains unchanged (fixed size by type) until the user enables the option

## Non-goals

- Changing node colors based on connection count (colors remain type-based)
- Backend API changes — connection counts can be derived client-side from the existing edge data
- Persisting the toggle state to localStorage (may be added later)

## Capabilities

### New Capabilities
- `graph-node-sizing`: Toggle and logic for scaling graph node radius by connection count

### Modified Capabilities
- `network-frontend`: Adds a new graph control and modifies node rendering behavior in the Graph visualization requirement

## Impact

- **Frontend**: `frontend/src/routes/network/graph/+page.svelte` — node rendering, collision force, controls panel
- **No backend changes**: Connection counts are computed from existing graph edge data on the client
- **No new dependencies**: Uses existing D3 APIs
