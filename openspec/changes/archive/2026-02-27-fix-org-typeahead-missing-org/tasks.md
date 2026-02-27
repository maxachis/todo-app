## 1. Component Logic

- [x] 1.1 Add `showNoMatch` derived state in `TypeaheadSelect.svelte`: true when `inputText` is non-empty, `filtered` is empty, and `onCreate` is undefined
- [x] 1.2 Update `handleInput` dropdown-open condition (line 99) to include `showNoMatch` alongside `showCreateOption`
- [x] 1.3 Update `open()` function condition (line 59) to include `showNoMatch`

## 2. Template

- [x] 2.1 Update the `{#if}` guard on the `<ul>` dropdown (line 205) to include `showNoMatch`
- [x] 2.2 Add a non-selectable `<li>` with `role="status"` rendering "No match found — add it first" when `showNoMatch` is true (no `onmousedown`, no hover highlight, not in `totalItems`)

## 3. Styling

- [x] 3.1 Add `.typeahead-no-match` CSS class with muted text styling (similar to `.typeahead-create` but non-interactive: `cursor: default`, muted color, italic)

## 4. Verification

- [x] 4.1 Test manually: type a non-existent name in a TypeaheadSelect without `onCreate` (e.g., LinkedEntities org selector) — dropdown should stay open with "No match found" message
- [x] 4.2 Test manually: type a non-existent name in a TypeaheadSelect with `onCreate` (e.g., org type on organizations page) — should still show "Create [text]" as before
- [x] 4.3 Test manually: typed text is preserved while "No match found" is visible; pressing Escape or clicking outside clears normally
- [x] 4.4 Run `cd frontend && npm run check` to verify no type errors
