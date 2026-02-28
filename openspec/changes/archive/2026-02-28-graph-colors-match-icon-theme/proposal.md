## Why

The graph visualization uses hardcoded colors (`#f97316` orange for orgs, `#4f46e5` indigo for people, `#9ca3af` gray for edges) that don't match the app's warm-brown accent theme (`--accent`) and don't respond to light/dark mode. Every other icon and accent color in the app uses CSS variables that adapt to the theme, making the graph feel visually disconnected.

## What Changes

- Replace hardcoded D3 node colors with theme-aware colors derived from CSS variables (`--accent`, `--text-primary`, `--text-secondary`, `--border`)
- Organization nodes use the accent color; person nodes use a complementary secondary color from the theme palette
- Edge stroke and label colors use theme-aware grays (`--border`, `--text-tertiary`)
- Node text labels use `--text-primary` so they remain legible in both light and dark mode
- Graph re-renders with correct colors when the user toggles the theme

## Non-goals

- Changing the graph layout algorithm or interaction behavior
- Adding new node types or graph features
- Modifying the backend graph API

## Capabilities

### New Capabilities

_None — this is a visual theming change within the existing graph._

### Modified Capabilities

- `network-frontend`: Graph visualization colors change from hardcoded hex values to theme-aware CSS variable-derived colors, satisfying the existing "Graph visualization parity" requirement with improved theme integration.

## Impact

- **Frontend only**: `frontend/src/routes/graph/+page.svelte` — D3 color assignments
- **Theme system**: May add 1-2 new CSS variables to `+layout.svelte` for graph-specific secondary color if needed
- **No API changes**, no backend changes, no data model changes
