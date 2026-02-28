## Context

The graph visualization in `frontend/src/routes/graph/+page.svelte` uses D3 to render a force-directed network graph. Currently, all D3 element colors are hardcoded hex values:
- Organization nodes: `#f97316` (orange)
- Person nodes: `#4f46e5` (indigo)
- Edge lines: `#9ca3af` (gray)
- Edge note labels: `#6b7280` (medium gray)
- Node labels: `#374151` (dark gray)

These don't match the app's warm-brown accent palette (`--accent: #b45828` light / `#d4753e` dark) and don't respond to theme changes. Every other styled element in the app uses CSS variables defined in `+layout.svelte`.

## Goals / Non-Goals

**Goals:**
- Graph node, edge, and label colors align with the app's CSS variable theme system
- Graph colors respond correctly when the user toggles light/dark mode
- Organization and person nodes remain visually distinct from each other

**Non-Goals:**
- Changing graph layout, forces, or interaction behavior
- Adding new CSS variables to the global theme (use existing variables)
- Modifying the backend graph API
- Making the legend or filter checkboxes styled differently

## Decisions

### 1. Read CSS variables via `getComputedStyle` at render time

D3 sets SVG attributes directly (not via CSS classes), so we need to resolve CSS variable values to concrete hex/rgb strings. At the top of `initGraph`, read the needed variables from `document.documentElement` using `getComputedStyle`. This is a one-time read at mount.

**Alternative considered**: Using CSS classes on SVG elements and letting the browser resolve variables. Rejected because D3's `.attr('fill', ...)` sets inline attributes which override CSS classes, and refactoring to use `.style()` throughout would be a larger change with less control.

### 2. Color mapping

| Element | Current | New source |
|---------|---------|------------|
| Organization nodes | `#f97316` | `--accent` |
| Person nodes | `#4f46e5` | `--text-tertiary` |
| Edge lines | `#9ca3af` | `--border` |
| Edge note labels | `#6b7280` | `--text-tertiary` |
| Node labels | `#374151` | `--text-primary` |

Organization nodes use the accent color to match icon styling throughout the app. Person nodes use `--text-tertiary` to remain distinct from orgs while staying within the theme palette. This avoids introducing new CSS variables.

**Alternative considered**: A dedicated `--graph-person` variable. Rejected to avoid variable sprawl for a single use case.

### 3. Theme change reactivity

Listen for changes to the `data-theme` attribute on `<html>` via a `MutationObserver`. When the theme changes, re-read CSS variables and update D3 element colors in place (`.attr('fill', newColor)`). This avoids re-initializing the entire graph.

**Alternative considered**: Destroying and re-creating the graph on theme change. Rejected because it would lose the current zoom/pan state and node positions.

## Risks / Trade-offs

- **[Subtle color distinction]** Using `--text-tertiary` for person nodes may not provide enough contrast against `--accent` for org nodes in some themes. Mitigation: the size difference (7px vs 9px radius) provides a secondary visual cue. Can be adjusted post-implementation if needed.
- **[MutationObserver overhead]** Minimal — only fires on theme toggle, which is infrequent. Observer is disconnected on component destroy via `onMount` cleanup.
