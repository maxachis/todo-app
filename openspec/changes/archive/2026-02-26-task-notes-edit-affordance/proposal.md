## Why

The task detail Notes field renders markdown by default, which makes it look like static read-only content. There is no visible indication that clicking a rendered block will switch it to an editable textarea. Users may not discover the editing capability without trial and error. A subtle visual affordance would improve discoverability without cluttering the UI.

## What Changes

- Add an "edit" pencil icon or similar indicator to the Notes section header that signals the content is editable
- Add a subtle placeholder/empty-state prompt (e.g., "Click to add notes...") when the notes field is empty, reinforcing that it accepts input
- Enhance hover state on rendered markdown blocks to more clearly communicate interactivity (e.g., slightly more prominent border or a small edit icon overlay)
- Keep changes purely cosmetic/UX — no changes to the data model, API, or editing mechanics

## Capabilities

### New Capabilities

_(none — this is a UX enhancement to an existing capability)_

### Modified Capabilities

- `svelte-frontend`: Adding visual edit affordance to the Live Markdown editor requirement (Notes section header hint, empty-state placeholder, enhanced hover cues on rendered blocks)

## Impact

- **Frontend only**: `MarkdownEditor.svelte` (hover/empty-state styling), `TaskDetail.svelte` (notes section header indicator)
- No backend, API, or data model changes
- No new dependencies
