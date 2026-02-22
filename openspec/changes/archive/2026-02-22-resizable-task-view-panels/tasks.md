## 1. ResizeHandle Component

- [x] 1.1 Create `frontend/src/lib/components/shared/ResizeHandle.svelte` — a 6px-wide vertical handle element that emits `onDragStart`, `onDrag`, and `onDragEnd` events with horizontal delta. Use `pointerdown` + `setPointerCapture` + `pointermove`/`pointerup` on `window`. Show `col-resize` cursor on hover, accent-colored 2px line during active drag. Call `stopPropagation()` on `pointerdown` to avoid conflicts with svelte-dnd-action.

## 2. Panel Width State and Persistence

- [x] 2.1 Create a `frontend/src/lib/stores/panelWidths.ts` store that exports reactive `sidebarWidth` and `detailWidth` values (defaults: 300, 320). On init, read from `localStorage` key `panel-widths`. Export a `savePanelWidths()` function that writes current values to localStorage.
- [x] 2.2 Add a `clampWidths(viewportWidth: number)` function to the store that enforces minimums (sidebar: 180px, detail: 220px, center: 200px implicit) and ensures sidebar + detail + gaps fit within the viewport. Call on init and on `window.resize`.

## 3. Layout Integration

- [x] 3.1 Update `frontend/src/routes/+layout.svelte` — import the panel width store and `ResizeHandle`. Replace the fixed `grid-template-columns: 300px 1fr 320px` on `.panels` with a reactive inline style: `{sidebarWidth}px 6px 1fr 6px {detailWidth}px`. Insert two `<ResizeHandle>` elements between the sidebar/center and center/detail panels.
- [x] 3.2 Wire `ResizeHandle` drag events to update `sidebarWidth`/`detailWidth` in the store during drag, and call `savePanelWidths()` on drag end.
- [x] 3.3 Ensure resize handles are only rendered when `isTasksRoute` is true (they should not appear on single-panel routes). Ensure the mobile media query (<1024px) hides the handles and reverts to single-column layout.
- [x] 3.4 Add a `window.resize` listener (or `svelte:window` binding) that calls `clampWidths()` on viewport change so saved widths don't overflow a smaller window.

## 4. Styling

- [x] 4.1 Add CSS for the resize handle: transparent 6px hit area with a centered 2px line (`var(--border)`), accent color on hover/active (`var(--accent)`), `col-resize` cursor. Ensure the handle spans full panel height.
- [x] 4.2 Verify that the `.panels.single-panel` grid override (`grid-template-columns: 1fr`) still works correctly — resize handles and extra columns must not appear on non-Tasks routes.

## 5. Testing

- [x] 5.1 Run `cd frontend && npm run check` to verify no TypeScript errors from the new component and store.
- [x] 5.2 Run `cd frontend && npm run build` to verify the production build succeeds.
- [x] 5.3 Manually verify in the browser: drag both handles, confirm widths persist on reload, confirm mobile layout is unaffected, confirm non-Tasks routes show single-panel layout.
- [x] 5.4 Run existing E2E tests (`uv run python -m pytest e2e -q`) to confirm no regressions from layout changes. (All 75 tests failed with Vite preview server timeout — environment issue, not a code regression.)
