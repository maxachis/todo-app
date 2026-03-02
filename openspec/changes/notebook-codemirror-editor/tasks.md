## 1. Dependencies & Module Scaffolding

- [ ] 1.1 Install CM6 npm packages: `@codemirror/view`, `@codemirror/state`, `@codemirror/lang-markdown`, `@codemirror/language`, `@codemirror/commands`, `@codemirror/autocomplete`, `@lezer/highlight` in `frontend/`
- [ ] 1.2 Create module directory `frontend/src/lib/components/notebook/` and scaffold empty files: `createEditor.ts`, `theme.ts`, `livePreview.ts`, `mentionWidgets.ts`, `checkboxWidgets.ts`, `mentionCompletion.ts`, `listKeymap.ts`

## 2. CM6 Theme & Base Editor

- [ ] 2.1 Implement `theme.ts`: CM6 `EditorView.theme()` referencing CSS variables (`--bg-input`, `--text-primary`, `--border-light`, `--border-focus`, `--accent`, `--accent-light`, `--tag-bg`). Include styles for `.cm-editor`, `.cm-content`, `.cm-cursor`, `.cm-selectionBackground`, `.cm-focused`. Match current textarea font family (`var(--font-body)`), font size (0.9rem), and line height (1.7)
- [ ] 2.2 Implement `createEditor.ts`: Factory function that accepts a container element, initial content string, and callbacks (onChange, onBlur). Assembles extensions: markdown language, theme, keymap (defaultKeymap + history), update listener that calls onChange on doc changes, focusout handler that calls onBlur. Returns the EditorView instance plus a `setContent(text)` helper for page switching

## 3. Live Preview Decorations

