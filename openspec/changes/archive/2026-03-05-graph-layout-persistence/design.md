## Context

The network graph page (`frontend/src/routes/network/graph/+page.svelte`) uses D3 force simulation with configurable layout sliders (spacing, repulsion, centering, label size) and filter checkboxes. Currently, cluster colors and edge colors already persist to localStorage using dedicated keys (`graph-cluster-colors`, `graph-edge-colors`). Layout sliders and filters reset to hardcoded defaults on every page load.

## Goals / Non-Goals

**Goals:**
- Persist all layout slider values and filter checkbox states to localStorage
- Restore saved values on page load, using current defaults as fallbacks
- Follow the same localStorage persistence pattern already used for colors

**Non-Goals:**
- Persisting zoom/pan transform, node positions, or focus mode
- Server-side settings storage
- Adding a "reset to defaults" button for layout settings (though the pattern makes this trivial to add later)

## Decisions

### 1. Single localStorage key for all graph settings

Store all layout and filter settings under one key (`graph-layout-settings`) as a JSON object, rather than one key per setting.

**Rationale**: The graph already uses per-concern keys for colors, but layout settings are a cohesive group that are always loaded/saved together. A single key reduces localStorage clutter and simplifies the save/load logic.

**Alternative considered**: Individual keys per setting (e.g., `graph-spacing`, `graph-repulsion`). Rejected — too many keys for simple scalar values that belong together.

### 2. Save on input change, load on mount

Save to localStorage whenever a slider or checkbox changes (inside the existing `attachInput` handler). Load from localStorage during `onMount` before initializing the graph, applying values to the input elements before D3 reads them.

**Rationale**: Matches the existing color persistence pattern. No debouncing needed — localStorage writes are synchronous and fast for small payloads.

### 3. Initialize HTML input values before graph init

Set input element values from localStorage *before* calling `initGraph()`, so the existing `updateForces()` / `refreshVisibility()` calls pick up the correct values naturally without any changes to the D3 logic.

**Rationale**: Minimizes changes to the existing graph initialization flow. The slider/checkbox refs are bound by the time `onMount` runs, so we can set `.value` / `.checked` directly.

## Risks / Trade-offs

- **Stale settings after UI changes**: If we add/remove a filter checkbox in the future, old localStorage data may have extra or missing keys. → Mitigation: Use fallback defaults for any missing key; ignore unknown keys.
- **localStorage unavailable**: Private browsing or storage full. → Mitigation: Wrap in try/catch (same as existing color persistence), gracefully fall back to defaults.
