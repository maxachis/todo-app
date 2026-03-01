## Context

All drag-and-drop zones in the app use svelte-dnd-action (`dndzone` / `dragHandleZone` directives). The library applies a default `dropTargetStyle` of `outline: "rgba(255, 255, 102, 0.7) solid 2px"` — a bright yellow outline — to any zone that is an active drop target. The app's design system uses warm brown/earth tones (`--accent: #b45828` light, `--accent: #d4753e` dark) and currently does not override this default.

Five call sites invoke svelte-dnd-action directives:
1. `DragContainer.svelte` — `use:dndzone` and `use:dragHandleZone` (generic wrapper)
2. `ListSidebar.svelte` — `use:dndzone` (list reordering)
3. `SectionList.svelte` — `use:dragHandleZone` (section reordering)
4. `PinnedSection.svelte` — `use:dndzone` (pinned task reordering)

TaskRow's custom `drop-before` / `drop-nest` indicators already use `var(--accent)` and are unaffected.

## Goals / Non-Goals

**Goals:**
- Replace the bright yellow drop-target outline with the app's accent color in all drag-and-drop zones
- Respect light/dark theme automatically

**Non-Goals:**
- Changing the outline width or style (keep `solid 2px`)
- Modifying TaskRow's custom drop indicators (already themed)
- Adding new CSS variables — reuse existing `--accent`

## Decisions

### Use `dropTargetStyle` option with an inline accent color

svelte-dnd-action accepts a `dropTargetStyle` config object that overrides the default. Pass `{ outline: "rgba(180, 88, 40, 0.7) solid 2px" }` to match `--accent` (#b45828 = rgb(180, 88, 40)).

**Why not use CSS variable in the style object?** `dropTargetStyle` is applied via JavaScript `element.style`, which doesn't resolve `var(--accent)` in the object literal. We must use a concrete color value.

**Why not use `dropTargetClasses` instead?** While `dropTargetClasses` could apply a CSS class with `outline: 2px solid var(--accent)`, it requires coordinating a global CSS class definition. The inline style approach is simpler and self-contained for each component.

### Centralize the style constant

Define a shared `DROP_TARGET_STYLE` constant (e.g., in a small util or directly in DragContainer) so all call sites reference the same value. For the 3 components that call svelte-dnd-action directly (not via DragContainer), import or duplicate the same object.

### Use the light-mode accent as the single color value

`rgba(180, 88, 40, 0.7)` (derived from light-mode `--accent: #b45828`) provides good visibility in both light and dark themes. The warm brown outline is visible on light backgrounds and has sufficient contrast on dark backgrounds. This avoids needing JS-level theme detection.

## Risks / Trade-offs

- **Hardcoded color value**: The outline color won't automatically update if `--accent` changes in CSS. → Acceptable since the accent color is stable and the risk is minimal for a single-user app.
- **Single color for both themes**: The light-mode accent at 0.7 opacity may be slightly less visible on dark backgrounds than on light. → The dark-mode accent (#d4753e) is lighter, but testing shows the light-mode value is still clearly visible on dark backgrounds. If needed, JS theme detection could be added later.
