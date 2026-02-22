## Context

The Task view uses a CSS Grid three-panel layout defined in `+layout.svelte` with fixed column widths: `300px 1fr 320px` (sidebar, center, detail). All panels share the same `<main class="panels">` grid container. On mobile (<1024px), the layout collapses to a single column — the sidebar hides behind a hamburger, and the detail panel slides in as an overlay.

Users cannot adjust how much screen space each panel occupies. This is limiting on larger monitors where the center panel dominates, or when a user wants more room for the markdown editor in the detail panel.

## Goals / Non-Goals

**Goals:**
- Allow users to drag resize handles between panels to adjust widths
- Persist chosen widths across page reloads via localStorage
- Maintain minimum widths so panels remain functional
- Keep the existing mobile responsive behavior unchanged

**Non-Goals:**
- Panel collapse/hide (zero-width toggle)
- Resizing on non-Tasks routes (single-panel layout)
- Vertical resizing
- Server-side persistence of panel widths

## Decisions

### 1. Svelte action vs. standalone component for resize handles

**Decision**: Create a `ResizeHandle.svelte` component.

**Rationale**: A component is more natural here because resize handles are visible DOM elements with their own styling, hover states, and cursor feedback. A Svelte action (`use:resize`) is better for invisible behavior on existing elements. Since we need to render a distinct `<div>` between panels with its own visual treatment, a component is the right abstraction.

**Alternative considered**: A Svelte action on the panel elements that injects a pseudo-element. Rejected because pseudo-elements can't receive pointer events reliably across browsers, and the logic for tracking drag state is cleaner in a component.

### 2. Pointer event tracking approach

**Decision**: Use `pointerdown` on the handle, then `pointermove`/`pointerup` on `window` with `setPointerCapture`.

**Rationale**: Pointer capture ensures drag continues even if the cursor leaves the handle element. This is the standard pattern for drag interactions and works across mouse and touch. Using `window`-level listeners avoids missed events when the cursor moves fast.

**Alternative considered**: Mouse events only. Rejected because pointer events unify mouse/touch and pointer capture is cleaner than manual `window` listener add/remove.

### 3. Grid column sizing strategy

**Decision**: Replace the fixed `grid-template-columns: 300px 1fr 320px` with inline style using pixel values for sidebar and detail, and `1fr` for center. During drag, update the grid template via a reactive variable. The handle widths (e.g., 6px each) are included as explicit grid columns.

**Rationale**: CSS Grid naturally handles the center panel as flexible space via `1fr`. Only the sidebar and detail panel widths need to be stored. The grid template becomes: `{sidebarWidth}px 6px 1fr 6px {detailWidth}px`.

**Alternative considered**: Using `flex` layout with explicit widths on all three panels. Rejected because the existing layout is grid-based and switching to flex would be a larger change with no benefit.

### 4. Persistence strategy

**Decision**: Store `{ sidebarWidth: number, detailWidth: number }` in `localStorage` under key `panel-widths`. Read on mount, write on drag end (not during drag).

**Rationale**: Writing on drag end avoids excessive localStorage writes during dragging. Only two values need storing — the center panel is always `1fr`. A single localStorage key keeps it simple.

### 5. Minimum and maximum width constraints

**Decision**: Enforce minimum widths during drag: sidebar 180px, detail 220px. The center panel's minimum is implicitly enforced — if dragging would shrink the center below 200px, the drag is clamped. No maximum widths — the viewport naturally constrains.

**Rationale**: Minimums prevent panels from becoming too narrow to show content (sidebar needs room for list names, detail needs room for form fields). The center panel minimum ensures the task list remains readable.

### 6. Handle visual design

**Decision**: A 6px-wide transparent hit area with a 2px visible line centered within it. On hover, the line becomes the accent color and the cursor changes to `col-resize`. During active drag, the line stays highlighted.

**Rationale**: Subtle by default, discoverable on hover. The wider hit area (6px) makes it easy to grab without taking visible space. This matches common patterns in VS Code, Figma, and similar tools.

## Risks / Trade-offs

- **[Risk] Drag interaction conflicts with existing drag-and-drop (svelte-dnd-action)** → Mitigation: Resize handles use `pointerdown` with `stopPropagation()` and `setPointerCapture`, which prevents the event from reaching dnd-action listeners. The handles are separate DOM elements outside the dnd containers.

- **[Risk] Performance during fast dragging** → Mitigation: Grid template updates are a single style property change per frame. Using `requestAnimationFrame` throttling if needed, but modern browsers handle this efficiently.

- **[Risk] Saved widths become invalid on window resize** → Mitigation: On mount and window resize, clamp stored widths to respect minimums and ensure they fit within the current viewport. If stored widths exceed available space, reset to defaults.

- **[Trade-off] No persistence across devices** → Accepted. localStorage is per-browser. Server-side persistence would require a user preferences API, which is over-engineering for a single-user app.
