## Why

The task detail notes field uses a basic MarkdownEditor with per-block editing — click a block to get a plain textarea, blur to see rendered markdown. This feels disconnected: you're either writing raw markdown or viewing rendered output, never both. The notebook pages already have a CodeMirror 6 editor with live preview (headings, bold, italic, code, links, lists, checkboxes all render inline while editing). Bringing that same editing experience to task detail notes gives users consistent, rich markdown editing everywhere.

## Non-goals

- Adding @mention/linking features (those are notebook-specific)
- Changing the notebook editor
- Modifying the notes data model or API

## Capabilities

### New Capabilities

- `notes-codemirror-editor`: A CodeMirror 6 editor for task detail notes with live markdown preview, checkbox widgets, and list continuation keymaps. Reuses notebook editor modules (livePreview, checkboxWidgets, listKeymap, theme) without mentions or autocompletion. Blur commits the notes value via the existing auto-save mechanism.

### Modified Capabilities

(none — the old MarkdownEditor component stays available for other uses; we just stop using it in TaskDetail)

## Impact

- **New file**: `frontend/src/lib/components/shared/NotesEditor.svelte` — Svelte wrapper around a slim CodeMirror editor
- **Modified file**: `frontend/src/routes/+page.svelte` or `TaskDetail.svelte` — replace `<MarkdownEditor>` with `<NotesEditor>`
- **Reused modules**: `notebook/livePreview.ts`, `notebook/checkboxWidgets.ts`, `notebook/listKeymap.ts`, `notebook/theme.ts`
- **No new dependencies**: CodeMirror packages already installed
