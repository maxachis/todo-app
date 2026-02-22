## Context

The app uses a CSS grid layout defined in `+layout.svelte`. The `.app-shell` grid has `min-height: 100vh` with rows `auto 1fr auto` (header, main, mobile-tabs). The main `.panels` area uses a three-column grid for Tasks and `single-panel` (one column) for all other routes. None of the panels constrain their height or set `overflow-y: auto`, so content growth pushes the entire document to scroll.

Network pages (People, Orgs, Interactions) use a two-column `.network-grid` inside the center panel. Relationships uses a similar two-column grid. Neither grid constrains panel heights.

## Goals / Non-Goals

**Goals:**
- Viewport-locked layout: the app shell fills exactly `100vh` with no document scroll.
- Each panel within a page scrolls independently via `overflow-y: auto`.
- Header stays pinned at all times without `position: fixed` hacks (achieved via grid constraint).

**Non-Goals:**
- Changing mobile/responsive behavior — stacked layouts on narrow screens can continue to use document scroll.
- Adding custom scrollbar styling.
- Virtual scrolling or lazy-loading for long lists.

## Decisions

### 1. Use `height: 100vh` + `overflow: hidden` on `.app-shell` instead of `min-height`

**Rationale**: Switching from `min-height: 100vh` to `height: 100vh` with `overflow: hidden` on the app shell prevents any document-level scroll. The `1fr` row for `main` then gets exactly the remaining viewport height after the header, and panels within can each manage their own overflow.

**Alternative considered**: Using `position: sticky` on the header — rejected because it still allows document scroll and panels wouldn't get a fixed height to enable independent scrolling.

### 2. Set `overflow-y: auto` + `min-height: 0` on each panel

**Rationale**: In CSS grid, children default to `min-height: auto` which prevents them from shrinking below content size. Setting `min-height: 0` on each grid child allows the grid to constrain their height, and `overflow-y: auto` enables scrolling within each panel. This is a well-established CSS grid pattern.

### 3. Network pages: make `.network-grid` fill its container and constrain column heights

**Rationale**: The network pages are rendered inside `#center-panel`. The center panel itself will already have a constrained height from the layout. The `.network-page` and `.network-grid` just need to fill that height (`height: 100%` or flex/grid fill) and each `.panel` within needs `overflow-y: auto` + `min-height: 0`.

### 4. Apply only at desktop breakpoint

**Rationale**: On mobile (`max-width: 1023px`), panels stack vertically and the user expects to scroll the page. The height-locking and independent scroll only apply above this breakpoint, preserving existing mobile behavior.

## Risks / Trade-offs

- **[Risk] Content that expects document-level scroll position** → No known features rely on `window.scrollY`; keyboard navigation and deep-link scrolling use `element.scrollIntoView()` which works within overflow containers.
- **[Risk] Drag-and-drop near panel edges** → SortableJS auto-scroll should work within `overflow-y: auto` containers. May need testing.
- **[Trade-off] `100vh` on mobile browsers** → The `100vh` value can be taller than the visual viewport on mobile due to browser chrome. However, mobile uses the stacked layout with normal document scroll, so this only affects desktop where it's reliable.
