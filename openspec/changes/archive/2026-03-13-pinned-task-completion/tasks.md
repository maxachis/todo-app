## 1. Add completion checkbox to PinnedSection

- [x] 1.1 Import `completeTask` from `$lib/stores/tasks` in `PinnedSection.svelte`
- [x] 1.2 Add a checkbox `<input type="checkbox">` before the task title in each pinned row
- [x] 1.3 Add click handler on checkbox that calls `completeTask(entry.task.id)` with `event.stopPropagation()` to prevent jump-to-task
- [x] 1.4 Style the checkbox consistent with task row checkboxes (size, cursor, spacing)

## 2. Verify behavior

- [x] 2.1 Verify completing a pinned task removes it from the pinned section
- [x] 2.2 Verify clicking the checkbox does not scroll to or select the task
- [x] 2.3 Verify recurring task completion shows the next-occurrence toast
- [x] 2.4 Run `cd frontend && npm run check` to confirm no type errors
