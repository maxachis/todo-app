## Why

Several inline-edit input fields across the app are missing an explicit `background` CSS property, causing them to inherit browser-default styling. In dark mode, this creates nearly unreadable bright text on a bright (white) background. The fix ensures all editable inputs use the theme's `--bg-input` and `--text-primary` CSS variables for consistent, readable styling.

## What Changes

- Add `background: var(--bg-input)` to inline-edit inputs that currently lack it:
  - `.title-input` in TaskRow (inline task title editing)
  - `.name-input` in SectionHeader (section name editing)
  - `input` in ListItem (list name editing)
  - `.edit-input` in Projects page (project name editing)
  - `.block-editor` in MarkdownEditor (markdown editing textarea)
- Ensure all affected inputs also have `color: var(--text-primary)` for consistent text color

## Non-goals

- Redesigning the input field appearance or adding new focus ring styles
- Changing how the theme system works
- Modifying inputs that already have correct background/color properties (TaskDetail, TaskCreateForm, RecurrenceEditor, TypeaheadSelect)

## Capabilities

### New Capabilities

_None_ — this is a CSS bug fix, not a new capability.

### Modified Capabilities

- `dark-mode`: Input fields in inline-edit contexts must use theme CSS variables (`--bg-input`, `--text-primary`) for background and text color, ensuring readability in all theme modes.

## Impact

- **Frontend components**: TaskRow.svelte, SectionHeader.svelte, ListItem.svelte, MarkdownEditor.svelte, Projects +page.svelte
- **No API or backend changes**
- **No dependency changes**
- **Risk**: Minimal — additive CSS properties only, matching the pattern already used by correctly-styled inputs
