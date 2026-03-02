# Notebook CodeMirror Editor

## Purpose

CodeMirror 6-based rich markdown editor for notebook pages, providing live preview, list/checkbox handling, entity mention widgets with autocomplete, and theme integration.

## Requirements

### Requirement: CodeMirror 6 editor replaces textarea for notebook content editing
The notebook page editor SHALL use a CodeMirror 6 `EditorView` instance instead of a plain `<textarea>` for content editing. The editor SHALL be mounted in a container `<div>` within the editor area of `routes/notebook/+page.svelte`. The editor SHALL support standard text editing operations (typing, selection, copy/paste, undo/redo, spellcheck). The CM6 editor setup, extensions, and configuration SHALL be organized in dedicated TypeScript modules under `lib/components/notebook/`.

#### Scenario: Editor renders for an open page
- **WHEN** a user opens a notebook page
- **THEN** a CodeMirror 6 editor is displayed in the editor area with the page content loaded

#### Scenario: Editor updates content on typing
- **WHEN** a user types text in the CM6 editor
- **THEN** the document content is updated and a debounced save is triggered after 1 second of inactivity

#### Scenario: Editor saves on blur
- **WHEN** the CM6 editor loses focus
- **THEN** the page content is saved immediately (cancelling any pending debounced save)

#### Scenario: Switching pages updates editor content
- **WHEN** a user switches from one notebook page to another
- **THEN** the CM6 editor document is replaced with the new page's content via a transaction (not by destroying/recreating the editor)

### Requirement: Markdown live preview with line-level cursor reveal
The CM6 editor SHALL render markdown formatting inline on lines where the cursor is NOT present. When the cursor is on a line, that line SHALL show raw markdown source. The following markdown elements SHALL be rendered:

