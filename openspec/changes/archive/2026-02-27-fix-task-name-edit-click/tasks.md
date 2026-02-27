## 1. Fix event propagation

- [x] 1.1 Add `onclick={(e) => e.stopPropagation()}` to the `<input class="title-input">` in `frontend/src/lib/components/tasks/TaskRow.svelte` (around line 194)

## 2. Verify

- [x] 2.1 Run `cd frontend && npm run check` to confirm no type/lint errors
- [x] 2.2 Manually verify: double-click a task title to enter edit mode, then click within the input — edit mode should remain active
