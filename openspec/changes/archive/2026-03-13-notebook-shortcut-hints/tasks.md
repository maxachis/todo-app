## 1. Update ShortcutHints Component

- [x] 1.1 Add optional `sections` prop to `ShortcutHints.svelte` accepting `{ title: string, shortcuts: Shortcut[] }[]` and render grouped sections with headings when provided, falling back to flat rendering when only `shortcuts` is passed
- [x] 1.2 Style the section headings to visually separate groups within the popover

## 2. Update Notebook Page

- [x] 2.1 Update `frontend/src/routes/notebook/+page.svelte` to pass `sections` prop with a "Shortcuts" group (Ctrl+\) and a "Syntax" group (@Name, @new[Name], [[, - [ ])

## 3. Verify

- [x] 3.1 Run `cd frontend && npm run check` to confirm no type errors