- **Headings** (h1-h6): `#` markers hidden, text styled with increasing font size and weight
- **Bold**: `**` delimiters hidden, text rendered in bold
- **Italic**: `*` delimiters hidden, text rendered in italic
- **Inline code**: backtick delimiters hidden, text rendered in monospace with background
- **Code blocks**: fenced code blocks (`` ``` ``) rendered with background styling
- **Links**: `[text](url)` rendered as styled text with URL hidden
- **Horizontal rules**: `---` rendered as a visual horizontal line
- **Blockquotes**: `>` prefix styled with left border and indentation

#### Scenario: Heading renders on non-active line
- **WHEN** the editor contains `# My Title` on line 1 and the cursor is on line 3
- **THEN** line 1 displays "My Title" styled as a large bold heading with the `# ` marker hidden

#### Scenario: Heading reveals source on active line
- **WHEN** the user moves the cursor to a line containing `# My Title`
- **THEN** the line displays the raw `# My Title` text so the user can edit the markdown source

#### Scenario: Bold text renders on non-active line
- **WHEN** the editor contains `This is **important** text` and the cursor is on a different line
- **THEN** "important" is rendered in bold with the `**` delimiters hidden

#### Scenario: Inline code renders on non-active line
- **WHEN** the editor contains `Use the `config.json` file` and the cursor is on a different line
- **THEN** "config.json" is rendered in monospace with a background highlight, backticks hidden

#### Scenario: Link renders on non-active line
- **WHEN** the editor contains `See [the docs](https://example.com) for details` and the cursor is on a different line
- **THEN** "the docs" is rendered as styled link text with `](https://example.com)` hidden

#### Scenario: Multiple elements on one line
- **WHEN** a non-active line contains `## **Bold heading** with *italic*`
- **THEN** the `## ` marker is hidden, "Bold heading" is bold, "italic" is italic, and the heading styling is applied to the full line

### Requirement: Bullet list rendering with indent and dedent
Bullet list items (`- item`) SHALL render with the `- ` marker replaced by a `•` bullet character on non-active lines. Pressing Tab on a list item line SHALL indent the item by adding leading spaces. Pressing Shift+Tab SHALL dedent the item by removing leading spaces. Pressing Enter at the end of a list item SHALL create a new line with `- ` prefix to continue the list. Pressing Enter on an empty list item (`- ` with no content) SHALL remove the list marker and create a blank line.

#### Scenario: Bullet renders on non-active line
- **WHEN** the editor contains `- Buy groceries` and the cursor is on a different line
- **THEN** the line displays `• Buy groceries` with the `- ` replaced by `• `

#### Scenario: Tab indents list item
- **WHEN** the cursor is on a line containing `- Sub item` and the user presses Tab
- **THEN** the line becomes `  - Sub item` (indented by 2 spaces)

#### Scenario: Shift+Tab dedents list item
- **WHEN** the cursor is on a line containing `  - Sub item` and the user presses Shift+Tab
- **THEN** the line becomes `- Sub item` (dedented by 2 spaces)

#### Scenario: Enter continues list
- **WHEN** the cursor is at the end of a line containing `- First item` and the user presses Enter
- **THEN** a new line is created with `- ` prefix and the cursor is placed after the prefix

#### Scenario: Enter on empty list item ends list
- **WHEN** the cursor is on a line containing only `- ` and the user presses Enter
- **THEN** the `- ` is removed and a blank line remains with the cursor on it

### Requirement: Checkbox widget rendering with click toggle
Lines matching `- [ ] ` and `- [x] ` SHALL render as interactive checkbox widgets on non-active lines. The `- [ ] ` pattern SHALL display as an unchecked checkbox input followed by the text. The `- [x] ` pattern SHALL display as a checked checkbox input followed by the text. Clicking a checkbox widget SHALL toggle the source text between `[ ]` and `[x]` via a CM6 transaction. On the active line (cursor present), raw checkbox syntax SHALL be shown instead of the widget.

#### Scenario: Unchecked checkbox renders as widget
- **WHEN** the editor contains `- [ ] Buy milk` on a non-active line
- **THEN** an unchecked checkbox input is displayed followed by "Buy milk"

#### Scenario: Checked checkbox renders as widget
- **WHEN** the editor contains `- [x] Done item` on a non-active line
- **THEN** a checked checkbox input is displayed followed by "Done item"

#### Scenario: Clicking checkbox toggles state
- **WHEN** a user clicks an unchecked checkbox widget for `- [ ] Buy milk`
- **THEN** the source text is updated to `- [x] Buy milk` and the widget displays as checked

#### Scenario: Clicking checked checkbox unchecks it
- **WHEN** a user clicks a checked checkbox widget for `- [x] Done item`
- **THEN** the source text is updated to `- [ ] Done item` and the widget displays as unchecked

#### Scenario: Checkbox on active line shows raw syntax
- **WHEN** the user moves the cursor to a line containing `- [ ] Buy milk`
- **THEN** the raw text `- [ ] Buy milk` is displayed without a checkbox widget

### Requirement: Entity mention widgets always rendered as styled chips
Entity mentions in the formats `@[person:ID|Label]` and `[[type:ID|Label]]` (where type is `page`, `task`, `org`, or `project`) SHALL always render as styled inline chip widgets, regardless of whether the cursor is on that line. Each chip SHALL display a type badge emoji and the label text. The raw mention syntax SHALL never be visible to the user. Pressing Backspace at the position immediately after a mention chip SHALL delete the entire mention (atomic deletion).

#### Scenario: Person mention renders as chip
- **WHEN** the editor contains `Met with @[person:7|John Smith] today`
- **THEN** `@[person:7|John Smith]` is replaced by a styled chip showing "John Smith"

#### Scenario: Task mention renders as chip
- **WHEN** the editor contains `- [ ] [[task:42|Call the dentist]]`
- **THEN** `[[task:42|Call the dentist]]` is replaced by a styled chip showing "Call the dentist"

#### Scenario: Page link renders as chip
- **WHEN** the editor contains `See [[page:3|Meeting Notes]] for details`
- **THEN** `[[page:3|Meeting Notes]]` is replaced by a styled chip showing "Meeting Notes"

#### Scenario: Mention chip always visible on active line
- **WHEN** the cursor is on a line containing `@[person:7|John Smith]`
- **THEN** the mention still renders as a "John Smith" chip (not raw syntax)

#### Scenario: Backspace deletes entire mention
- **WHEN** the cursor is positioned immediately after a mention chip and the user presses Backspace
- **THEN** the entire mention syntax (e.g., `@[person:7|John Smith]`) is deleted

### Requirement: Mention autocomplete for people and entities
The CM6 editor SHALL provide autocomplete suggestions when the user types `@` followed by characters (for people) or `[[` (for entities). The people autocomplete SHALL filter the loaded people list by first/last name matching the typed query, showing up to 8 results. The entity autocomplete SHALL search across pages, tasks, organizations, and projects, showing up to 12 results with type badges. Selecting a completion SHALL insert the full mention syntax (`@[person:ID|Label]` or `[[type:ID|Label]]`) and the mention widget SHALL render immediately.

#### Scenario: Person autocomplete triggers on @
- **WHEN** the user types `@Jo` in the editor
- **THEN** an autocomplete dropdown appears showing people whose names contain "Jo" (e.g., "John Smith", "Jo Adams")

#### Scenario: Entity autocomplete triggers on [[
- **WHEN** the user types `[[meet` in the editor
- **THEN** an autocomplete dropdown appears showing matching pages, tasks, orgs, and projects with type badges

#### Scenario: Selecting person autocomplete inserts mention
- **WHEN** the user selects "John Smith" from the person autocomplete
- **THEN** the text `@Jo` is replaced with `@[person:7|John Smith]` and the mention renders as a chip

#### Scenario: Selecting entity autocomplete inserts link
- **WHEN** the user selects a page "Meeting Notes" from the entity autocomplete
- **THEN** the text `[[meet` is replaced with `[[page:3|Meeting Notes]]` and the mention renders as a chip

#### Scenario: Escape closes autocomplete
- **WHEN** the autocomplete dropdown is open and the user presses Escape
- **THEN** the dropdown closes without inserting anything

### Requirement: Content rewrite handling preserves cursor position
When the save response returns content that differs from the current CM6 document (due to server-side checkbox-to-task rewriting), the editor SHALL apply the changes via a targeted CM6 transaction that patches only the modified lines, preserving the user's cursor position and scroll state. If the user has made further edits between the save request and the save response, the patch SHALL be skipped to avoid conflicts (the next debounced save will reconcile).

#### Scenario: Server rewrites checkbox to task link
- **WHEN** the user typed `- [ ] Buy milk`, the save fires, and the server returns `- [ ] [[task:99|Buy milk]]`
- **THEN** the editor patches that specific line to include the task link without moving the cursor or scrolling

#### Scenario: User edited during save round-trip
- **WHEN** the save was based on document version A, but the user has since typed more (document is now version B), and the server returns rewritten version of A
- **THEN** the patch is skipped and the current document is preserved as-is

### Requirement: Theme integration with CSS variables
The CM6 editor theme SHALL reference the application's existing CSS variables for all visual properties. The editor SHALL support light and dark modes automatically via the `data-theme` attribute on `<html>`. The editor's font family, font size, line height, border, and border-radius SHALL match the current textarea styling.

#### Scenario: Editor matches app theme in light mode
- **WHEN** the app is in light mode
- **THEN** the CM6 editor uses light-mode CSS variable values for background, text color, borders, and selection

#### Scenario: Editor matches app theme in dark mode
- **WHEN** the user switches to dark mode
- **THEN** the CM6 editor immediately reflects dark-mode CSS variable values without re-initialization
