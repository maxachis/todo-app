## Why

The app currently uses a fixed warm light color scheme with no way to adapt to user preference or ambient lighting. Adding dark mode reduces eye strain in low-light environments and respects OS-level appearance preferences via `prefers-color-scheme`.

## What Changes

- Add a dark color palette defined as CSS variable overrides on `:root`
- Support automatic theme switching based on `prefers-color-scheme` media query
- Add a manual light/dark/system toggle in the top navigation bar
- Persist the user's theme preference in `localStorage`
- Adjust shadows, borders, accent colors, and status colors for legibility on dark backgrounds
- Ensure pinned-task, tag, toast, and search-bar styling works in both themes

## Non-goals

- Per-list or per-project theme customization
- Custom user-defined color palettes beyond light and dark
- High-contrast / accessibility-specific themes (separate effort)
- Backend or API changes — this is purely frontend

## Capabilities

### New Capabilities
- `dark-mode`: Theme switching system including dark color palette, toggle UI, OS preference detection, and localStorage persistence

### Modified Capabilities
- `svelte-frontend`: The three-panel layout shell and top navigation bar gain a theme toggle control; all existing CSS variable consumers must render correctly under both light and dark variable sets

## Impact

- **CSS variables** in `+layout.svelte` `:root` — primary location for dark overrides
- **Top navigation bar** (`+layout.svelte`) — new toggle control added
- **All components using CSS variables** — visual verification needed but no code changes expected if variables are used consistently
- **Components with hardcoded colors** — any inline `color`, `background`, `border`, `box-shadow` values outside the variable system will need migration
- **E2E tests** — may need screenshot baselines updated if visual regression tests exist
- **No backend changes** — theme state lives entirely in the browser
- **No new dependencies** — implementable with CSS media queries and a small Svelte store
