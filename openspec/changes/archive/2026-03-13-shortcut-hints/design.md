## Context

The Tasks page has 9 keyboard shortcuts (navigation, completion, indent/outdent, section/list cycling) and the Notebook page has 1 (sidebar toggle). These are invisible to users — there's no UI affordance indicating they exist.

## Goals / Non-Goals

**Goals:**
- Make keyboard shortcuts discoverable via a visible UI element
- Reusable component that any page can adopt by passing a shortcut list
- Minimal visual footprint when not in use

**Non-Goals:**
- Keyboard trigger (`?` key) for the popover
- Remembering dismissed state across sessions
- Animating the popover

## Decisions

### 1. Single shared component with prop-driven content
The `ShortcutHints.svelte` component accepts a `shortcuts` array prop. Each page is responsible for defining its own shortcut list. This keeps the component generic and avoids a centralized shortcut registry.

**Alternative**: A global shortcut map keyed by route. Rejected — adds coupling and isn't needed for two pages.

### 2. Fixed position bottom-right with upward popover
The badge sits at `position: fixed; bottom: 1rem; right: 1rem` with a high z-index. The popover opens upward from the badge. This avoids interfering with page content and works consistently across the Tasks three-panel layout and the Notebook layout.

### 3. Click-outside to close via Svelte action or window listener
A `click` handler on `window` closes the popover when clicking outside. Simple and standard.

### 4. CSS variables for theming
Use existing CSS custom properties (`--bg`, `--text`, `--border`, etc.) so the component works in both light and dark mode without extra logic.

## Risks / Trade-offs

- [Badge overlaps content] → Fixed-position badge could overlap scrollable content in edge cases. Mitigated by small size (32-36px circle) and semi-transparent background on hover.
- [Z-index conflicts] → Use a z-index consistent with other overlays in the app.
