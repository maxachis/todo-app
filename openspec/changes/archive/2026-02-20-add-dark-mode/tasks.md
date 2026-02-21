## 1. FOUC Prevention & App Entry Point

- [x] 1.1 Add inline `<script>` to `frontend/src/app.html` `<head>` that reads `localStorage('theme')` and `prefers-color-scheme`, then sets `data-theme` on `<html>` before body renders

## 2. Theme Store

- [x] 2.1 Create `frontend/src/lib/stores/theme.ts` with a writable store holding `'light' | 'dark' | 'system'`
- [x] 2.2 Initialize store from `localStorage` (default `'system'`), sync changes to `localStorage` and `document.documentElement.dataset.theme`
- [x] 2.3 Add `matchMedia('(prefers-color-scheme: dark)')` listener that updates resolved theme when preference is `'system'`

## 3. Dark Color Palette

- [x] 3.1 Add `:root[data-theme="dark"]` block in `frontend/src/routes/+layout.svelte` overriding all CSS variables (backgrounds, text, borders, accents, shadows, status, pinned, tag colors)
- [x] 3.2 Audit components for hardcoded color values (hex/rgb literals outside CSS variables) and migrate them to use CSS variables — check `TaskRow.svelte`, `TaskDetail.svelte`, `SectionHeader.svelte`, `ListSidebar.svelte`, `Toast.svelte`, `SearchBar.svelte`, `PinnedSection.svelte`, `EmojiPicker.svelte`

## 4. Theme Toggle UI

- [x] 4.1 Create theme toggle component or add toggle markup in `frontend/src/routes/+layout.svelte` nav bar (between nav links and SearchBar)
- [x] 4.2 Implement cycle behavior: click cycles light → system → dark → light, with icon/label updating to reflect current state
- [x] 4.3 Ensure toggle is keyboard accessible (Enter/Space triggers cycle)

## 5. Verification

- [x] 5.1 Visually verify all pages (Tasks, Projects, Timesheet, Import) in dark mode — panels, sidebar, detail panel, forms, modals
- [x] 5.2 Verify drag-and-drop ghost elements are legible in dark mode
- [x] 5.3 Verify emoji picker renders correctly in dark mode
- [x] 5.4 Verify toast notifications (success, error, info) are legible in dark mode
- [x] 5.5 Verify no FOUC when loading with dark preference saved
- [x] 5.6 Run `npm run check` in `frontend/` to confirm no type errors
