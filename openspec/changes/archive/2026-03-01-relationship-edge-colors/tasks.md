## 1. Backend: Add relationship type to graph edge data

- [x] 1.1 Add `select_related("relationship_type")` to both relationship querysets in `network/api/graph.py`
- [x] 1.2 Include `relationship_type_id` and `relationship_type_name` fields in person-person and org-person edge data dicts in `network/api/graph.py`
- [x] 1.3 Update `frontend/src/lib/api/types.ts` — add `relationship_type_id: number | null` and `relationship_type_name: string | null` to `GraphEdge['data']`

## 2. Frontend: Edge color localStorage store

- [x] 2.1 Add edge color persistence logic in the graph component: load/save a `Record<string, string>` from localStorage key `'graph-edge-colors'`, with type keys formatted as `"pp-{id}"` or `"op-{id}"`
- [x] 2.2 Add a helper function to get the edge color for a given edge (lookup by type key, fallback to `--border` color)

## 3. Frontend: Edge color picker UI

- [x] 3.1 Add an "Edge Colors" section in the graph left sidebar controls (below layout sliders) in `frontend/src/routes/network/graph/+page.svelte`
- [x] 3.2 Extract distinct relationship types from loaded graph edge data and render each as a row with type name + `<input type="color">`
- [x] 3.3 Show "No relationship types" message when no typed edges exist
- [x] 3.4 Add a "Reset" button that clears the `'graph-edge-colors'` localStorage entry and reverts all edges to default

## 4. Frontend: Apply edge colors to graph rendering

- [x] 4.1 Update the D3 edge rendering in `+page.svelte` to use the edge color lookup function instead of the static `colors.border` value
- [x] 4.2 Update the theme-change handler (MutationObserver) to re-apply edge colors correctly — custom colors persist, uncolored edges update to new theme's `--border`
- [x] 4.3 Update hover/detail display to show the edge's relationship type name when available

## 5. Verification

- [x] 5.1 Verify graph renders with default colors when no custom colors are set
- [x] 5.2 Verify color picker changes edge color immediately
- [x] 5.3 Verify colors persist across page reload
- [x] 5.4 Verify "Reset" reverts all edges to default
- [x] 5.5 Verify theme toggle preserves custom colors while updating defaults
- [x] 5.6 Run `cd frontend && npm run check` to verify no type errors
