## Why

The network graph page resets all layout sliders (spacing, repulsion, centering, label size) and filter checkboxes to their defaults every time the page is loaded. Users who have tuned these settings to their preferred view lose their configuration on every navigation. Cluster colors and edge colors already persist via localStorage — layout settings should follow the same pattern for a consistent experience.

## What Changes

- Persist graph layout slider values (spacing, repulsion, centering, label size) to localStorage
- Persist graph filter checkbox states (People, Organizations, Person-Person, Org-Person, Hide isolated, Show relationship notes, Scale by connections, Show org clusters) to localStorage
- Restore persisted values on page load, falling back to current defaults when no saved state exists

## Capabilities

### New Capabilities
- `graph-layout-persistence`: Persist and restore graph layout settings (sliders and filter checkboxes) across sessions via localStorage

### Modified Capabilities

_(none — existing graph specs cover rendering and interaction, not settings persistence)_

## Non-goals

- Persisting zoom/pan position or individual node positions
- Persisting focus mode state
- Server-side storage of graph preferences
- Undo/reset-to-defaults UI (beyond the existing reset buttons for colors)

## Impact

- **Frontend**: `frontend/src/routes/network/graph/+page.svelte` — add localStorage read/write for layout settings, initialize inputs from stored values
- **No backend changes** — purely client-side localStorage
- **No new dependencies**
