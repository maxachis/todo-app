## Why

The graph filter checkboxes currently render with the checkbox underneath and centered relative to the label text, making it hard to visually associate which checkbox belongs to which label. Aligning them inline (checkbox beside label text) follows standard form conventions and improves usability.

## What Changes

- Update CSS for filter `<label>` elements in the graph page to use inline layout (checkbox and text side-by-side) instead of vertical grid stacking
- Ensure consistent alignment across all filter checkboxes in the Filters card

## Capabilities

### New Capabilities

_None — this is a CSS-only fix to existing UI._

### Modified Capabilities

_None — no spec-level behavior changes, only visual alignment._

## Non-goals

- Redesigning the overall graph sidebar layout
- Changing filter functionality or behavior
- Modifying checkbox styles beyond alignment

## Impact

- **Code**: `frontend/src/routes/network/graph/+page.svelte` — `label` and `.stack` CSS rules within the `<style>` block
- **Risk**: Minimal — CSS-only change scoped to graph page styles
