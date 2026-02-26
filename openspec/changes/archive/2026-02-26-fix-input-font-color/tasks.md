## 1. Fix inline-edit input backgrounds

- [x] 1.1 Add `background: var(--bg-input)` to `.title-input` in `frontend/src/lib/components/tasks/TaskRow.svelte`
- [x] 1.2 Add `background: var(--bg-input)` to `.name-input` in `frontend/src/lib/components/sections/SectionHeader.svelte`
- [x] 1.3 Add `background: var(--bg-input)` to `input` rule in `frontend/src/lib/components/lists/ListItem.svelte`
- [x] 1.4 Add `background: var(--bg-input)` to `.edit-input` in `frontend/src/routes/projects/+page.svelte`
- [x] 1.5 Add `background: var(--bg-input)` to `.block-editor` in `frontend/src/lib/components/shared/MarkdownEditor.svelte`

## 2. Ensure text color consistency

- [x] 2.1 Verify each input in tasks 1.1–1.5 has `color: var(--text-primary)` — add where missing

## 3. Verify

- [x] 3.1 Visual check: all edited inputs are readable in dark mode (dark background, light text)
- [x] 3.2 Visual check: all edited inputs are readable in light mode (white background, dark text)
- [x] 3.3 Run `cd frontend && npm run check` to confirm no type/lint errors
