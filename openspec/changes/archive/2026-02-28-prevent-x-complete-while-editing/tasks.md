## 1. Guard destructive shortcuts

- [x] 1.1 In `frontend/src/lib/actions/keyboard.ts`, modify the "x" key handler (line ~144) to check that `eventElement` is not null before calling `onCompleteTask`. If `eventElement` is null (focus is not on a `[data-task-id]` element), return early without acting.
- [x] 1.2 In `frontend/src/lib/actions/keyboard.ts`, modify the "Delete" key handler (line ~150) to check that `eventElement` is not null before showing the confirmation dialog. If `eventElement` is null, return early without acting.

## 2. Verification

- [x] 2.1 Run `cd frontend && npm run check` to verify no TypeScript or lint errors.
- [x] 2.2 Run `uv run python -m pytest e2e -q` to confirm existing E2E tests still pass (fixed 2 tests that dispatched Delete event on scope instead of task row).
- [ ] 2.3 Manual test: select a task, click a non-task-row element in the center panel (e.g., "Add section" input), press "x" — confirm task is NOT completed.
- [ ] 2.4 Manual test: select a task, focus on the task row, press "x" — confirm task IS completed as before.
