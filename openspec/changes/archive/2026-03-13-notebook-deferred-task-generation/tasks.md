## 1. Backend: Add process_checkboxes flag

- [x] 1.1 Add `process_checkboxes: bool = True` field to `PageUpdateInput` in `notebook/api/schemas.py`
- [x] 1.2 Add `process_checkboxes` parameter to `reconcile_mentions()` in `notebook/mentions.py`; skip `create_tasks_from_checkboxes()` when `False`
- [x] 1.3 Pass `payload.process_checkboxes` through in `update_page()` in `notebook/api/pages.py`

## 2. Frontend: API client update

- [x] 2.1 Update the notebook page update API call in `frontend/src/lib/api/` to accept and forward `process_checkboxes` parameter

## 3. Frontend: Wire save modes

- [x] 3.1 Update `savePage()` in `+page.svelte` to accept a `processCheckboxes` parameter (default `true`)
- [x] 3.2 Update `debouncedSave()` to call `savePage(false)` — typing saves skip task generation
- [x] 3.3 Update `handleContentBlur()` to call `savePage(true)` — blur saves trigger task generation
- [x] 3.4 Update `handleTitleBlur()` to call `savePage(true)`

## 4. Frontend: Enter-after-checkbox detection

- [x] 4.1 Add `onCheckboxNewline` callback to `createEditor` options in `frontend/src/lib/components/notebook/createEditor.ts` — detect Enter on a checkbox line (matching `- [ ] <text>` without `[[task:`) and invoke the callback
- [x] 4.2 Wire the callback in `+page.svelte` to trigger immediate `savePage(true)`

## 5. Verify

- [x] 5.1 Run `cd frontend && npm run check` to confirm no type errors (0 errors); notebook tests all pass (33/33)
- [ ] 5.2 Manual verification: type a checkbox, pause typing — no task created; press Enter or blur — task created