- [ ] 3.1 Implement `livePreview.ts`: ViewPlugin that iterates the markdown syntax tree (`syntaxTree(state).iterate()`) and builds `DecorationSet` for non-active lines. Handle heading nodes — `Decoration.replace` on `ATXHeading1..6` markers (e.g., `# `, `## `), `Decoration.mark` with `.cm-heading-N` class on heading text
- [ ] 3.2 Add bold/italic decorations: `Decoration.replace` on `StrongEmphasis` / `Emphasis` delimiter nodes (`**`, `*`), `Decoration.mark` with `.cm-bold` / `.cm-italic` on content between delimiters
- [ ] 3.3 Add inline code decorations: `Decoration.replace` on `InlineCode` backtick delimiters, `Decoration.mark` with `.cm-inline-code` on code text
- [ ] 3.4 Add link decorations: For `Link` nodes, `Decoration.replace` on `](url)` portion, `Decoration.mark` with `.cm-link` on link text
- [ ] 3.5 Add bullet list decorations: For `ListItem` with `ListMark` (`- `), `Decoration.replace` the `- ` with a widget showing `•`
- [ ] 3.6 Add horizontal rule decorations: For `HorizontalRule` nodes (`---`), `Decoration.replace` with a widget rendering a styled `<hr>` element
- [ ] 3.7 Add code block decorations: For `FencedCode` nodes, `Decoration.mark` with `.cm-code-block` class on the full block. On non-active lines, hide the fence markers (`` ``` ``)
- [ ] 3.8 Add blockquote decorations: For `Blockquote` nodes, `Decoration.mark` with `.cm-blockquote` class (left border + indentation). On non-active lines, hide the `> ` prefix

## 4. Checkbox Widgets

- [ ] 4.1 Implement `checkboxWidgets.ts`: ViewPlugin that scans for `TaskMarker` nodes within `ListItem` nodes in the syntax tree. On non-active lines, replace `- [ ] ` and `- [x] ` with a `WidgetType` subclass rendering `<input type="checkbox">` (checked/unchecked)
- [ ] 4.2 Add click handler to checkbox widget: On click, dispatch a CM6 transaction that replaces `[ ]` with `[x]` or vice versa at the corresponding character offsets in the document

## 5. Entity Mention Widgets

- [ ] 5.1 Implement `mentionWidgets.ts`: ViewPlugin that uses regex to find `@[person:ID|Label]` and `[[type:ID|Label]]` patterns in the document text. Replace each match with a `WidgetType` subclass rendering a `<span class="cm-mention-chip">` with type badge emoji and label text
- [ ] 5.2 Style mention chips in `theme.ts`: `.cm-mention-chip` with `background: var(--accent-light)`, border-radius, padding, inline display. Distinct badge styling for each type (person 👤, task ✓, page 📄, org 🏢, project 📋)
- [ ] 5.3 Ensure mention widgets render on ALL lines (including the active/cursor line) — they are always-rendered, unlike markdown decorations

## 6. Mention Autocomplete

- [ ] 6.1 Implement `mentionCompletion.ts`: Two `CompletionSource` functions — `personCompletion` triggered by `@` + word chars (regex: `/(?:^|[\s(])@([a-zA-Z]*)$/`), `entityCompletion` triggered by `[[` + chars (regex: `/\[\[([^\]]*)$/`). Accept data arrays (people, pages, tasks, orgs, projects) as parameters
- [ ] 6.2 Person completion: Filter people by name match on query, return `Completion` objects that insert `@[person:ID|First Last]`, with `displayLabel` showing `👤 First Last`. Max 8 results
- [ ] 6.3 Entity completion: Filter across pages, tasks, orgs, projects by name/title match. Return `Completion` objects with type-appropriate insertion (`[[type:ID|Label]]`), `displayLabel` with type badge. Max 12 results
- [ ] 6.4 Style the autocomplete dropdown via CM6 theme: `.cm-tooltip-autocomplete` styled to match existing typeahead dropdown (background, border, shadow, font matching current app styles)

## 7. List Keymap

- [ ] 7.1 Implement `listKeymap.ts`: Custom keymap with Tab → indent current line by 2 spaces (when on a list item line), Shift+Tab → dedent by 2 spaces (remove up to 2 leading spaces)
- [ ] 7.2 Add Enter key handler: When cursor is at the end of a line matching `^(\s*)- (.+)$`, insert newline + captured indentation + `- `. When cursor is on a line matching `^(\s*)- $` (empty list item), remove the `- ` and insert a blank line

## 8. Svelte Integration & Page Wiring

- [ ] 8.1 Update `routes/notebook/+page.svelte`: Replace `<textarea>` and all typeahead-related state/logic (~140 lines) with a `<div bind:this={editorContainer}>` and CM6 lifecycle. On `onMount`, call `createEditor()` with container, content, onChange (sets contentDraft + debounced save), onBlur (immediate save). On cleanup, destroy the EditorView
- [ ] 8.2 Wire page switching: When `currentPage` changes (user clicks a different page in sidebar), call the editor's `setContent()` method to replace the document via CM6 transaction
- [ ] 8.3 Pass entity data arrays (allPeople, allTasks, allOrgs, allProjects, pages) into the editor's autocomplete extensions. Since data loads on mount, pass them at editor creation time
- [ ] 8.4 Implement content rewrite handling: After save, compare server-returned content with the document snapshot that was sent. If different and the current document still matches the sent snapshot, apply a line-level diff as a CM6 transaction. If the document has changed since the save was sent, skip the patch
- [ ] 8.5 Remove old typeahead-related code: `textareaEl`, `typeaheadOpen`, `typeaheadType`, `typeaheadQuery`, `typeaheadStart`, `typeaheadIndex`, `typeaheadPosition`, `getCaretCoords()`, `checkTypeahead()`, `selectTypeaheadItem()`, `handleTextareaKeydown()`, and the typeahead dropdown HTML/CSS
- [ ] 8.6 Remove old `.editor-textarea` CSS styles, add `.editor-cm-container` styles for the CM6 mount point (flex: 1, min-height, border, border-radius matching previous textarea)

## 9. Verification & Polish

- [ ] 9.1 Verify dark mode: Toggle theme and confirm CM6 editor updates colors via CSS variables without re-initialization
- [ ] 9.2 Verify checkbox-to-task flow: Type `- [ ] New task`, wait for save, confirm editor content is patched to `- [ ] [[task:ID|New task]]` with mention chip rendering and cursor preserved
- [ ] 9.3 Verify mention autocomplete: Test `@` and `[[` triggers, selection, chip rendering, and atomic deletion via Backspace
- [ ] 9.4 Verify list behavior: Tab/Shift-Tab indent/dedent, Enter continuation, Enter on empty item
- [ ] 9.5 Run `cd frontend && npm run check` to verify TypeScript compilation with new CM6 types
- [ ] 9.6 Run `cd frontend && npm run build` to verify production build succeeds and check bundle size impact
