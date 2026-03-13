## 1. Create ShortcutHints Component

- [x] 1.1 Create `frontend/src/lib/components/shared/ShortcutHints.svelte` with `shortcuts` prop (array of `{ key: string, description: string }`), fixed-position `?` badge, click-to-toggle popover opening upward, and click-outside-to-close behavior
- [x] 1.2 Style the component using existing CSS custom properties for light/dark theme support

## 2. Integrate on Pages

- [x] 2.1 Add `ShortcutHints` to `frontend/src/routes/+page.svelte` (Tasks) with all 9 task shortcuts
- [x] 2.2 Add `ShortcutHints` to `frontend/src/routes/notebook/+page.svelte` (Notebook) with sidebar toggle shortcut

## 3. Verify

- [x] 3.1 Run `cd frontend && npm run check` to confirm no type errors
