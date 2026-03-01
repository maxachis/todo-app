## Context

The graph page filter sidebar (`frontend/src/routes/network/graph/+page.svelte`) renders filter checkboxes inside a `.card > .stack` container. Each filter is a `<label>` wrapping an `<input type="checkbox">` and text. The current CSS for `label` uses `display: grid` with `gap: 0.25rem` but no `grid-template-columns`, causing the checkbox and text to stack vertically — checkbox on top, label text below. This makes it unclear which checkbox belongs to which label.

## Goals / Non-Goals

**Goals:**
- Align each checkbox inline with its label text (horizontal layout)
- Maintain existing spacing between filter rows

**Non-Goals:**
- Changing filter behavior or state management
- Redesigning the sidebar layout or card structure
- Modifying other label styles outside the graph page (these are scoped styles)

## Decisions

**Inline layout via `grid-template-columns: auto 1fr`**: Change the `label` rule to use `grid-template-columns: auto 1fr` so the checkbox takes its natural width and the label text fills the remaining space, with `align-items: center` for vertical centering.

- *Alternative: `display: flex`* — Would also work, but grid is already used and `grid-template-columns` gives more explicit control. The `.depth-toggle label` already uses flex with the same pattern, confirming this approach works.
- *Alternative: Wrapping in extra elements* — Unnecessary; the existing `<label><input>text</label>` structure works fine with the right grid properties.

## Risks / Trade-offs

- **[Low]** Other `<label>` elements on the graph page (e.g., range inputs, text inputs) also match this rule → These labels have different content (text + input), but the `auto 1fr` columns still work correctly since the first child takes its natural width. The `.depth-toggle label` override already uses flex and won't be affected.
