## 1. Fix TaskRow keydown handler

- [x] 1.1 Add text-entry guard to the `.task-row` `onkeydown` handler in `frontend/src/lib/components/tasks/TaskRow.svelte` (lines 148–153): if `event.target` is inside `input, textarea, select, [contenteditable="true"]`, return early before processing Space/Enter

## 2. Verify

- [x] 2.1 Run `cd frontend && npm run check` to confirm no type or lint errors
- [x] 2.2 Manually verify: double-click a task to inline-edit, confirm space inserts a character; press Escape, confirm space re-selects the task row as before
