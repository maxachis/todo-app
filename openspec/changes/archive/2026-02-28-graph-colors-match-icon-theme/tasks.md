## 1. Read theme colors from CSS variables

- [x] 1.1 In `frontend/src/routes/graph/+page.svelte`, at the top of `initGraph`, add a helper that reads `--accent`, `--text-primary`, `--text-tertiary`, and `--border` from `getComputedStyle(document.documentElement)` and returns them as an object

## 2. Replace hardcoded colors with theme values

- [x] 2.1 Replace organization node fill `#f97316` with the resolved `--accent` value (`frontend/src/routes/graph/+page.svelte` line 177)
- [x] 2.2 Replace person node fill `#4f46e5` with the resolved `--text-tertiary` value (same file, line 177)
- [x] 2.3 Replace edge stroke `#9ca3af` with the resolved `--border` value (line 156)
- [x] 2.4 Replace edge note label fill `#6b7280` with the resolved `--text-tertiary` value (line 167)
- [x] 2.5 Replace node label fill `#374151` with the resolved `--text-primary` value (line 205)

## 3. Theme change reactivity

- [x] 3.1 Add a `MutationObserver` on `document.documentElement` watching for `data-theme` attribute changes. On change, re-read CSS variables and update all D3 element colors in place (node fills, edge strokes, label fills). Disconnect the observer in the `onMount` cleanup return.

## 4. Verify

- [x] 4.1 Run `cd frontend && npm run check` to verify no type errors
- [x] 4.2 Manually confirm: graph loads with accent-colored org nodes, muted person nodes, and theme-aware edges/labels in both light and dark mode
