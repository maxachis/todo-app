## Why

The drag-and-drop zones use svelte-dnd-action's default `dropTargetStyle`, which applies a bright yellow outline (`rgba(255, 255, 102, 0.7) solid 2px`). This clashes with the app's warm brown/earth-tone design system and looks out of place in both light and dark themes.

## What Changes

- Override svelte-dnd-action's default `dropTargetStyle` in all drag-and-drop zones to use the app's existing `--accent` color instead of bright yellow
- Affects: DragContainer, ListSidebar, SectionList, and PinnedSection — every component that calls `use:dndzone` or `use:dragHandleZone`

## Non-goals

- No changes to the custom drop indicators in TaskRow (the `drop-before` / `drop-nest` box-shadows already use `--accent`)
- No changes to drag ghost styling or animation behavior

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `drag-drop-subtask-nesting`: Visual feedback during drag should use the app's accent color instead of the library default

## Impact

- **Frontend only**: 4 Svelte components that invoke svelte-dnd-action directives
- No API or backend changes
- No dependency changes — `dropTargetStyle` is an existing configuration option in svelte-dnd-action
