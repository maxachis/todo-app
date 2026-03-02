## Context

The notebook view (`/notebook`) uses a CSS grid with `grid-template-columns: 220px 1fr` for its two-panel layout. The sidebar is always visible and contains page navigation (New Page, Today buttons, Recent/Daily page lists). The editor area fills the remaining space.

The app already has established patterns for collapsible UI elements:
- Section collapse in task lists using a `Set<number>` toggle pattern with chevron icons
- `NotebookMentions.svelte` uses a simple `$state(false)` boolean for collapse
- The main layout uses `detailOpen` state for mobile detail panel toggling
- localStorage persistence is used throughout (theme, panel widths)

## Goals / Non-Goals

**Goals:**
- Allow users to collapse the notebook sidebar to maximize editor space
- Persist collapse state across page reloads via localStorage
- Provide both a visible toggle button and a keyboard shortcut
- Smooth transition when collapsing/expanding

**Non-Goals:**
- Drag-to-resize sidebar width
- Mobile-responsive sidebar behavior
- Changing sidebar content or grouping

## Decisions

### 1. Toggle state management: Svelte `$state` boolean + localStorage

Use a simple reactive boolean `sidebarCollapsed` initialized from localStorage. On toggle, update both the reactive state and localStorage.

**Why over a Svelte store in a separate file:** The state is local to the notebook page component — no other component needs it. A page-level `$state` variable with `$effect` for localStorage sync is simpler and follows the `NotebookMentions` precedent.

**Alternative considered:** A dedicated store in `stores/` like `panelWidths.ts`. Rejected because this is a single boolean used in one route, not shared state.

### 2. CSS transition for collapse animation

Use `grid-template-columns` transition with a CSS transition on the grid container. When collapsed, set columns to `0px 1fr` with `overflow: hidden` on the sidebar. A ~200ms ease transition provides smooth animation.

**Why over JS-driven animation:** CSS grid transitions are GPU-accelerated, simple to implement, and don't require JS animation libraries. The grid approach means the editor naturally fills the space.

**Alternative considered:** Using `display: none` or `width: 0` on the sidebar. Rejected because grid column transition is smoother and the editor resizes naturally.

### 3. Toggle button placement: Inside the sidebar header area, persists when collapsed

Place a small toggle button (chevron icon) at the top of the sidebar. When collapsed, render a slim vertical strip (~32px) with just the expand button so users can re-open the sidebar without the keyboard shortcut.

**Why over a button in the editor toolbar:** The toggle conceptually belongs to the sidebar. A persistent slim strip is a common pattern (VS Code, Notion) and ensures discoverability.

### 4. Keyboard shortcut: `Cmd/Ctrl + \`

Use `Cmd+\` (Mac) / `Ctrl+\` (Windows/Linux) as the toggle shortcut. This mirrors VS Code's sidebar toggle.

**Why this shortcut:** It's an established convention for sidebar toggles in developer tools. Low collision risk with other app shortcuts.

### 5. localStorage key: `notebook-sidebar-collapsed`

Store as `"true"` / `"false"` string under this key, following the app's existing localStorage patterns.

## Risks / Trade-offs

- **[CSS grid transition support]** → All modern browsers support grid transitions. No polyfill needed.
- **[Keyboard shortcut collision]** → `Cmd/Ctrl+\` is rarely used by browsers. If collision is found, can be changed without architectural impact.
- **[Collapsed state hides navigation]** → Mitigated by the persistent slim expand button strip. Users always have a visible way to re-expand.
