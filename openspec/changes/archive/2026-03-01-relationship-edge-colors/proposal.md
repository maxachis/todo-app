## Why

All edges in the network graph currently render with the same `--border` color, making it impossible to visually distinguish different relationship types at a glance. Adding per-relationship-type edge colors with a color picker lets users immediately see patterns in their network (e.g., "friends" vs "colleagues" vs "mentors") and the colors persist across sessions via localStorage.

## What Changes

- Add a color picker UI in the graph controls panel that lets users assign a color to each relationship type (both person-person and org-person types).
- Render graph edges using the assigned color for their relationship type, falling back to the default `--border` color for unassigned types.
- Persist color assignments in localStorage so they survive page reloads and sessions.
- Add a "Reset colors" button to clear all custom edge color assignments.

## Non-goals

- Changing node colors (those remain theme-driven).
- Backend storage of color preferences (this is a client-side preference only).
- Changing edge thickness or style (dashed, dotted) per relationship type — only color.

## Capabilities

### New Capabilities
- `edge-color-customization`: Per-relationship-type edge color assignment with color picker, localStorage persistence, and default fallback.

### Modified Capabilities
- `network-frontend`: Graph visualization edges now use per-type colors instead of a single `--border` color.

## Impact

- **Frontend**: `frontend/src/routes/network/graph/+page.svelte` — edge rendering logic, new color picker controls, localStorage read/write.
- **Frontend API types**: May need relationship type info included in graph edge data (currently edges have `type` but not the specific relationship type name/ID).
- **Backend API**: `network/api/graph.py` — may need to include `relationship_type` ID and name on edge data so the frontend can map colors.
- **No database changes**: Colors are stored client-side only.
- **No new dependencies**: Native HTML `<input type="color">` for the picker.
