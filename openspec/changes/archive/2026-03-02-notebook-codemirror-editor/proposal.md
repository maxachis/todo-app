## Why

The notebook editor uses a plain `<textarea>` with no live formatting. Users must mentally parse markdown syntax while writing — `# Heading` stays as literal text, `- [ ]` shows raw brackets, `**bold**` shows asterisks. The recent `inbox-and-note-tasks` change made this worse by introducing `[[task:ID|Title]]` syntax that users now see as raw text in their notes. Modern note-taking apps like Obsidian render markdown inline as you type, and users expect the same here.

## What Changes

- **Replace the `<textarea>` with a CodeMirror 6 editor** providing Obsidian-style live preview — markdown syntax renders inline on non-active lines and reveals raw source when the cursor is on the line
- **Markdown live preview decorations**: Headings (h1-h6), bold, italic, inline code, code blocks, links, horizontal rules, and blockquotes render with proper styling; syntax markers hidden on non-active lines
- **List handling**: Bullet points render as `•` characters; Tab/Shift-Tab indents and dedents list items; Enter at end of list item continues the list with `- ` prefix
- **Checkbox widgets**: `- [ ]` and `- [x]` render as clickable checkbox input widgets; clicking toggles between checked/unchecked in the source text
- **Entity mention widgets**: `@[person:ID|Name]` and `[[type:ID|Name]]` render as styled inline chips (type badge + label), always visible even on the active line; backspace over a chip removes the whole mention
- **Mention autocomplete**: The existing `@` (people) and `[[` (entities) typeahead reimplemented as CM6 completion sources with the same data sources and matching logic
- **Content rewrite handling**: When the server returns rewritten content after save (checkbox-to-task link insertion from `inbox-and-note-tasks`), the CM6 document is patched via transaction to preserve cursor position
- **Theme integration**: CM6 theme references existing CSS variables so dark mode works seamlessly

## Non-goals

- Node-level cursor reveal (showing raw markdown only for the specific syntax node under cursor) — start with line-level reveal
- Toolbar or formatting buttons — keyboard/syntax-driven only, matching Obsidian's approach
- Slash commands (e.g., `/heading`, `/todo`)
- Collaborative editing or CRDT — single-user app
- Changing the backend storage format — content remains plain text markdown
- Bidirectional checkbox-task sync (already a non-goal from inbox-and-note-tasks)

## Capabilities

### New Capabilities
- `notebook-codemirror-editor`: CodeMirror 6-based markdown editor with live preview decorations, checkbox widgets, entity mention widgets, mention autocomplete, list indent/dedent, and CSS variable theme integration

### Modified Capabilities
- `notebook-core`: The editor area switches from `<textarea>` to a CM6 EditorView; save/blur/page-switch logic rewired through CM6 update listeners; content rewrite handling uses CM6 transactions for document patching

## Impact

- **Frontend**: `routes/notebook/+page.svelte` is the primary file changed — textarea replaced with CM6, ~140 lines of typeahead/keyboard logic replaced with CM6 extensions. New CM6 modules extracted into `lib/components/notebook/` for editor setup, decorations, completions, and theme.
- **Dependencies**: New npm packages — `@codemirror/view`, `@codemirror/state`, `@codemirror/lang-markdown`, `@codemirror/language`, `@codemirror/commands`, `@codemirror/autocomplete`, `@lezer/highlight`. Bundle size increase ~80-100KB gzipped.
- **Backend**: No changes. Content format unchanged.
- **Interaction with inbox-and-note-tasks**: Checkbox rendering and task-link widget rendering are first-class concerns. The content rewrite flow (server inserting `[[task:ID|Title]]` after save) must work with CM6's document model.
