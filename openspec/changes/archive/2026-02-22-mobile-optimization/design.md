## Context

The app already has a mobile layout framework at the `@media (max-width: 1023px)` breakpoint: the three-panel task layout collapses to a single center panel, the sidebar becomes a hamburger toggle, the detail panel slides in as a fixed overlay, and a bottom tab bar replaces the top nav for page navigation. This structural work is solid.

However, within that mobile shell, individual components and pages were built for desktop-width viewports. On phone screens (375–430px), several layouts overflow horizontally, text is untruncated, touch targets are mouse-sized, and a few pages have grid/flex layouts that assume 600px+ of space. The existing CSS variable system and component-scoped styles make targeted fixes straightforward.

## Goals / Non-Goals

**Goals:**

- Every page and component renders without horizontal overflow on a 375px viewport
- All interactive elements (buttons, checkboxes, inputs, tags) meet 44px minimum touch target height
- Text-heavy elements truncate or wrap gracefully instead of overflowing
- The `100vh` layout works correctly with mobile browser chrome (URL bar resize)

**Non-Goals:**

- No tablet-specific breakpoints or optimizations
- No swipe gestures, pull-to-refresh, or mobile-native interaction patterns
- No page-level redesigns — existing layouts are preserved, just made to fit
- No JavaScript or Svelte logic changes — CSS only

## Decisions

### 1. Single additional breakpoint at 640px

**Decision**: Add `@media (max-width: 640px)` rules within each affected component's `<style>` block.

**Why over alternatives**:
- A single phone breakpoint keeps CSS simple (vs. adding 480px, 640px, 768px tiers)
- 640px captures all phone viewports while excluding tablets (which already work at the 1023px breakpoint)
- Component-scoped media queries (in Svelte `<style>`) over a global stylesheet — consistent with the existing pattern where each component owns its responsive behavior

### 2. Use `dvh` units for viewport height

**Decision**: Replace `100vh` with `100dvh` (dynamic viewport height) in the app shell, with `100vh` as fallback.

**Why**: On mobile browsers, `100vh` includes the area behind the URL bar, causing content to be hidden when the bar is visible. `dvh` adjusts dynamically as the browser chrome shows/hides. Fallback ensures older browsers still work.

### 3. Touch targets via min-height, not padding inflation

**Decision**: Apply `min-height: 44px` and `min-width: 44px` to interactive elements inside the 640px media query, rather than globally increasing padding.

**Why**: Inflating padding everywhere would change the visual density on desktop. `min-height` within a media query only affects phone viewports, preserving the compact desktop aesthetic. This also avoids cascading layout shifts.

### 4. SearchBar: fluid width with max-width cap

**Decision**: Change from `width: 220px` to `width: 100%; max-width: 220px` on the search input, and within the 640px query reduce `max-width` further or hide behind a toggle icon.

**Why**: The search bar competes with nav items for horizontal space. On phones, a full-width input below the nav or a magnifying glass icon that expands the input is more practical than a permanently visible 220px input. Since the proposal scopes this as CSS-only, a fluid width with a reduced max-width at 640px is the minimal fix.

### 5. Timesheet: flex-wrap stacking, not redesign

**Decision**: Add `flex-wrap: wrap` to the summary bar, entry form, and entry rows. Let flex items naturally stack when the viewport narrows.

**Why**: A minimal fix that prevents overflow. Each flex child gets `flex: 1 1 auto` with a `min-width` that triggers wrapping at phone widths. This preserves the existing layout on wider viewports while making it usable on phones.

### 6. TaskRow meta: allow wrapping

**Decision**: Remove `white-space: nowrap` from `.meta` at the 640px breakpoint and allow tags/due date/subtask count to wrap to a second line.

**Why over truncation**: Truncating metadata loses information. Wrapping to a second line within the task row preserves all info while fitting the viewport. The task title already truncates with ellipsis, which is the right behavior for titles.

### 7. Projects create form: stack vertically

**Decision**: Change `grid-template-columns: 1fr 1fr auto` to `grid-template-columns: 1fr` at 640px, stacking all form fields vertically.

**Why**: Three columns at 375px gives ~80px per field, which is unusable. Vertical stacking is the standard mobile form pattern.

## Risks / Trade-offs

- **Information density decreases on phones** → Acceptable trade-off; the alternative is unreadable/untappable UI. Users on phones expect less density.
- **Wrapping meta in TaskRow increases row height** → Rows may be taller on phones, requiring more scrolling. Mitigated by the fact that task titles are typically short enough to leave space.
- **`dvh` browser support** → Supported in all modern browsers (Chrome 108+, Safari 15.4+, Firefox 94+). The `vh` fallback handles older browsers gracefully.
- **No E2E test coverage for phone viewports** → The existing Playwright E2E suite doesn't test at phone widths. Visual regression on phones would be caught only by manual testing. Low risk given CSS-only changes behind media queries.
