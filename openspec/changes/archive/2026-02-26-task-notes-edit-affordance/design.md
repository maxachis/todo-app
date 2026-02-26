## Context

The task detail panel includes a Notes field powered by the `MarkdownEditor` component. This component splits content into blocks, renders each as HTML via `marked` + `DOMPurify`, and switches to a textarea on click. Currently, rendered blocks look like static text — the only hints are a `cursor: text` and a subtle border/background on hover. Empty notes show an empty invisible block with no prompt.

## Goals / Non-Goals

**Goals:**
- Make it visually discoverable that notes are editable without requiring hover or click
- Provide a clear empty-state prompt so users know where to start
- Keep changes minimal and non-intrusive — subtle cues, not heavy chrome

**Non-Goals:**
- Changing the editing mechanics (block-based, textarea, blur-to-save)
- Adding a toolbar, formatting buttons, or WYSIWYG features
- Modifying the backend, API, or data model
- Changing the Notes section label or layout in TaskDetail

## Decisions

### 1. Pencil icon on hover via CSS pseudo-element

**Choice**: Show a small pencil (✎) icon in the top-right corner of `.block-render` on hover/focus, using a CSS `::after` pseudo-element.

**Why over alternatives**:
- *Inline SVG icon*: Requires markup changes and an icon library/asset — overkill for one symbol.
- *Always-visible icon*: Adds visual noise. Hover-only keeps the clean look.
- *Tooltip*: Not discoverable without hovering; doesn't help with empty state.

The pseudo-element approach is zero-dependency, purely CSS, and easy to remove later.

### 2. Placeholder text for empty state

**Choice**: When `blocks()` yields a single empty string, render a `.block-placeholder` element with muted "Click to add notes..." text. Clicking it triggers `startEdit(0)`.

**Why**: The current empty state renders an invisible empty block — users see nothing and have no reason to click. A placeholder follows standard form conventions (like `<input placeholder>`).

### 3. Enhanced hover styling

**Choice**: Keep existing hover border/background but also show the same styles on `:focus-visible` for keyboard users. No changes to the base hover colors — the pencil icon is the primary new affordance.

## Risks / Trade-offs

- **Pencil character rendering**: The ✎ (U+270E) character renders differently across OS/fonts. → Mitigation: Use a simple Unicode pencil that degrades gracefully; it's decorative, not functional.
- **Empty-state click target**: Placeholder text is smaller than a full block. → Mitigation: Apply padding to ensure a reasonable click target area.
