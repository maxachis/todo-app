## Context

The Relationships page uses a nested CSS Grid layout:
1. `.network-page` — `grid-template-rows: auto 1fr` gives the grid area all remaining viewport height
2. `.network-grid` — `display: grid` with no row constraints, so panels stretch to fill
3. `.panel` — `display: grid; gap: 0.75rem` with no `align-content`, so rows (h2, form, list) stretch evenly to fill the panel height

When the panel is taller than its content (few relationships, tall viewport), the extra space is distributed across the grid rows, producing large gaps between the heading, each form input, and the list.

## Goals / Non-Goals

**Goals:**
- Panel content packs at the top; extra space appears below the content, not between rows

**Non-Goals:**
- Changing any spacing values or visual design

## Decisions

### Add `align-content: start` to `.panel`

**Choice**: Add `align-content: start` to the `.panel` CSS rule.

**Rationale**: This tells the grid to pack rows at the start, leaving any extra space at the bottom. The existing `gap: 0.75rem` between rows and `overflow-y: auto` scrolling continue to work correctly. Single property change, zero side effects.

**Alternative considered**: Adding explicit `grid-template-rows` — rejected as more complex and brittle.

## Risks / Trade-offs

None. This is a purely additive CSS property that resolves the stretching behavior without affecting any other layout aspect.
