## Why

The notebook editor has rich special syntax for mentions, entity links, checkboxes, and contact drafts, but none of it is documented in the UI. Users have to know the triggers (`@`, `[[`, `- [ ]`, `@new[`) by memory. The existing `ShortcutHints` component on the Notebook page only shows `Ctrl+\` — it should also surface these typing prompts.

## What Changes

- Expand the Notebook page's `ShortcutHints` shortcuts list to include special typing syntax triggers alongside the existing keyboard shortcut
- Group hints into "Shortcuts" and "Syntax" sections within the popover so they're visually distinct
- Update the `ShortcutHints` component to support optional section grouping

## Non-goals

- Changing any notebook editor behavior
- Adding hints for Markdown formatting (bold, italic, etc.) — these are standard and widely known

## Capabilities

### New Capabilities
<!-- None — this extends the existing shortcut-hints capability -->

### Modified Capabilities
- `shortcut-hints`: Add support for grouped hint sections (shortcuts vs. syntax) and include notebook typing prompts

## Impact

- Modified component: `frontend/src/lib/components/shared/ShortcutHints.svelte` (add section grouping support)
- Modified page: `frontend/src/routes/notebook/+page.svelte` (expanded hints data)
- No API or backend changes
