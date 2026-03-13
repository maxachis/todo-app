## 1. Add Delete Button to Task Detail

- [x] 1.1 Import `deleteTask` from `$lib/stores/tasks` in `TaskDetail.svelte`
- [x] 1.2 Add `handleDelete` async function that calls `confirm()` then `deleteTask(task.id)`
- [x] 1.3 Add "Delete" button markup at bottom of `.detail` div, after NotebookMentions
- [x] 1.4 Add destructive button styles (red/error color, border, hover state) to `<style>` block

## 2. Verify

- [x] 2.1 Run `cd frontend && npm run check` to verify no type errors
- [ ] 2.2 Manually test: select task → click Delete → confirm → task removed, detail cleared
- [ ] 2.3 Manually test: select task → click Delete → cancel → task remains
