## Context

The notebook editor in `routes/notebook/+page.svelte` uses a plain `<textarea>` for content editing. It has ~140 lines of custom typeahead logic for `@` (people) and `[[` (entity) mentions, using regex matching, caret coordinate calculation, and a manually positioned dropdown. The `inbox-and-note-tasks` change added checkbox-to-task creation (`- [ ] text` → `- [ ] [[task:ID|Title]]`) with server-side content rewriting on save.

Content is stored as plain markdown text in a Django `TextField`. The backend `reconcile_mentions` function parses content on save for entity references and (since inbox-and-note-tasks) creates tasks from checkbox syntax. The save response returns the potentially-rewritten content which the frontend syncs back into the editor.

The app uses CSS variables for theming (`--text-primary`, `--bg-input`, `--accent`, etc.) with light/dark mode support.

## Goals / Non-Goals

**Goals:**
- Replace textarea with CM6 providing Obsidian-style live preview of markdown
- Render checkboxes as clickable widgets, entity mentions as styled chips
- Maintain full compatibility with existing mention syntax and server-side content rewriting
- Integrate with existing CSS variable theme system for seamless dark mode

**Non-Goals:**
- Node-level cursor reveal (start with line-level: entire active line shows raw markdown)
- Formatting toolbar or buttons
- Slash commands
- Changing backend storage format or mention syntax

## Decisions

### 1. Module structure: Extract CM6 setup into `lib/components/notebook/`

**Decision**: Create dedicated modules rather than inlining everything in +page.svelte:

```
lib/components/notebook/
  createEditor.ts        # EditorView factory, extensions assembly
  theme.ts               # CM6 theme using CSS variables
  livePreview.ts         # ViewPlugin for markdown decorations
  mentionWidgets.ts      # ViewPlugin for @[person:] and [[entity:]] rendering
  checkboxWidgets.ts     # ViewPlugin for [ ] / [x] checkbox rendering
  mentionCompletion.ts   # CompletionSource for @ and [[ autocomplete
  listKeymap.ts          # Tab indent, Shift-Tab dedent, Enter list continuation
```

**Why over alternatives**:
- *All-in-one in +page.svelte*: The textarea approach was ~140 lines and already complex. CM6 extensions will be substantially more code — keeping it in one file would be unmanageable.
- *Svelte components wrapping CM6*: CM6 manages its own DOM — wrapping it in a Svelte component adds indirection with no benefit. Better to use plain `.ts` modules that export CM6 extensions and call them from the Svelte mount lifecycle.

### 2. Line-level live preview via ViewPlugin + Decorations

**Decision**: A single `ViewPlugin` (`livePreview.ts`) walks the markdown syntax tree from `@codemirror/lang-markdown` and generates `Decoration.replace` and `Decoration.mark` decorations for syntax nodes not on the cursor's current line. When the cursor moves, decorations are recalculated.

