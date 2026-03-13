## Context

Task detail notes currently use `MarkdownEditor.svelte` which splits content into blocks and provides per-block textarea editing with blur-to-render. The notebook already has a CodeMirror 6 editor (`createEditor` in `notebook/createEditor.ts`) with live preview, checkboxes, list keymaps, and mention completion. We want the same live-editing experience for task notes, minus mentions.

## Goals / Non-Goals

**Goals:**
- Replace MarkdownEditor in TaskDetail with a CodeMirror editor that has live markdown preview
- Reuse existing notebook modules for consistency

**Non-Goals:**
- Adding mention/linking to task notes
- Changing MarkdownEditor.svelte (it may be used elsewhere or can be cleaned up later)

## Decisions

### 1. Create a slim editor factory vs. parameterize the existing one

**Decision**: Create a new `createNotesEditor` function that builds a CodeMirror instance with a subset of extensions (no mentions, no autocompletion). This lives alongside the notebook's `createEditor`.

**Rationale**: The notebook editor has mention-specific types and callbacks baked into its interface. Parameterizing it would complicate its API. A separate slim factory is cleaner and only ~30 lines.

### 2. Svelte wrapper component

**Decision**: Create `NotesEditor.svelte` as a thin Svelte wrapper that manages the CodeMirror lifecycle (mount, update content from props, destroy). It accepts `value` and `onSave` props matching the existing MarkdownEditor interface.

**Rationale**: Keeps the TaskDetail integration simple — just swap `<MarkdownEditor>` for `<NotesEditor>` with the same props.

### 3. Theme reuse

**Decision**: Reuse `notebookTheme` from `notebook/theme.ts` directly. Add a compact size override in the notes editor for the task detail context (smaller default height, auto-grow).

### 4. Blur behavior

**Decision**: On `focusout`, call `onSave` with the current editor content. This matches the existing MarkdownEditor blur-to-save behavior.

## Risks / Trade-offs

- **Bundle size**: CodeMirror is already loaded for notebook, so no additional download cost.
- **Height management**: The editor needs to auto-grow with content but not take unbounded space. Use a min-height with CSS and CodeMirror's line wrapping.
