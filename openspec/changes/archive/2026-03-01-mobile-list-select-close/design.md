## Context

The Tasks page uses a three-panel layout. On mobile (≤1023px), the sidebar is hidden and shown as an overlay controlled by `sidebarOpen` state in `+layout.svelte`. List selection is handled by `selectList()` from the lists store, called via `ListItem.svelte → ListSidebar.svelte`. Currently, selecting a list updates the store but does not close the sidebar overlay, requiring an extra tap.

## Goals / Non-Goals

**Goals:**
- Auto-close the sidebar overlay when a list is selected on mobile

**Non-Goals:**
- Changing sidebar animation or timing
- Adding gesture-based dismissal
- Modifying desktop layout behavior

## Decisions

### Use `$effect` watching `selectedListStore` to close sidebar

**Approach**: Add an `$effect` in `+layout.svelte` that watches `$selectedListStore` and sets `sidebarOpen = false` when the value changes (and viewport is mobile-width).

**Alternatives considered:**
1. **Pass `onSidebarClose` callback through ListSidebar → ListItem**: Requires prop drilling and couples sidebar UI state to list components. More invasive.
2. **Create a shared `sidebarOpen` store**: Over-engineering for a single boolean that only `+layout.svelte` owns.
3. **Close unconditionally (no viewport check)**: On desktop, `sidebarOpen` is irrelevant (sidebar is always shown via grid), so an unconditional close is also safe. Simpler, and no risk of stale `innerWidth` issues.

**Decision**: Use an unconditional `$effect` — when `selectedListStore` changes, set `sidebarOpen = false`. On desktop the sidebar is always visible via CSS grid regardless of `sidebarOpen`, so this is a no-op.

## Risks / Trade-offs

- **Risk**: Effect fires on initial load when `selectedListStore` is first set → **Mitigation**: On initial load, `sidebarOpen` is already `false`, so setting it `false` again is a no-op.
- **Risk**: Creating a new list also triggers `selectList` → **Mitigation**: Closing the sidebar after creating a list is actually desirable behavior — user wants to see their new list's tasks.
