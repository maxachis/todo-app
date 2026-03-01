## 1. Connection Count Logic

- [x] 1.1 Add a function to compute connection counts per node from the filtered edge list — returns a `Map<string, number>` keyed by node ID. File: `frontend/src/routes/network/graph/+page.svelte`
- [x] 1.2 Add a function to compute scaled radius given a connection count, max connection count, min radius (5), and max radius (20) using linear interpolation. File: `frontend/src/routes/network/graph/+page.svelte`

## 2. UI Toggle

- [x] 2.1 Add a `scaleByConnections` checkbox element ref and wire it into the Filters card after "Show relationship notes". File: `frontend/src/routes/network/graph/+page.svelte`
- [x] 2.2 Add an event listener on the checkbox that triggers re-rendering of node radii and collision force update

## 3. Dynamic Node Rendering

- [x] 3.1 Update the node circle `.attr('r', ...)` call to use the scaled radius when `scaleByConnections` is checked, falling back to the fixed type-based radius when unchecked
- [x] 3.2 Update the `forceCollide` radius to use a per-node function that returns the node's current radius plus padding when sizing is enabled, reverting to 18px when disabled
- [x] 3.3 Ensure filter toggles (People, Organizations, Person ↔ Person, Org → Person) recompute connection counts and update node sizes when `scaleByConnections` is active

## 4. Verification

- [ ] 4.1 Manual test: enable toggle with a graph containing nodes of varying degree — confirm high-degree nodes are visibly larger
- [ ] 4.2 Manual test: toggle edge type filters while sizing is enabled — confirm node sizes update
- [ ] 4.3 Manual test: disable toggle — confirm nodes revert to fixed type-based sizes and collision force resets
- [x] 4.4 Run `cd frontend && npm run check` to verify no type errors
