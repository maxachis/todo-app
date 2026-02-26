## 1. Empty-state placeholder

- [x] 1.1 In `MarkdownEditor.svelte`, add a conditional block that renders a `.block-placeholder` element with muted "Click to add notes..." text when blocks contain only an empty string
- [x] 1.2 Style `.block-placeholder` with muted color (`var(--text-muted)`), italic text, and adequate padding for a comfortable click target
- [x] 1.3 Wire the placeholder click to call `startEdit(0)` so clicking opens the editor

## 2. Hover pencil icon

- [x] 2.1 Add a CSS `::after` pseudo-element on `.block-render` that displays a pencil character (✎) positioned top-right, hidden by default
- [x] 2.2 Show the `::after` pencil on `.block-render:hover` and `.block-render:focus-visible` with muted color and small font size
- [x] 2.3 Ensure the pencil icon does not appear on the empty-state placeholder block

## 3. Keyboard focus affordance

- [x] 3.1 Add `:focus-visible` styles to `.block-render` matching the existing hover styles (border color, background) so keyboard navigation shows the same cues

## 4. Verify

- [x] 4.1 Manually verify: empty notes show placeholder, clicking placeholder opens editor
- [x] 4.2 Manually verify: hovering a content block shows pencil icon + border/background
- [x] 4.3 Manually verify: Tab-focusing a content block shows the same affordance as hover
- [x] 4.4 Run `cd frontend && npm run check` to confirm no type or lint errors
