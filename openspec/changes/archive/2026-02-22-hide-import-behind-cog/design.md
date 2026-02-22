## Context

The app's top navigation bar currently lists all page routes as flat tabs, including Import. As more utility pages are added, the tab bar becomes crowded. Import is an infrequent action used only occasionally, unlike daily-driver tabs like Tasks, Projects, and Timesheet.

The navbar already has a theme toggle button in the top-right area. A cog/settings button can sit alongside it, providing a natural home for utility actions.

## Goals / Non-Goals

**Goals:**
- Remove Import from the primary tab list (both desktop nav and mobile bottom tabs)
- Add a cog icon button next to the theme toggle
- Cog button opens a dropdown menu with an "Import" link
- Dropdown closes on outside click, Escape key, or navigation
- Consistent styling with the existing theme toggle button

**Non-Goals:**
- No new settings page or configuration UI
- No changes to the Import page itself or its route
- No backend changes
- No restructuring of other navigation tabs

## Decisions

### Inline dropdown in +layout.svelte vs. separate component

**Decision**: Implement the dropdown directly in `+layout.svelte`.

**Rationale**: The dropdown is small (a button + a positioned menu with one link). Extracting a separate component adds indirection for minimal benefit. If more menu items are added later, it can be extracted then.

**Alternative considered**: A `SettingsMenu.svelte` component — rejected as premature abstraction for a single menu item.

### Cog icon implementation

**Decision**: Use the Unicode gear character `\u2699\uFE0F` for the cog icon, matching the existing emoji-based approach used by the theme toggle (`\u2600\uFE0F`, `\uD83C\uDF19`, `\uD83D\uDCBB`).

**Alternative considered**: SVG icon — rejected to stay consistent with the existing icon style in the navbar.

### Dropdown positioning

**Decision**: Position the dropdown with `position: absolute` relative to a wrapper `div` around the cog button, anchored to the right edge. The menu appears below the button.

**Rationale**: Simple CSS positioning is sufficient. No need for a positioning library (Floating UI, etc.) since the button is in a fixed location in the top-right of the nav bar with no overflow concerns.

### Mobile behavior

**Decision**: On mobile, also remove Import from the bottom tab bar and include it in the cog dropdown. The cog button is visible in the top nav on all viewports.

**Rationale**: Keeps the experience consistent across breakpoints. The cog button is already in the top nav which is visible on mobile.

## Risks / Trade-offs

- **Discoverability**: Import is now one click further away (cog → Import). → Acceptable since Import is infrequent; the cog icon is a universal "settings" affordance.
- **Future menu items**: If many items are added to the cog dropdown, it may need restructuring. → Current scope is just Import; cross that bridge later.