**How it works**:
1. On each view update (cursor move, doc change), get the line number(s) containing the selection
2. Iterate the markdown syntax tree via `syntaxTree(state).iterate()`
3. For each node (heading marker, emphasis delimiters, bullet markers, etc.), check if it overlaps an active line
4. If NOT on an active line: apply decorations — hide syntax markers (`#`, `**`, `*`, `` ` ``), apply styling classes (`.cm-heading-1`, `.cm-bold`, etc.)
5. If ON the active line: skip decorations, show raw markdown

**Why line-level over node-level**: Line-level is a single check (`node.from` to line number comparison). Node-level requires tracking the exact cursor position relative to each syntax node and handling edge cases (cursor between `**` and text, multi-line nodes). Line-level is Obsidian's V1 approach and is well-understood.

**Decoration types by element**:

| Element | Decoration | Effect |
|---------|------------|--------|
| `# Heading` | `Decoration.replace` on `#` + space; `Decoration.mark` with class on text | Hides marker, styles text |
| `**bold**` | `Decoration.replace` on `**` delimiters; `Decoration.mark` with class on text | Hides markers, bolds text |
| `*italic*` | `Decoration.replace` on `*` delimiters; `Decoration.mark` with class on text | Hides markers, italicizes text |
| `` `code` `` | `Decoration.replace` on backticks; `Decoration.mark` with class on text | Hides markers, mono + bg |
| `[text](url)` | `Decoration.replace` on `](url)`; `Decoration.mark` with class on text | Hides URL, colors text |
| `- item` | `Decoration.replace` on `- ` with bullet widget `•` | Shows bullet character |
| `---` | `Decoration.replace` with horizontal rule widget | Shows styled `<hr>` |
| Code blocks | `Decoration.mark` on fenced block with class | Background styling |

### 3. Checkbox rendering via widget decorations

**Decision**: A `ViewPlugin` (`checkboxWidgets.ts`) scans for `- [ ] ` and `- [x] ` patterns using the syntax tree (ListItem → TaskMarker nodes). On non-active lines, it replaces `- [ ] ` / `- [x] ` with a `WidgetType` subclass that renders an `<input type="checkbox">` element. Clicking the checkbox dispatches a CM6 transaction that toggles `[ ]` ↔ `[x]` in the source.

**Why regex + syntax tree rather than pure syntax tree**: The markdown parser recognizes task list syntax as `TaskMarker` nodes inside `ListItem` nodes. However, the checkbox click handler needs to know the exact character offsets of `[ ]` / `[x]` to dispatch the replacement transaction, so we use the syntax tree for detection and character offsets for mutation.

**Active-line behavior**: On the active line, show raw `- [ ] ` / `- [x] ` to allow manual editing. On other lines, show the checkbox widget.

### 4. Entity mention widgets: always rendered, atomic

**Decision**: A separate `ViewPlugin` (`mentionWidgets.ts`) scans the document for `@[person:ID|Label]` and `[[type:ID|Label]]` patterns via regex (not the markdown syntax tree, since these are custom syntax). These are replaced with `WidgetType` widgets that render a styled `<span>` chip (type badge emoji + label text). Mention widgets are **always rendered**, even on the active line — the raw syntax is never useful to the user.

**Atomic deletion**: Mention widgets are rendered as CM6 `Decoration.replace` decorations spanning the full mention syntax. When the user presses Backspace at the position immediately after a mention widget, the entire mention is deleted (this is CM6's default behavior for replaced ranges — the cursor skips over them).

**Why always rendered**: Unlike standard markdown (where seeing `## ` helps you know the heading level), mention syntax (`@[person:7|John Smith]`) was machine-inserted via autocomplete and has no user-editable meaning. Showing raw syntax would be confusing. If the user wants to change a mention, they delete it and re-trigger autocomplete.

### 5. Mention autocomplete via `@codemirror/autocomplete`

**Decision**: Define two `CompletionSource` functions in `mentionCompletion.ts`:

1. **Person completion**: Triggers when the user types `@` followed by word characters. Queries the `allPeople` array, returns `Completion` objects that insert `@[person:ID|Label]`.
2. **Entity completion**: Triggers when the user types `[[`. Queries `pages`, `allTasks`, `allOrgs`, `allProjects` arrays, returns `Completion` objects with type badges that insert `[[type:ID|Label]]`.

The data arrays (`allPeople`, `allTasks`, etc.) are passed into the completion sources via CM6 compartments or by rebuilding the extension when data changes. Since entity data is loaded once on mount and rarely changes, a simple approach is to pass the arrays into `createEditor` and rebuild the autocomplete extension only when data reloads.

**Why CM6 autocomplete over custom dropdown**: The current custom typeahead is ~80 lines of caret coordinate calculation, dropdown positioning, keyboard interception, and focus management. CM6's `@codemirror/autocomplete` handles all of this natively with better edge-case handling (scroll, viewport boundaries, multi-line).

### 6. Content rewrite handling: diff-and-patch transactions

**Decision**: When the save response returns content that differs from the current CM6 document (due to server-side checkbox→task rewriting), apply the changes as a CM6 transaction using `dispatch({ changes })` rather than replacing the entire document.

**Approach**: Use a simple line-by-line diff:
1. Split current doc and server response into lines
2. Find lines that differ (the server only adds `[[task:ID|Title]]` inside existing lines)
3. Build a `ChangeSpec[]` array with targeted replacements
4. Dispatch a single transaction with all changes

**Why not full document replace**: `state.update({ changes: { from: 0, to: doc.length, insert: newContent } })` would reset cursor position and scroll state. Line-level diffing preserves both since only the modified lines are touched — and the cursor is unlikely to be on a line that just got rewritten (the save fires on a debounce, by which time the user has moved on).

**Edge case**: If the user has made further edits between the save request and response, the diff may conflict. In this case, skip the patch — the next debounced save will sync correctly. Detect this by comparing the doc the save was based on with the current doc.

### 7. Svelte integration: mount/destroy lifecycle

**Decision**: In `+page.svelte`, create the CM6 EditorView in an `onMount` callback, targeting a `<div bind:this={editorContainer}>` element. Destroy it in the returned cleanup function. When `currentPage` changes (user opens a different page), dispatch a full document replacement transaction rather than destroying/recreating the EditorView.

**State bridge**: The CM6 `updateListener` extension fires on every document change, updating a local `contentDraft` variable (used by the save function). This replaces the old `bind:value={contentDraft}` on the textarea.

**Blur handling**: CM6's `EditorView.focusChangeEffect` or a DOM `focusout` listener on the editor container triggers the save-on-blur behavior.

### 8. Theme: CM6 `EditorView.theme` with CSS variables

**Decision**: Define a CM6 theme in `theme.ts` using `EditorView.theme()` that references the app's CSS variables:

```
.cm-editor         → background: var(--bg-input), color: var(--text-primary)
.cm-cursor         → border-color: var(--text-primary)
.cm-selectionBackground → background: var(--accent-light)
.cm-heading-1      → font-size: 1.5em, font-weight: 700
.cm-heading-2      → font-size: 1.25em, font-weight: 700
.cm-heading-3      → font-size: 1.1em, font-weight: 600
.cm-bold           → font-weight: 700
.cm-italic         → font-style: italic
.cm-inline-code    → background: var(--tag-bg), font-family: monospace
.cm-link           → color: var(--accent)
.cm-mention-chip   → background: var(--accent-light), border-radius: 3px, padding: 0 4px
.cm-checkbox       → cursor: pointer, vertical-align: middle
```

Dark mode works automatically since CSS variables update based on the `data-theme` attribute.

## Risks / Trade-offs

- **[Bundle size]** → CM6 adds ~80-100KB gzipped. Acceptable for a desktop-first personal tool. The notebook route can use dynamic import to avoid loading CM6 on other pages.

- **[CM6 learning curve]** → The ViewPlugin + Decoration API is powerful but verbose. Each decoration type (heading, bold, list, etc.) requires specific syntax tree node matching. **Mitigation**: Well-structured modules with one concern each. The markdown syntax tree from `@lezer/markdown` is well-documented.

- **[Content rewrite race condition]** → If the user types during the 1s debounce window, the save fires with stale content, and the rewritten response may conflict with current editor state. **Mitigation**: Compare the document state at save-time with current state before applying patches. If they differ, skip the patch — the next save will reconcile.

- **[Custom mention syntax not in Lezer parser]** → `@[person:ID|Name]` and `[[type:ID|Name]]` aren't standard markdown. The Lezer markdown parser won't produce nodes for them. **Mitigation**: Mention widget plugin uses regex scanning independent of the syntax tree. This is the same approach the current textarea uses — robust and well-tested.

- **[Textarea behavior expectations]** → Users may expect textarea-like behavior (Cmd+A to select all, browser spellcheck). **Mitigation**: CM6 supports both natively. Spellcheck can be enabled via `EditorView.contentAttributes.of({ spellcheck: "true" })`.

## Open Questions

None — all decisions resolved during exploration.
